# Bind mounts
To persist data on the host machine, even after the containers are stopped or even deleted, the relevant data directories are mounted to the host. **artifacts/** stores all mlflow experiment artifacts, and **postgres/** stores the tracking database entries. You can choose to store the data elsewhere by changing the mount locations in **docker-compose.yaml**. Note that in order for the container to read or write to a bind mount, it will need sufficient permissions. Unless you have a reason not to, the easiest way to ensure this can happen is by assigning 777 permissions (anyone can read, write, and execute files) to files and directories that are mounted:
```bash
$ chmod 777 path
```
