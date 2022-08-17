# Bind mounts
Bind-mounting allows files to be shared between the host machine and container. In the context of mlflow experiments, there are 2 reasons we might want to use bind mounts. First, for experiments with large parameter sets, mounting an input file may be much more convenient than passing many arguments to `mlflow run`. Second, our experiment may generate files that we don't want to save to the tracking server, such as debugging logs, or files that we want to re-use in subsequent experiments, such as pre-processed data. 

In **sample-project-full**, we mount   **parameters.json**, providing a convenient way to pass many parameters to the project, and save pre-processed data to **cache/** so that it can be reused on subsequent experiments.
