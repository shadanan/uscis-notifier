# Send Pushover Notification when USCIS Receipt Date is Updated

This repo contains a cloud function that sends pushover notifications when USCIS
updates the receipt date on their
[website](https://egov.uscis.gov/processing-times/).

## Pseudocode

```
- retrieve the receipt date for a case inquiry from USCIS processing times web site
- read the previous receipt date from disk
- compare the previous receipt date with current receipt date
- if they are different, then:
  - send a notification
  - update the previous receipt date with the current receipt date
```

## Deploying

1. Set the project ID.

   ```shell
   export PROJECT_ID=uscis-processing-times-330718
   gcloud config set project $PROJECT_ID
   ```

1. Set the service account.

   ```shell
   export SERVICE_ACCOUNT=uscis-notify-cloud-function-sa
   ```

1. Deploy the cloud function.

   ```shell
   gcloud functions deploy uscis-notify \
     --entry-point=main \
     --runtime=python39 \
     --service-account="$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
     --set-env-vars="PROJECT_ID=$PROJECT_ID" \
     --source=cf \
     --trigger-topic=trigger-uscis-notify-cloud-function
   ```
