#! ./env/bin/python

from dotenv import load_dotenv
import mlflow
import os

# read mlflow port and logging level from .env
load_dotenv()

# docker mounts need to be absolute paths
# to make the defaults work, we expand them to absolute paths in python
os.environ['INPUT_PARAMS'] = os.path.abspath(os.environ['INPUT_PARAMS'])
os.environ['LOG_DIR'] = os.path.abspath(os.environ['LOG_DIR'])
os.system('echo ${INPUT_PARAMS} ${LOG_DIR} test!!!')

print(os.environ['INPUT_PARAMS'], os.environ['LOG_DIR'], sep='\n')
mlport = os.environ['MLFLOW_SERVER_PORT']

mlflow.set_tracking_uri('http://localhost:{}'.format(mlport))

# print insructions (tracking uri, etc)
mlflow.projects.run('example-mlflow-project', docker_args={'net':'host'},)
