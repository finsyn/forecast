## GCP instructions

### Create dedicated service account
To deploy the GAE application you need a dedicated GCP service account to authenticate against GBQ.

1. create service account
```
gcloud iam service-accounts create forecaster --display-name "market forecaster"
```

2. add service account as member to role
```
gcloud projects add-iam-policy-binding PROJECT_ID --member serviceAccount:forecaster@PROJECT_ID.iam.gserviceaccount.com --role roles/bigquery.dataViewer
```

3. create service account key
```
gcloud iam service-accounts keys create key.json --iam-account forecaster@PROJECT_ID.iam.gserviceaccount.com
```
