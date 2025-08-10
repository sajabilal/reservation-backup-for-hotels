import json
import boto3
import os
import requests
from requests_aws4auth import AWS4Auth

service = 'es'
region = 'us-east-1'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token = credentials.token)
url = os.environ['opensearch'].strip()+os.environ['index'].strip()+"/_doc/"

def lambda_handler(event, context):
    # TODO implement
    idd = json.loads(event['body'])['id']
    print("id is:" + idd)
    final_url = url+idd
    print("final url is:" + final_url)
    #access primary opensearch and search the id 
    try:
        print("in the try")
        response = requests.get(final_url, auth = awsauth , headers={"Content-Type": "application/json"}, timeout=10 )
        print ("after search response")
        print("response is:" +response.text)
        # return {
        #     'statusCode': 200,
        #     'body': json.dumps(search_response.text)
        # }
        search_response = response.json()
        return {
            'statusCode': 200,
            'body': json.dumps(search_response)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error occurred while searching for the document')
        }

   
