import json
import boto3
import os
import requests 
from requests_aws4auth import AWS4Auth

credentials = boto3.Session().get_credentials()
service = 'es'
region = 'us-east-1'
url = os.environ['domain']+os.environ['index']+'_search/'
AwsAuth= AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
s3 = boto3.client('s3')
eventbridge = boto3.client('events')

def lambda_handler(event, context):
    # TODO implement
    try:
        query = {
    "query": {
        "match_all": {}
    },
    "size": 100  # Fetch up to 100 records
        } 
        search_response = requests.get(url, auth=AwsAuth, json=query, headers={'Content-Type': 'application/json'})
        print("search_response is:" +search_response.text)
        if search_response.status_code != 200:
            print("the search failed")
            return {
                'statusCode': 400,
                'body': json.dumps('Search failed')
            }
        # response_test = s3.put_object( Body=b"test", Bucket="primary-open-search-backup", Key='backups/debug-test.txt')
        # print("response_test")
        # print("response_test:", json.dumps(response_test))
        response_saveS3 = s3.put_object(Body=json.dumps(search_response.json()).encode("utf-8"), Bucket="primary-open-search-backup", Key='backups/data.json')
        print("response_saveS3 is :"+ json.dumps(response_saveS3))
        if response_saveS3['ResponseMetadata']['HTTPStatusCode'] != 200:
            print("saving backup failed")
            return {
                'statusCode': 400,
                'body': json.dumps('Saving backup failed')
            }
        
        response = eventbridge.put_events(
        Entries=[
            {
                'Source': 'save-backup-in-s3-primary',
                'DetailType': 'Lambda save-backup-in-s3-primary Function Finished',
                'Detail': json.dumps({
                    'message': 's3 Backup finished',
                    'functionName': 'save-backup-in-s3-primary'
                }),
                'Resources': ['arn:aws:lambda:us-east-1:476959162071:function:save-backup-in-s3-primary'],
            }
        ]
    )

        print("Event sent to EventBridge:", response)
    

    except Exception as e:
        print(e)
    

    return {
        'statusCode': 200,
        'body': json.dumps('backups ready in s3')
    }
