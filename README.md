# mlflow-server-docker
Minimal, fully-containerized mlflow server with remote postgres tracking db and sftp artifact store.

# High-throughput, portable, reproducible, and organized experiments


Computational researchers, especially in non-cs disciplines, are often expected to write large volumes of code without being taught good development practices.
  - Needing a figure from a study you ran 3 years ago, but not being able to find it.
  - Code that used to run now seems to give different results or error out
  - Code from a published paper doesn't work when you try to run it.
  - Your collaborators promise that "it works on their machine", but you can't run it on yours.
  - Many other issues




## How it works


## Why docker?


## Why mlflow?


# Installation
## Install docker
The only dependency of the server is Docker. Follow the instructions from docker
to install it on your system. Since docker runs as root, you will likely need to
run docker commands with **sudo** after installation. To run docker without sudo,
you can add your user to the docker group:

```bash
$ sudo usermod -ag docker ${USER}
```
Note that older installations of docker may not include docker compose. If you don't
already have compose, update your installation of docker to a recent version.
  
## Run the server

With docker installed, the server will work out of the box. Simply run
```bash
$ # run without optional -d argument to view container status in terminal
$ docker compose up -d
```
and the server will run.

## Adjust server settings
Variable definitions, including the port that the mlflow server runs on 
and the ssh key used to connect to artifact storage, are are specified in **.env**.
To use new values, simply change the definitions in this file.

The configuration of the containers is specified in **docker-compose.yaml**
To change the images used for each component, commands executed upon startup,
and other settings, you can update this file.

# Start tracking!
With the server running, you are ready to start tracking experiments!

## Tracking with regular python files
Minimal code is needed to start saving results to the mlflow server. The
tracking commands can be inserted into existing code, minimizing the cost of adopting mlflow.
A minimal example shows only 3 lines of code are needed to track a value:
```python3
>>> import mlflow
>>> # tell mlflow where to save results to. assumes the server runs on port 5000
>>> mlflow.set_tracking_uri("http://localhost:5000")
>>> mlflow.log_param("favorite_number", 45) # logs a value to the tracking server
```

## Tracking with mlflow projects
Mlflow also provides a method for packaging code into portable, reproducible collections
called **projects**. Some simple example mlflow projects, including instructions
for running and tracking them, are provided in the **example-mlflow-projects/** directory.

# Accessing the results

## Browser
Open your favorite browser and go to **http://localhost:5000** (assuming the server is on port 5000).
You should see a table of run tracking data. Click on a run to view more details, including 
the saved models, interactive figures, and more.

## Python
You can also access run results programatically in Python.
```python3
>>> import mlflow
>>> mlflow.set_tracking_uri("http://localhost:5000")
>>> # get unique identifier of experiment with name "Default"
>>> exp_id = mlflow.get_experiment_by_name('Default').experiment_id
>>> # get a pandas dataframe of all runs included in the default experiment
>>> df = mlflow.search_runs([exp_id,])
```

