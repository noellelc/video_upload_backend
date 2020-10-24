$destinationPath = "..\GetPresignedPostData\lambdaFunc.zip"

Compress-Archive -Path "..\GetPresignedPostData\*" -DestinationPath $destinationPath -F

aws lambda update-function-code --function-name GetSignedUrl --zip-file fileb://$destinationPath --region us-west-2
