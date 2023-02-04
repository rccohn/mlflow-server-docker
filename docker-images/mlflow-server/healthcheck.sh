#! /bin/bash

set -eou pipefail

healthcheck_ssh(){
    # verify connection to artifact store
	ssh -o "BatchMode yes" artifact-store pwd > /dev/null

}

healthcheck_mlflow(){
    # verify connection to server/tracking db
python - <<-EOF
import mlflow
mlflow.MlflowClient('http://localhost:5000') \
.search_experiments(max_results=5)
EOF
}

healthcheck(){
	# run all healthchecks
	echo running healthcheck
	healthcheck_ssh && \
	healthcheck_mlflow
	echo status $?
}


# if any healtheck fails, return exit code 1
healthcheck || exit 1
