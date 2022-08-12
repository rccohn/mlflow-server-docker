#! /bin/ash

# generate keys for ssh server
ssh-keygen -A

# copy mlflow server public key to authorized_key file
# to register the key as valid and assign the correct permissions
echo "${MLF_PUBLIC_KEY}" > /home/sftp/.ssh/authorized_keys && \
    chmod 600 /home/sftp/.ssh/authorized_keys && \
    chown sftp:sftp /home/sftp/.ssh/authorized_keys   
    
# make sure user can write to mounted volume
chown sftp /home/sftp/artifacts

# start ssh server. "$@" allows for additional options to be passed from the command line
/usr/sbin/sshd -D "$@"

