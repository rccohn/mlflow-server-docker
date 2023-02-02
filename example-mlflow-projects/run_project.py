#! ./env/bin/python

from dotenv import load_dotenv
import mlflow
import os
from sys import argv


def run_minimal_project():
    """Runs the minimal project as a single run and saves the results to the
    mlflow tracking server."""
    # host networking used so both host and container can reach tracking
    # server on localhost.
    mlflow.projects.run(
        "sample-project-minimal",
        docker_args={"net": "host"},
    )


def run_full_project():
    """
    Runs the full project three times with different polynomial degrees
    and saves the results to the tracking server as 3 separate runs.
    """
    # docker mounts need to be absolute paths
    # to make the defaults work, we expand them to absolute paths in python
    os.environ["INPUT_PARAMS"] = os.path.abspath(
        "../" + os.environ["INPUT_PARAMS"]
    )
    os.environ["CACHE_DIR"] = os.path.abspath("../" + os.environ["CACHE_DIR"])

    # projects can be run from remote uris such as github as well as
    # local files (like in run_minimal.py). When this is done, the remote
    # mlflow ui will link to the corresponding commit in the repository
    project_uri = (
        "https://github.com/rccohn/mlflow-server-docker.git"
        "#example-mlflow-projects/sample-project-full"
    )

    # Automatically run a parameter sweep- train models for
    # 1st, 2nd, and 3rd degree polynomials
    for degree in range(1, 4):
        # run the project with the desired degree parameter. To reach the
        # tracking server from localhost, we use the host networking mode
        # with docker.
        mlflow.projects.run(
            project_uri,
            parameters={"degree": degree},
            docker_args={"net": "host"},
        )


def main():
    # validate inputs
    if argv[-1].lower() not in ("minimal", "full"):
        print("usage: python run_project.py <project>")
        print('<project> must be either "minimal" or "full"')
        exit()

    which = argv[-1].lower()  # which project to run

    # read mlflow port and logging level from .env
    # env file is read from parent directory to ensure that
    # mlflow server port doesn't have to be specified twice
    load_dotenv("../.env")

    # set tracking to use the correct port specified in .env file
    mlflow.set_tracking_uri(
        "http://localhost:{}".format(os.environ["MLFLOW_SERVER_PORT"])
    )

    # run the correct project
    if which == "minimal":
        run_minimal_project()
    elif which == "full":
        run_full_project()


if __name__ == "__main__":
    main()
