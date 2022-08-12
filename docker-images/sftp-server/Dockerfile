# alpine is an extremely small image (~5MB) that still has everything we need
FROM alpine:3.16.1

# add ssh so we can generate keys and run the server
RUN apk add --update --no-cache openssh

# create a non-root user for sftp connections
RUN	adduser --disabled-password sftp \
    &&  passwd -d sftp

# copy  configura
WORKDIR /home/sftp
COPY sshd_config /etc/ssh/sshd_config
COPY entrypoint.sh entrypoint.sh

# create ~/.ssh for non-root user "sftp" and 
# configure it with correct ownership/permissions
RUN mkdir .ssh && chmod 700 .ssh && chown sftp .ssh && \
    chmod +x entrypoint.sh

# artifact storage will be mounted so it will persist
# even after container is closed
VOLUME /home/sftp/artifacts

# by default ssh server runs on port 22
EXPOSE 22

# run the entrypoint script on startup
ENTRYPOINT ["/home/sftp/entrypoint.sh"]
