#! ./env/bin/python

from dotenv import load_dotenv
import mlflow
import os

# read mlflow port and logging level from .env
# env file is read from parent directory to ensure that
# mlflow server port doesn't have to be specified twice
load_dotenv("../.env")

# docker mounts need to be absolute paths
# to make the defaults work, we expand them to absolute paths in python
os.environ["INPUT_PARAMS"] = os.path.abspath(
    "../" + os.environ["INPUT_PARAMS"]
)
os.environ["CACHE_DIR"] = os.path.abspath("../" + os.environ["CACHE_DIR"])

# set port to track to same port that mlflow server runs on
mlport = os.environ["MLFLOW_SERVER_PORT"]
mlflow.set_tracking_uri("http://localhost:{}".format(mlport))

# Automatically run a parameter sweep- train models for
# 1st, 2nd, and 3rd degree polynomials
for degree in range(1, 4):

    # projects can be run from remote uris such as github as well as
    # local files (like in run_minimal.py). When this is done, the remote
    # uri is stored in the tracking db, and it links to the correct version of
    # code when viewed with the mlflow UI. In other words, you can always see
    # the exact version of code used, even if it is later changed.
    project_uri = (
        "git@github.com:rccohn/mlflow-server-docker.git"
        "#example-mlflow-projects/sample-project-full"
    )

    # run the project with the desired degree parameter. To reach the tracking
    # server from localhost, we use the host networking mode with docker.
    mlflow.projects.run(
        project_uri, parameters={"degree": degree}, docker_args={"net": "host"}
    )
