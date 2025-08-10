import json
import os 
import boto3

ses = boto3.client('ses', region_name='us-east-1')
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "sajabilal69@gmail.com").strip()

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        recipient_emails = body.get("toEmails", [])
        subject = body.get("subject", "No Subject")
        message = body.get("message", "No Message")
        print(f"Recipient Emails: {recipient_emails}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")

        ses.send_email(Destination={
            'ToAddresses': 
                recipient_emails,
        },Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Text': {
                    'Data': message,
                }
            }
        },Source = SENDER_EMAIL,)

        return {
            'statusCode': 200,
            'body': json.dumps('edit request sent to hotel!')
        }
    except Exception as e:
        print("edit request not sent", e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
