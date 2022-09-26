# MLflow tracking server on GCP
Since mlflow-server-docker is a modular system, you can easily switch the location of the backend and/or artifact stores.
This example provides a working configuration to store tracking data and artifacts on gcp instead of locally.
For this to work, you will need the following:
  - cloud storage bucket to store artifacts
  - cloud SQL instance to store tracking data (project currently configured with postgres)
  - service account key with IAM permission to access cloud sql (cloud sql client)
  - service account key with IAM permission to access cloud storage (storage object admin)

Update `.env` with your values for the key files, connection name, storage bucket name, etc. Then, to start tracking on the cloud, simply run:

```bash 
docker compose up
``` 

 The server will run on `http://localhost:5000` (unless you change the port in `.env`) To run the server in the cloud, just make sure the firewall allows tcp traffic on port 5000 of the VM used to run the server.