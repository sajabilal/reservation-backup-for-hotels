import json
import boto3
import os 
import requests
from requests_aws4auth import AWS4Auth
from datetime import datetime


s3= boto3.client('s3')
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
aws4auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
url= os.environ['domain']+os.environ['index']+'_doc/'
def lambda_handler(event, context):
    try:
        response_get=s3.get_object(Bucket='primary-open-search-backup', Key='backups/data.json')#python dic which has [Body]key which needs to be read
        response_get_s3 = response_get['Body'].read().decode('utf-8')#reading the records in "body", now it is a string
        response_get_s3= json.loads(response_get_s3)#converting string to python dic
        print("response_get is:")
        print(response_get_s3)
        for record in response_get_s3['hits']['hits']:
            print ("record is :")
            print (record)
            id = record['_id']
            final_url = url + id 
            print (type(final_url))
            response_dbstore= requests.put(final_url, auth=aws4auth, json=record['_source'], headers={'Content-Type': 'application/json'})
            print("response_dbstore is :" + response_dbstore.text)

    except Exception as e :
        print(e)

    return {
        'statusCode': 200,
        'body': json.dumps('data pulled from s3 into secondary db')
    }
