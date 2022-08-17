# Docker images
This section contains Dockerfiles and required dependencies for building the images used in this project. There are 4 different containers:
- **mlflow-project-environment-full** provides the container in which our sample mlflow project will run in. It incorporates Docker "good practices" like running as a non-root user, which provides several benefits when running experimetns.
- **mlflow-project-environment-minimal** provides a much simpler version of the mlflow project environment. It is easier to follow and understand than the full mlflow project. The trade-off is it runs as root, and elevated permissions are required to view the files saved to bind-mounts on the host, like the log files. 
- **sftp-server** is a simple, minimal ssh server configured for sftp connections. It is used to store artifacts (saved models, figures, etc) during experiments.
- **mlflow-server** runs an instance of an mlflow server that can connect to a tracking db (like our postgres container, or a remote db server), and an artifact storage server (like our sftp-server, or a cloud storage bucket)

Note that the mlflow and sftp server images can be built when running docker compose, so the only image that needs to be built manually is the experiment environment. To build the image, simply enter the **mlflow-project-environment-{minimal,full}/** folder and run the **build-image.sh** script.
