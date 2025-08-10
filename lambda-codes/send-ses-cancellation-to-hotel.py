import json
import os
import boto3
import requests
from requests_aws4auth import AWS4Auth

QUEUE_URL = os.environ.get('QUEUE_URL', "https://sqs.us-east-1.amazonaws.com/476959162071/queue-to-db2").strip()
sqs = boto3.client('sqs', region_name='us-east-1')
ses = boto3.client('ses' , region_name='us-east-1')
#Must be a verified email in AWS SES
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "sajabilal69@gmail.com").strip()
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()

awsauth = AWS4Auth(credentials.access_key,
                   credentials.secret_key,
                   region,
                   service,
                   session_token=credentials.token)

def lambda_handler(event, context):
    
    try:
        # Parse request body
        body = json.loads(event["body"])
        recipient_emails = body.get("toEmails", [])
        subject = body.get("subject", "No Subject")
        message = body.get("message", "No Message")
        print(f"Recipient Emails: {recipient_emails}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        

        # Send email via AWS SES
        response = ses.send_email(
            Destination={"ToAddresses": recipient_emails},
            Message={
                "Body": {"Text": {"Data": message}},
                "Subject": {"Data": subject}
            },
            Source=SENDER_EMAIL
        )

        id = body.get("id", {})
        record = {
            "reservationId" : id,
            "process" : "delete"
        }
        print(record)
        # send to sqs
        sqs.send_message(QueueUrl=QUEUE_URL,MessageBody=(json.dumps(record)))

        #delete from opensearch
        # data = event.get("queryStringParameters", {})
        # reservationId = data.get("reservationID")
        # base_url = os.environ['opensearch'] + os.environ['index']
        # url = f"{base_url}/_doc/{reservationID}"
        # response_opensearch = requests.delete(url, auth=awsauth)

        return {
            'statusCode': 200,
            'body': json.dumps('cancelation email sent to hotel successfully')
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
