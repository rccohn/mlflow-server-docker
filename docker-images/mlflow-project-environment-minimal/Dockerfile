# use python base image. slim-buster excludes a lot of
# extra files from the full debian or ubuntu images
# that we don't need, so we use slim-buster
FROM python:3.10.6-slim-buster AS main

# create python environment dependencies
COPY requirements.txt requirements.txt

# install virtual environment and dependencies
RUN python -m venv /mlf-env && \
    /mlf-env/bin/python -m pip install -r requirements.txt && \
    mkdir /home/mlf-project # directory where python file saves some temp data during execution

# automatically activate python environment by default when calling "python"
ENV PATH="/mlf-env/bin:${PATH}"
