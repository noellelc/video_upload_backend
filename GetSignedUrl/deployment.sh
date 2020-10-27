$destinationPath = ".\lambdaFunc.zip"

Compress-Archive -Path ".\*" -DestinationPath $destinationPath -F

aws lambda update-function-code --function-name GetSignedUrl --zip-file fileb://$destinationPath --region us-west-2
