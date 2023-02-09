from hashlib import md5
import string
import boto3
from datetime import datetime, timedelta
import requests

class URL_Shortner:
    time_format = '%d/%m/%Y %H:%M:%S'

    def __init__(self, long_url) -> None:
        self.long_url = long_url

    def encode(self) -> str:
        str_to_int = int(md5(self.long_url.encode('utf-8')).hexdigest(), 16)
        s = string.ascii_letters + string.digits
        hash_str = ''
        while str_to_int > 0:
            hash_str = s[str_to_int % 62] + hash_str
            str_to_int = str_to_int // 62
        return hash_str
    
    def create_record(self) -> dict:
        uuid = self.encode()
        if uuid:
            created_on = datetime.utcnow()
            expires_on = created_on + timedelta(days=365*2)
            record = {
                'Id': {'S': uuid},
                'Orignal_URL': {'S': self.long_url},
                'Created_on': {'S': created_on.strftime(self.time_format)},
                'Expires_on': {'S': expires_on.strftime(self.time_format)},
                'Hits': {'N': '0'}
            }
            return record
        return {}

    def check_url(self) -> bool:
        try:
            response = requests.get(self.long_url, timeout=5)
            return response.ok
        except:
            return False
    
    def store_record(self) -> None:
        if self.long_url:
            is_url_valid = self.check_url()
            if is_url_valid:
                dynamo_client = boto3.client('dynamodb')
                record = self.create_record()
                if record:
                    response = dynamo_client.put_item(Item = record, TableName='URL_SHORTNER')
                    return {
                        'HTTPStatusCode': response.get('ResponseMetadata', {}).get('HTTPStatusCode'),
                        'Id': record.get('Id')
                    }
        return {
            'HTTPStatusCode': 400
        }