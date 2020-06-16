set %1
set %2
set %3
set %4
set %5

gcloud config set project %GCP_PROJECT% && ^
gcloud beta functions deploy webHook --entry-point handle --region=europe-west1 --runtime python37 --trigger-http --memory=128MB ^
--set-env-vars=TELEGRAM_TOKEN=%TELEGRAM_TOKEN%,AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID%,AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY%,AWS_DEFAULT_REGION=%AWS_DEFAULT_REGION%