#! /bin/ash
# create password file
htpasswd -bc /etc/nginx/.htpasswd ${MLFLOW_TRACKING_USERNAME} ${MLFLOW_TRACKING_PASSWORD}

# start nginx without daemon
nginx -g "daemon off;"
