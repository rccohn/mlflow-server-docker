"""
Very simple linear regression experiment to show mlflow functionality, but
adds some complexities compared to the minimal example. Fits a polynomial
function to a synthetic dataset.
  - Reading desired degree of polynomial from command line
  - Read input file for dataset parameters from file mounted to container
  - Save processed data to a cache so it does not have to be recomputed
    if project is run again with new paremeters.
"""
from hashlib import sha256
import json
import mlflow
import numpy as np
import os
from plotly import graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sys import argv
import yaml


def get_data(params: dict, use_cache: bool):
    """
    Loads the dataset.

    If the dataset has already been processed, it is loaded from the cache.
    Otherwise, it is processed and saved to the cache.

    Parameters
    ----------
    params: dict
        contains parameters for generating dataset with the following keys:
            random_seed: int
                 seed for generating noise added to points
            n_points: int
                 number of points sampled in dataset
    Returns
    ---------
    x, y: ndarray
        x is a n_sample x 1 array of feature data
        y is a n_sample element array of regression targets

    """

    # load parameters for generating dataset
    seed = params["random_seed"]
    n_points = params["n_points"]
    mlflow.set_tags({"dataset_seed": seed, "dataset_n_points": n_points})

    # directory to save processed data cache
    cache_path = os.path.join(
        "/mnt/cache", "{}-{}.json".format(seed, n_points)
    )

    # attempt to load cached processed data
    data_loaded = False
    if use_cache == "true" and os.path.isdir(cache_path):
        print("Loading cached data")
        with open(cache_path, "r") as f:
            data = json.load(f)

        # ensure data has not changed on disk
        if checksum(data) == data["sha256_sum"]:
            print("hash matches- loading data")
            # convert back from list to numpy array
            x = np.asarray(data["x"])
            y = np.asarray(data["y"])
            # indicate data successfully loaded
            data_loaded = True

    # processed data could not be loaded, generate new dataset
    if not data_loaded:
        print("Cached data could not be loaded, processing data now")
        rng = np.random.default_rng(seed)
        x = (np.linspace(5, 25, n_points) + rng.uniform(size=20) - 0.5)[
            :, np.newaxis
        ]
        y = (3 - 11.5 * x + 4.8 * x**1.7 - 0.65 * x**2.2)[:, 0] + (
            (rng.uniform(size=n_points) - 0.5) * 5
        )

        # save processed data to cache
        data = {"x": x.tolist(), "y": y.tolist()}
        data["sha256_sum"] = checksum(data)
        with open(cache_path, "w") as f:
            json.dump(data, f)

    return x, y


def checksum(data: dict) -> str:
    """
    Compute sha256 hash of data loaded from disk.

    Used to confirm that the cached file has not been changed.

    Parameters
    ----------
    data: dict
        should have keys: 'x': list[list[float]]- feature data
                          'y': list[float]: regression targets
    Returns
    ----------
    checksum: str
        sha256 hash of data.
    """
    cs = sha256()

    # check keys in fixed order to ensure that the hash is always the same.
    for key in ("x", "y"):
        # convert list of numbers to string so it can be hashed
        cs.update(",".join(str(x) for x in data[key]).encode("utf-8"))
    return cs.hexdigest()


def main():

    with mlflow.start_run():

        # tags define run name and some descriptive data about the run
        mlflow.set_tags(
            {
                "mlflow.runName": "linear regression test",
                "description": "basic example of mlflow functionality",
            }
        )

        # run dataset parameters mounted to container
        with open("/mnt/params.json", "r") as f:
            params = yaml.safe_load(f)

        # save parameter file as artifact for reproducibility
        mlflow.log_artifact("/mnt/params.json", "dataset_params.json")

        # load the data
        x, y = get_data(params, use_cache=os.environ["USE_CACHE"])

        # this experiment takes a single integer input- the degree of the
        # polynomial used to fit the data
        degree = abs(int(argv[1]))
        mlflow.log_param("degree", degree)  # log degree as a mlflow parameter

        # create the sklearn polynomial regression model by combining
        # the linear regression model with polynomial features
        model = Pipeline(
            [
                ("poly", PolynomialFeatures(degree=degree)),
                ("linear", LinearRegression(fit_intercept=False)),
            ]
        )

        # train model
        model.fit(x, y)

        # generate predictions and evaluate model on the basis of r-squared
        # and MSE loss.
        yp = model.predict(x)
        r2 = r2_score(y, yp)
        mse = mean_squared_error(y, yp)

        # Save performance metrics to mlflow tracking database.
        mlflow.log_metrics({"mse": mse, "r-squared": r2})

        # Save the trained model to mlflow database.
        mlflow.sklearn.log_model(model, "model")

        # generate residuals for visualization
        residuals_x = np.repeat(x.squeeze(), 3)
        residuals_y = np.zeros_like(residuals_x)
        residuals_y[::3] = yp
        residuals_y[1::3] = y
        residuals_y[2::3] = np.nan

        fig = go.Figure()  # visualize prediction results

        # plot residuals first so they are on bottom of plot (z position)
        fig.add_trace(
            go.Scatter(
                name="residuals",
                x=residuals_x,
                y=residuals_y,
                mode="lines",
                legendrank=3,
                line={"width": 1, "color": "red"},
            )
        )
        # plot ground truth data
        fig.add_trace(
            go.Scatter(
                name="data", mode="markers", x=x[:, 0], legendrank=2, y=y
            )
        )
        # plot predicted data
        fig.add_trace(
            go.Scatter(
                name="fit (degree={})".format(degree),
                mode="lines",
                x=x[:, 0],
                legendrank=1,
                y=yp,
            )
        )

        # Save figure as artifact.
        # By saving as html instead of image figure will be
        # able to be interacted with in mlflow ui.
        fig.write_html("/home/mlf-project/results.html")
        mlflow.log_artifact("/home/mlf-project/results.html")
        os.remove("/home/mlf-project/results.html")


if __name__ == "__main__":
    main()
