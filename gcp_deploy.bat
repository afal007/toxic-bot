gcloud config set project %1 && gcloud beta functions deploy handle --region=europe-west1 --runtime python37 --trigger-http --memory=128MB --set-env-vars=TOKEN=%2