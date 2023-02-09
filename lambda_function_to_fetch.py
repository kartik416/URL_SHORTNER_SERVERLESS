import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    dynamo_client = boto3.client('dynamodb')
    query = {
        'Id': {
            'S': event.get('Id', '')
        }
    }
    result = dynamo_client.get_item(TableName='URL_SHORTNER', Key=query)
    redirect_url = result.get('Item', {}).get('Orignal_URL', {}).get('S', '')
    if redirect_url:
        return {
            'statusCode': 200,
            'redirect_url': redirect_url
        }
    return {
        'statusCode': 400
    }