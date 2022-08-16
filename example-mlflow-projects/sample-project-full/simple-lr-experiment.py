import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error
import mlflow
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import os
from sys import argv
from hashlib import sha256
from pathlib import Path
import yaml
import json


# TODO significant code cleanup required
def get_data(params, use_cache):
    seed = params['random_seed']
    n_points = params['n_points']
    mlflow.set_tags({'dataset_seed': seed, 'dataset_n_points': n_points})
    cache_path = Path('/mnt','cache', '{}-{}.json'.format(seed, n_points))
    
    # attempt to load cached processed data
    data_loaded=False
    if use_cache == "true" and cache_path.is_file():
        with open(cache_path, 'r') as f:
            data = json.load(f)
        if checksum(data) == data['sha256_sum']:
            # convert back from list to numpy array
            x = np.asarray(data['x'])
            y = np.asarray(data['y'])
            # indicate data successfully loaded   
            data_loaded = True
    
    # processed data could not be loaded, generate new dataset
    if not data_loaded:
        rng = np.random.default_rng(seed)
        x = (np.linspace(5,25,n_points) + rng.uniform(size=20)-0.5)[:, np.newaxis]
        y = (3 - 11.5*x + 4.8*x**1.7 - 0.65 * x ** 2.2)[:,0] \
                + ((rng.uniform(size=n_points) - 0.5)*5)
        
        # save processed data to cache
        data = {'x': x.tolist(), 'y': y.tolist()}
        data['sha256_sum'] = checksum(data)
        with open(cache_path, 'w') as f:
            json.dump(data, f)
    return x, y


def checksum(data):
    cs = sha256()
    for key in ('x','y'):
        cs.update(','.join(str(x) for x in data[key]).encode('utf-8'))
    return cs.hexdigest()


def main():
    
        
    with mlflow.start_run() as run:
        mlflow.set_tags({'mlflow.runName': 'linear regression test', 
        'description':'basic example of mlflow functionality'})

    
        with open('/mnt/params.json', 'r') as f:
            params = yaml.safe_load(f)
        x, y = get_data(params, use_cache=os.environ['USE_CACHE'])
            
        degree = abs(int(argv[1]))
        mlflow.log_param('degree', degree)        

        model = Pipeline([('poly', PolynomialFeatures(degree=degree)),
                   ('linear', LinearRegression(fit_intercept=False))])
        model.fit(x, y)
        yp = model.predict(x)
        
        r2 = r2_score(y, yp)
        mse = mean_squared_error(y, yp)
        
        mlflow.log_metrics(
                    {   'mse': mse,
                        'r-squared': r2
                }
        )

        mlflow.sklearn.log_model(model, 'model')


        y_pred = model.predict(x)
        
        residuals_x = np.repeat(x.squeeze(), 3)
        residuals_y = np.zeros_like(residuals_x)
        residuals_y[::3] = y_pred
        residuals_y[1::3] = y
        residuals_y[2::3] = np.nan

        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            name='residuals',
            x=residuals_x,
            y=residuals_y,
            mode='lines',
            legendrank=3,
            line={'width':1, 'color': 'red'}
            ))
        fig.add_trace(go.Scatter(
            name='data',
            mode='markers',
            x=x[:, 0],
            legendrank=2,
            y=y
            ))
        fig.add_trace(go.Scatter(
            name='fit (degree={})'.format(degree),
            mode='lines',
            x=x[:, 0],
            legendrank=1,
            y=y_pred))

        fig.write_html('/home/mlf-project/results.html')
        mlflow.log_artifact('/home/mlf-project/results.html')
        os.remove('/home/mlf-project/results.html')


if __name__ == "__main__":
    main()
        
