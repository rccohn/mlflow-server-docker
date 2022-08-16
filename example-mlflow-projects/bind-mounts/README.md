# Bind mounts
Bind-mounting allows files to be shared between the host machine and container. In the context of mlflow experiments, there are 2 reasons we might want to use bind mounts. First, for experiments with large parameter sets, mounting an input file may be much more convenient than passing many arguments to `mlflow run`. Second, our experiment may generate files that we don't want to save to the tracking server, such as debugging logs, or files that we want to re-use in subsequent experiments, such as pre-processed data. 

In our toy experiment, we mount the input parameters **parameters.json**, and save some logs that we don't want to keep in our mlflow database in **logs/**.
