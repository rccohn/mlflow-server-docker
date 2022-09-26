#! /bin/bash
echo "waiting for backend db connection"
sleep 5 # should be enough time
mlflow server $@ # start the server
