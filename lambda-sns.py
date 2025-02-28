import json
import os 
import boto3

sns = boto3.client('sns', region_name='us-east-1')
sns_arn = os.environ.get('SNS_TOPIC_ARN',"arn:aws:sns:us-east-1:476959162071:HotelEmailSending")
print("SNS Topic ARN being used:", sns_arn)

def lambda_handler(event, context):
    #get data from event dictionary 
    path = event.get("rawPath")
    #set the options for messages
    messages_options = {
        "decline" : "the hotel rejected your request",
        "accept" : "the hotel accepted your request"
    }
    #sent sns 
    if path == "/decline":
        response = sns.publish(
            TopicArn = sns_arn,
            Subject = "decline",
            Message = messages_options["decline"]
        )
        return {"statusCode": 200}
    elif path == "/accept":
        response = sns.publish(
            TopicArn = sns_arn,
            Subject = "accept",
            Message = messages_options["accept"]
        )
        return {"statusCode": 200}
    else:
        response = sns.publish(
            TopicArn = sns_arn,
            Subject = "error",
            Message = "error"
            )
        return {"statusCode": 400}
    
# Simulate AWS Lambda test event
if __name__ == "__main__":
    test_event = {
        "rawPath": "/accept"  # Change to "/accept" for the accept case
    }
    
    test_response = lambda_handler(test_event, None)
    print("Lambda Response:", json.dumps(test_response, indent=2))

