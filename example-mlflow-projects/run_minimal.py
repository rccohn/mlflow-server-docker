#! ./env/bin/python
from dotenv import dotenv_values
import mlflow

# read port that mlflow server is running on and configure tracking uri
mlport = dotenv_values('../.env')['MLFLOW_SERVER_PORT']
mlflow.set_tracking_uri('http://localhost:{}'.format(mlport))

# in order to run on localhost without having to look up ip of mlflow server container,
# we run the project with docker host networking mode. No other parameters need to be specified. 
mlflow.projects.run('sample-project-minimal', docker_args={'net':'host'},)
