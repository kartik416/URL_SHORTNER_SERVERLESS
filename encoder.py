from hashlib import md5
import string
import boto3
from datetime import datetime, timedelta
import requests

class URL_Shortner:
    time_format = '%d/%m/%Y %H:%M:%S'

    def encode(self, url:str) -> str:
        str_to_int = int(md5(url.encode('utf-8')).hexdigest(), 16)
        s = string.ascii_letters + string.digits
        hash_str = ''
        while str_to_int > 0:
            hash_str = s[str_to_int % 62] + hash_str
            str_to_int = str_to_int // 62
        return hash_str
    
    def create_record(self, url:str) -> dict:
        uuid = self.encode(url)
        if uuid:
            created_on = datetime.utcnow()
            expires_on = created_on + timedelta(days=365*2)
            record = {
                'Id': {'S': uuid},
                'Orignal_URL': {'S': url},
                'Created_on': {'S': created_on.strftime(self.time_format)},
                'Expires_on': {'S': expires_on.strftime(self.time_format)},
                'Hits': {'N': '0'}
            }
            return record
        return

    def check_url(self, url:str) -> bool:
        try:
            response = requests.get(url, timeout=10)
            return response.ok
        except:
            return False
    
    def store_record(self, url: str) -> None:
        if url:
            is_url_valid = self.check_url(url)
            if is_url_valid:
                dynamo_client = boto3.client('dynamodb')
                record = self.create_record(url)
                if record:
                    response = dynamo_client.put_item(Item = record, TableName='URL_SHORTNER')
                    print(response)

shortner = URL_Shortner()
print(shortner.check_url('https://www.delftstack.com/howto/python/python-ping/'))