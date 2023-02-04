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

WORKDIR /home/mlf-server/

COPY --chown=mlf-server requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt \
    && rm requirements.txt


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
COPY --chown=mlf-server healthcheck.sh healthcheck.sh

HEALTHCHECK --start-period=10s CMD bash healthcheck.sh

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
