# This is an example of a multi-stage build. We need the 'su-exec' tool,
# but don't need git or the compiler tools in our final container. To keep
# the image as small as possible, we download and compile su-exec in one
# container, and copy the resulting binary to the second container.
# More information about su-exec and why we need it is found in entrypoint_root.sh


# use same base image as our main container for consistency
FROM python:3.10.6-slim-buster AS builder

# install compiler and git
RUN apt-get update && apt-get install -y \
    build-essential git && \
    rm -rf /var/lib/apt/lists/* && \
    # download the source for su-exec
    cd /home/ && git clone https://github.com/ncopa/su-exec.git && \
    # build su-exec and move the binary to /usr/local/sbin
    cd su-exec && make su-exec && mv su-exec /usr/local/sbin && \
    # remove the remaining files when we are done
    rm -rf /home/su-exec

# use python base image. slim-buster excludes a lot of
# extra files from the full debian or ubuntu images
# that we don't need
FROM python:3.10.6-slim-buster AS main

# copy the compiled su-exec binary without any extra uneeded dependencies
COPY --from=builder /usr/local/sbin/su-exec /usr/local/sbin/su-exec

# create python environment to run code
COPY requirements.txt requirements.txt

ARG VENV=/usr/local/share/env

RUN python -m venv ${VENV} && \
    ${VENV}/bin/python -m pip install -r requirements.txt && \
    rm requirements.txt

# automatically use our new python environment by default
ENV PATH=${VENV}/bin:${PATH}

WORKDIR /home

# copy entrypoint script, add permissions to execute it, and
# run the script on container start
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/home/entrypoint.sh"]
