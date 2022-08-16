#! ./env/bin/python

from dotenv import load_dotenv
import mlflow
import os

# read mlflow port and logging level from .env
# env file is read from parent directory to ensure that
# mlflow server port doesn't have to be specified twice
load_dotenv('../.env')

# docker mounts need to be absolute paths
# to make the defaults work, we expand them to absolute paths in python
os.environ['INPUT_PARAMS'] = os.path.abspath('../'+os.environ['INPUT_PARAMS'])
os.environ['CACHE_DIR'] = os.path.abspath('../'+os.environ['CACHE_DIR'])

mlport = os.environ['MLFLOW_SERVER_PORT']

mlflow.set_tracking_uri('http://localhost:{}'.format(mlport))


for degree in range(1,4):

    project_uri='git@github.com:rccohn/mlflow-server-docker.git'\
                '#example-mlflow-projects/sample-project-full'
    mlflow.projects.run(project_uri, parameters={'degree': degree}, docker_args={'net':'host'},)
