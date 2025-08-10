import json
import boto3
import os
import requests
from requests_aws4auth import AWS4Auth


region = 'us-east-1'
service = 'es' #using sigV4 #this type of authentication "AWS4AUTH" uses es as a name ofor opensearch service
credentials = boto3.Session().get_credentials() 
base_url= os.environ['opensearch']+os.environ['index']+"/_doc/"
print("url is :" + base_url)
awsauth = AWS4Auth(credentials.access_key,
                   credentials.secret_key,
                   region,
                   service,
                   session_token=credentials.token) #auth into the opensearch 


def lambda_handler(event, context):
    id = json.loads(event['body'])
    print("id is:" + id)
    url = f"{base_url}{id}"
#     search_query = {
#   "query": {
#     "match": {
#       "id": id
#     }
#   }
# }

    try:
        response = requests.get(url, auth = awsauth, headers={"Content-Type": "application/json"})
    
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error occurred while searching for the document')
        }
    
    record = response.json().get("_source", {})
    record["id"] = id
    print(json.dumps(record))
    return {
        'statusCode': 200,
        # 'headers': {
        #     'Access-Control-Allow-Origin': '*',
        #     'Content-Type': 'application/json'
        # },
        'body': json.dumps(record)
    }
