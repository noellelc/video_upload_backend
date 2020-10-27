const AWS = require('aws-sdk');
const fs = require('fs');

exports.handler = async (event) => {
    let rawConfig = fs.readFileSync('config.json');
    let jsonConfig = JSON.parse(rawConfig);

    const s3 = new AWS.S3({
        accessKeyId: jsonConfig.accessKeyId,
        secretAccessKey: jsonConfig.secretAccessKey
    });

    const params = {
        Bucket: "devdiv-hackweek-translated",
        Key: event.fileName
    };
    
    let signedURL = s3.getSignedUrl('getObject', params);

    const responseBody = {
        signedURL: signedURL,
        fileName: event.fileName,
    };
    
    const response = {
        statusCode: 200,
        body: JSON.stringify(responseBody),
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        }
    }

    return response;
};
