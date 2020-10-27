const AWS = require('aws-sdk');
const fs = require('fs');
    
exports.handler = async function(event, context, callback) {
    let rawConfig = fs.readFileSync('config.json');
    let jsonConfig = JSON.parse(rawConfig);
    AWS.config.update({accessKeyId: jsonConfig.accessKeyId, secretAccessKey: jsonConfig.secretAccessKey});
    
    var s3 = new AWS.S3();
    var params = {Bucket: 'devdiv-hackweek-translated', Key: event.fileName};
    console.log(`checking for: ${event.fileName}`);
    try {
        let response = await s3.getObject(params).promise();
        console.log(response);
        return {
            statusCode: 204,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*'
            }
        };
    }
    catch (err) {
        console.log(err, err.stack);
        return {
            statusCode: 404,
            message: 'File is not available',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*'
            }
        };
    }
};