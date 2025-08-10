import json
import os
import boto3

# Initialize SES client
ses = boto3.client("ses", region_name="us-east-1") 

# Must be a verified email in AWS SES
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "sajabilal69@gmail.com").strip()

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
        
        if not recipient_emails:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Recipient email(s) missing"})
            }

        # Send email via AWS SES
        response = ses.send_email(
            Destination={"ToAddresses": recipient_emails},
            Message={
                "Body": {"Text": {"Data": message}},
                "Subject": {"Data": subject}
            },
            Source=SENDER_EMAIL
        )
        print("message is:" + str(Message))

        return {
            "statusCode": 200,
            "body": json.dumps({"success": "Email sent successfully!"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
