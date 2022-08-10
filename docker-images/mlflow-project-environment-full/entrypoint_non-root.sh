# Commands run as non-root user

# update environment variables not set by su-exec
USER=mlf-project
source /etc/profile

# run commands from command line input
$@
