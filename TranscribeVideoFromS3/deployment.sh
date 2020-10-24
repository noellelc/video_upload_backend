$destinationPath = ".\lambdaFunc.zip"
$lambdaFunctionName = "TranscribeVideoFromS3"

Compress-Archive -Path ".\*" -DestinationPath $destinationPath -F

aws lambda update-function-code --function-name $lambdaFunctionName --zip-file fileb://$destinationPath --region us-west-2
