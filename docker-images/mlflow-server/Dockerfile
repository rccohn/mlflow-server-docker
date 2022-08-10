# use python base image. slim-buster excludes a lot of
# extra files from the full debian or ubuntu images
# that we don't need
FROM python:3.10.6-slim-buster

# install ssh so that server can connect to artifact repository
RUN apt-get update && apt-get install -y openssh-client && rm -rf /var/lib/apt/lists/*

# add non-root user for added security and use it to run the container
RUN adduser --disabled-password mlf-server
USER mlf-server

# create python environment, activate it by default, 
# and install dependencies
ENV VENV="/home/mlf-server/venv"
RUN python -m venv ${VENV}
ENV PATH="${VENV}/bin:${PATH}"
RUN pip install --upgrade pip && pip install \
	psycopg2-binary==2.9.3 mlflow==1.27.0 pysftp==0.2.9

WORKDIR /home/mlf-server/
# to use sftp, mlflow requires ssh to be configured to
# connect to host without specifying any extra options,
# so we use the ~/.ssh/config to store all relevant configurations
RUN mkdir .ssh

COPY --chown=mlf-server ssh_config .ssh/config

# ssh is picky about permissions, so make sure they are set right
RUN chmod 700 .ssh && chmod 600 .ssh/config


# mlflow server runs on port 5000
EXPOSE 5000

# script to run on startup
COPY --chown=mlf-server entrypoint.sh entrypoint.sh
ENTRYPOINT ["bash", "entrypoint.sh"]
