const { getSignedUrl } = require('./getSignedUrl');

exports.handler = async (event) => {
    const uploadedFileName = event.fileName;
    const fileType = event.fileType;
    const bucket = event.bucket;
    const splitFileNameArry = uploadedFileName.split('.');
    const name = splitFileNameArry.shift();
    const fileExtension = splitFileNameArry.pop();
    let folder;
    if (fileType === 'application/pdf') {
        folder = 'pdfs/';
    }
    else if (fileType === 'application/mp4') {
        folder = 'videos/';
    }
    else {
        return {
            statusCode: 400,
            message: 'Invalid file type. Please upload a PDF or a video file.',
        };
    }

    const fileName = folder + name + '_' + Date.now() + '.' + fileExtension;
    
    const signedURL = getSignedUrl(fileName, bucket);

    const responseBody = {
        signedURL: signedURL,
        fileName: fileName,
        fileType: event.fileType,
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
