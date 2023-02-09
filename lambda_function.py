import json
from encoder import URL_Shortner

def lambda_handler(event, context):
    url_shortner = URL_Shortner(event.get("orignal_url", ""))
    response = url_shortner.store_record()
    return {
        'statusCode': response.get('HTTPStatusCode', 400),
        'Id': response.get('Id', '')
    }
