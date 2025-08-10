import json
import os 
import boto3

SENDER_EMAIL = os.environ.get('SENDER_EMAIL',"sajabilal69@gmail.com").strip()
QUEUE_URL = os.environ.get('QUEUE_URL', "https://sqs.us-east-1.amazonaws.com/476959162071/queue-to-db2").strip()
ses = boto3.client('ses', region_name='us-east-1')
sqs = boto3.client('sqs', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        print(event)
        data = event.get("queryStringParameters", {})#queryStringParameters is a dectionary which api adds input to
        customer_email = data.get("email")
        hotel_name = data.get("hotel")
        room_type= data.get("roomtype")
        arrival_date = data.get("arrivaldate")
        leaving_date = data.get("leavingDate")
        ID = data.get("id")
        print("customer_email",customer_email)
        print("hotelName",hotel_name)
        print("roomType", room_type)
        print("arrivalDate", arrival_date)
        print("leavingDate", leaving_date)
        ses.send_email(
            Source=SENDER_EMAIL,
            Destination={
                'ToAddresses': [
                    customer_email,
                ]
            },
            Message={
                'Subject': {
                    'Data': 'Request Accepted',
                },
                'Body': {
                    'Text': {
                        'Data': 'your request to ' + hotel_name + 'has been accepted ',
                    }
                }
            }
        )

        if (ID is None):
            print ("id is none")
            record = {
            "customer_email": customer_email,
            "hotel_name": hotel_name,
            "room_type": room_type,
            "arrival_date": arrival_date,
            "leaving_date": leaving_date,
            "process": "add to database"
            }
            print("process is :"+ record.get("process"))
        else: 
            print("id is : "+ID)
            record = {
                "doc": {
                    "id": ID,
                    "customer_email": customer_email,
                    "room_type": room_type,
                    "arrival_date": arrival_date,
                    "leaving_date": leaving_date,
                    "process": "edit to database"
                    }
                }
            print("process is :")
            print (record["doc"].get("process"))

        sqs_response =  sqs.send_message(QueueUrl=QUEUE_URL,MessageBody=(json.dumps(record)))
        print("sqs_response", sqs_response)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Accept email sent to customer!')
            
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('the error is :' +str(e))
        }
