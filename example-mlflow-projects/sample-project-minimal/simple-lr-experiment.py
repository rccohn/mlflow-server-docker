"""
Very simple linear regression experiment to show core mlflow functionality.
A synthetic dataset of x and y coordinates is generated, and a simple
linear regression model is fit to the data. Model parameters, performance
metrics, and the model itself are saved to the mlflow tracking database.

"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import mlflow
from plotly import graph_objects as go


def get_sample_data(seed=42):
    """
    Generate synthetic dataset for linear regression.

    Parameters
    ----------
    seed: int
        random seed for noise added to y coordinates.

    Returns
    ---------
    x, y: ndarry
        arrays of floating point values.
        x is a n x 1 array of inputs.
        y is a n-element array of prediction targets.
    """
    xcoords = np.linspace(0, 20, 50)

    rng = np.random.default_rng(seed)

    # add noise so there isn't a perfect fit
    noise = (rng.random(size=(xcoords.shape)) - 0.5) * 2

    ycoords = 2 * xcoords + 3 + noise

    # sklearn expects x to be 2d (n_sample x n_feature) so
    # we return x[:, np.newaxis]
    return xcoords[:, np.newaxis], ycoords


def main():
    # tags contain arbitrary descriptive data about the run
    mlflow.set_tags(
        {
            "mlflow.runName": "linear regression test",
            "description": "basic example of mlflow functionality",
        }
    )

    x, y = get_sample_data()  # get dataset

    # fit sklearn linear regression model to data
    lr = LinearRegression()
    reg = lr.fit(x, y)

    # evaulate the model based on r-squared score and MSE loss
    r2 = lr.score(x, y)
    yp = lr.predict(x)
    mse = mean_squared_error(y, yp)

    # save model parameters to tracking database
    mlflow.log_params(
        {
            "slope": reg.coef_[0],
            "intercept": reg.intercept_,
        }
    )

    # save model performance metrics to tracking database
    mlflow.log_metrics({"r-squared": r2, "mse": mse})

    # log the model itself as a tracking artifact
    mlflow.sklearn.log_model(lr, "model")

    # visualize results
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="data", mode="markers", x=x[:, 0], y=y))
    fig.add_trace(go.Scatter(name="fit", mode="lines", x=x[:, 0], y=yp))

    # Save figure as mlflow tracking artifact.
    # By saving as html instead of image, the figure
    # can be interacted with in the mlflow user interface.
    fig.write_html("results.html")
    mlflow.log_artifact("results.html")


if __name__ == "__main__":
    main()
