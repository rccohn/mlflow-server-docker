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
ARG VENV="/usr/local/share/env"
RUN python -m venv ${VENV} && \
    # automatically activate python environment by default
    echo "PATH=${VENV}/bin:${PATH}" >> /etc/profile && \
    ${VENV}/bin/python -m pip install -r requirements.txt && \
    rm requirements.txt


WORKDIR /home
COPY entrypoint_root.sh entrypoint_root.sh
COPY entrypoint_non-root.sh entrypoint_non-root.sh

ENTRYPOINT ["bash", "/home/entrypoint_root.sh"]
