## GetPresignedPostData
The purpose of this lambda function is to retrieve a URL from AWS, which will be used to directly upload content. This pattern is described [here](https://aws.amazon.com/blogs/compute/uploading-to-amazon-s3-directly-from-a-web-or-mobile-application/).

### Setup
Locally add a `config.json` file with the following keys:
```
{
    "accessKeyId": "******",
    "secretAccessKey": "******"
}
```
These values are created by going to My Security Credentials in the AWS Management Console and selecting _Create access key_.

Eventually, these configurations should be created/retrieved/deployed in a more secure and automated way.

### Deployment
Currently, there is no CI in place, so code can either be manually edited in the AWS Console Lambda Function UI or deployed via the AWS CLI and tested using the AWS API Gateway set up to run the lambda function.

To deploy using the AWS CLI (available [here](https://aws.amazon.com/cli/)), use the `deployment.sh` script in this folder.

### Testing
This lambda function is configured to be triggered via an HTTP request to a REST API endpoint. The current test endpoint can be found by going to the API Gateway in the us-west-2 (Oregon) region. Select `Deploy API` from the Actions dropdown menu and the `DevTest` deployment stage to retrieve the URL.