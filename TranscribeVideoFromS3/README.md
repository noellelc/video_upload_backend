## GetPresignedPostData
The purpose of this lambda function is to [initiate a transcription process](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe.html#TranscribeService.Client.start_transcription_job) on an uploaded video using the AWS Transcription Service. It assumes the uploaded video is in English and is triggered by an upload to the `videos/` folder in the S3 bucket.

### Setup
The role assigned to this lambda function needs to have a policy associated which allows:
- `s3:GetObject`
- `transcribe:StartTranscriptionJob`

### Deployment
Currently, there is no CI in place, so code can either be manually edited in the AWS Console Lambda Function UI or deployed via the AWS CLI and tested using the AWS API Gateway set up to run the lambda function.

To deploy using the AWS CLI (available [here](https://aws.amazon.com/cli/)), use the `deployment.sh` script in this folder.

### Testing
This lambda function is configured to be triggered whenever a new file is uploaded to the S3 bucket `videos/` folder. This is an async process and is best monitored viewing the logs in in CloudWatch after uploading a file to the appropriate folder.