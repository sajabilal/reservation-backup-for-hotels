import json
import boto3
import os



s3 = boto3.client("s3")


def lambda_handler(event, context):
    try:
        response_get=s3.get_object(Bucket='secondary-rescue', Key='backups/data.json')#python dic which has [Body]key which needs to be read
        response_get_s3 = response_get['Body'].read().decode('utf-8')#reading the records in "body", now it is a string
        response_get_s3= json.loads(response_get_s3)#converting string to python dic
        print("response_get is:")
        print(response_get_s3)
        
        response_put_s3 = s3.put_object(Bucket='primary-open-search-backup', Key='backups/recovery-data.json', Body=json.dumps(response_get_s3))
        print("response_put is:")
        print(response_put_s3)

    except Exception as e :
        print(e)

    return {
        'statusCode': 200,
        'body': json.dumps('all saved from s3 secondary into s3 primary ')
    }
