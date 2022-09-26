# use python base image. slim-buster excludes a lot of
# extra files from the full debian or ubuntu images
# that we don't need
FROM python:3.10.6-slim-buster

# add non-root user for added security and use it to run the container
RUN adduser --disabled-password mlf-server
USER mlf-server

# create python environment, activate it by default, 
# and install dependencies
ENV VENV="/home/mlf-server/venv"
RUN python -m venv ${VENV}
ENV PATH="${VENV}/bin:${PATH}"
RUN pip install --upgrade pip && pip install \
	psycopg2-binary==2.9.3 mlflow==1.28.0 google-cloud-storage==2.5.0

WORKDIR /home/mlf-server/
# to use sftp, mlflow requires ssh to be configured to
# connect to host without specifying any extra options,
# so we use the ~/.ssh/config to store all relevant configurations

# mlflow server runs on port 5000
EXPOSE 5000

# entrypoint waits before starting server
COPY --chown=mlf-server entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
