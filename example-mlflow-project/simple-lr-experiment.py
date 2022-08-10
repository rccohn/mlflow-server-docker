import numpy as np
from sklearn.linear_model import LinearRegression
import mlflow
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import os
from sys import argv
import logging
from pathlib import Path
import json


# TODO significant code cleanup required
def get_sample_data(seed, paramfile='/mnt/params.json'):

    with open(paramfile, 'r') as f:
        params = json.load(f)
        
    xcoords = np.linspace(0, 20, params['n_points'])
    
    rng = np.random.default_rng(seed)
    noise = ((rng.random(size=(xcoords.shape))-0.5)*3)*xcoords
    
    ycoords = 2*xcoords+3+noise

    return xcoords[:, np.newaxis], ycoords


def main():
    logdir = '/mnt/logs/'
    logformat = '%(process)d-%(levelname)s-%(message)s'
    log_level = {'debug': logging.DEBUG, 'info': logging.INFO}[os.environ['LOGLEVEL']]
    print('testing')
    print([x for x in Path('/mlflow','projects','code').glob('*')])
    with mlflow.start_run() as run:
        logging.basicConfig(
            filename='{}/{}-{}.log'.format(logdir,
            run.info.experiment_id, run.info.run_id,
            ),
        level=log_level,
        format=logformat
        )
        logging.info('started project')

        mlflow.set_tags({'mlflow.runName': 'linear regression test', 
        'description':'basic example of mlflow functionality'})
        
        logging.debug('reading seed')
        seed = abs(int(argv[1]))
        
        mlflow.log_param('seed', seed)
        x, y = get_sample_data(seed)
        
        logging.info('creating model')
        lr = LinearRegression()
        reg = lr.fit(x, y)
        r2 = lr.score(x, y)
        
        mlflow.log_metrics(
                    {   'slope': reg.coef_[0],
                        'intercept': reg.intercept_,
                        'r-squared': r2
                }
        )

        mlflow.sklearn.log_model(lr, 'model')


        y_pred = lr.predict(x)

        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            name='data',
            mode='markers',
            x=x[:, 0],
            y=y
            ))
        fig.add_trace(go.Scatter(
            name='fit',
            mode='lines',
            x=x[:, 0],
            y=y_pred))

        fig.write_html('/home/mlf-project/results.html')
        mlflow.log_artifact('/home/mlf-project/results.html')
        os.remove('/home/mlf-project/results.html')


if __name__ == "__main__":
    main()
        
