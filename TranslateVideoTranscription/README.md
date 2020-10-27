## TranslateVideoTranscription
The purpose of this lambda function is to take the results from the transcription job initiated by TranscribeVideoFromS3 and translate them into Hindi. Once translated, AWS Polly is used to create the Hindi audio, with the speed adjusted sentence by sentence to match the English sentence speed.

### Setup
The role assigned to this lambda function needs to have a policy associated which allows:
- `transcribe:GetTranscriptionJob`
- `s3:PutObject`
- `translate:TranslateText`
- `polly:SynthesizeSpeech`

### Deployment
Currently, there is no CI in place, so code can either be manually edited in the AWS Console Lambda Function UI or deployed via the AWS CLI and tested using the AWS API Gateway set up to run the lambda function.

To deploy using the AWS CLI (available [here](https://aws.amazon.com/cli/)), use the `deployment.sh` script in this folder.

### Testing
This lambda function is configured to be triggered by an EventBridge rule that listens for any Transcribe job state changes to `completed` or `failed`. Once completed, the translated audio file will be written to the specified S3 bucket.

Note: The default timeout for a Lambda function is 3 seconds; this function has been extended to time out after 1 minute.