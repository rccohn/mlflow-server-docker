#! /bin/bash

# add keys passed from environment variables to container
# and make sure their permissions are appropriate for ssh
cd .ssh && echo "${MLF_PUBLIC_KEY}" > id_rsa.pub && \
   echo "${MLF_PRIVATE_KEY}" > id_rsa && \
   chmod 600 id_rsa && chmod 644 id_rsa.pub


# more than enough time for artifact container to generate keys
# before we try connecting to it
sleep 5 # and start server

# establish connection to artifact-store to add server keys to
# ~/.ssh/known_hosts file, preventing mlflow sftp errors
ssh -o "BatchMode yes" artifact-store pwd

# run the mlflow server with arguments from the command line
mlflow server "$@"
