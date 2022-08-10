# use python base image. slim-buster excludes a lot of
# extra files from the full debian or ubuntu images
# that we don't need
FROM python:3.10.6-slim-buster AS main

# create python environment dependencies
COPY requirements.txt requirements.txt

# install virtual environment and dependencies
RUN python -m venv /usr/local/share/env && \
    /usr/local/share/env/bin/python -m pip install -r requirements.txt && \
# requirements file no longer needed after installation
# we also make /home/mlf-project since the python file saves some temp data here
    rm requirements.txt && mkdir /home/mlf-project

# automatically activate python environment by default
ENV PATH="/usr/local/share/env/bin:${PATH}"
