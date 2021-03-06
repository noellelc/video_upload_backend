const { scanTable } = require('./dynamo');

exports.handler =

  async (event) => {
    let responseCode = 200;
    console.log("request: " + JSON.stringify(event));
  
    const tableName = event.queryStringParameters.tableName;
  
    let result;
    try {
       result = await scanTable(tableName);
    } catch (err) {
      responseCode = 500;
      console.log('Error scanning table!');
    }

    console.log('Result', JSON.stringify(result));

    const responseBody = {
      result,
    };
    
    const response = {
      statusCode: responseCode,
      body: JSON.stringify(responseBody),
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*'
      }
    };
    console.log("response: " + JSON.stringify(response))
    return response;
  };



