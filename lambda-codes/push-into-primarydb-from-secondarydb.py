import json
import boto3
import boto3
from requests_aws4auth import AWS4Auth
import requests
import os 

region = 'us-east-1'
service = 'es'
s3 = boto3.client("s3")
credentials = boto3.Session().get_credentials() 
AwsAuth= AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
url = url = os.environ['domain']+os.environ['index']+'_search/'

def lambda_handler(event, context):
    # TODO implement
    try:
        query = {
    "query": {
        "match_all": {}
    },
    "size": 100  # Fetch up to 100 records
}

        response_db= requests.get(url, auth=AwsAuth, json=query, headers={"Content-Type": "application/json"})
        print(response_db.text)
        response_db = json.loads(response_db.text)
        response_s3 = s3.put_object(Bucket="secondary-rescue", Key="backups/data.json", Body=json.dumps(response_db))
        print(response_s3)
    except Exception as e:
        print(e)
        print("Error loading data from the secondary opensearch index into s3 rescue")



    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
