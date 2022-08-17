# MLflow projects
Mlflow projects package code for individual experiments. The MLproject YAML file defines the environment that the code runs in (in this case, the docker environment,) and the entrypoints for running code. When a project is run with python (*[mlflow.projects.run](https://www.mlflow.org/docs/latest/python_api/mlflow.projects.html#mlflow.projects.run*)) or the command line interface (*[mlflow run](https://www.mlflow.org/docs/latest/cli.html#mlflow-run)*), mlflow automatically activates the correct project environment and runs the specified entrypoint.  This makes it very convenient for sharing code with others as it makes the process of running experiments unambiguous.

# Example projects included here
This section contains two example mlflow projects for reference. Both projects apply simple linear regression models to small synthetic datasets. While not groundbreaking, these projects can be used for reference and also as templates for full projects.

## Minimal example
As the name suggests, **sample-project-minimal** provides a very simple project with a basic linear regression model. It runs in a very simple docker environment and does not take any external inputs. Despite this, it demonstrates the core functionality of mlflow projects and tracking, running code and sending the results to the tracking database. It saves tags, parameters, performance metrics, the trained model, and a visualization of the performance to the tracking server.

## Full-featured example 
Although still simple, **sample-project-full** demonstrates several additional features compared to the minimal example that may be useful when running projects:

 - Three sets of input parameters are used, allowing parameter tuning to be performed without changing the project code.
   - The degree of the polynomial to be fit is passed as a parameter to the mlflow project itself.
   - Settings for generating the dataset are mounted to the container from an input deck located on the host (**bind-mounts/params.yaml**). This demonstrates how large numbers of parameters can be passed to projects without having to specify many of python or command line arguments. 
   - The user UID to run the code with, and whether to use cached processed data instead of re-generating the dataset from scratch, are passed to the container as environment variables. This is useful for parameters that do not affect the results of the experiment and should not be logged to the tracking server.
 - After generating the dataset with a given set of parameters, the data are saved to a cache in the host machine (**bind-mounts/cache**). After the project finishes and the container is removed, the processed data persists on the host machine. If the dataset has already been generated, the project can load the cached data instead of re-processing it.
 - The docker environment correctly handles permissions for the mounted files, instead of changing their ownership to root, preventing the user from accessing them without elevated permissions.

# Running projects

As mentioned above, projects can be run with python (*[mlflow.projects.run](https://www.mlflow.org/docs/latest/python_api/mlflow.projects.html#mlflow.projects.run*)) or the command line interface (*[mlflow run](https://www.mlflow.org/docs/latest/cli.html#mlflow-run)*). Examples for running both projects with the python interface are provided in **run_full.py** and **run_minimal.py**. 
## Configure .env file

## Configure virtual environment
```bash
$ python -m venv env # create virtual enviroment named env.
$ # install dependencies to virtual environment
$ source env/bin/activate && python -m pip install -r requirements.txt
```
## Run desired project
To run minimal project: 
```bash
$ source env/bin/activate && python run_minimal.py
```
To run full project:
```bash 
$ source env/bin/activate && python run_full.py
```

