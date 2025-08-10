import json
import boto3
import os

ses = boto3.client('ses', region_name='us-east-1')

# Must be a verified email in AWS SES
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "sajabilal69@gmail.com").strip()

def lambda_handler(event, context):
    print("✅ Lambda function started!")
    try:

        data = event.get("queryStringParameters", {})#queryStringParameters is a dectionary which api adds input to
        customer_email = data.get("email")
        print("customer_email",customer_email)
        hotel_name = data.get("hotel")
        print("hotelName",hotel_name)

        if not customer_email:
            print("hotelName in if")
            return {
                'statusCode': 400,
                'body': json.dumps('no email added')
            }
        elif not hotel_name:
            print("hotelName in elif")
            return {
                'statusCode': 400,
                'body': json.dumps('no hotel name added')
            }
        else:
            # print("customer_email*2")
            # if isinstance (customer_email, str):
            #     print("issue not with type")
            # email = urllib.parse.unquote(customer_email.strip())
            # print("customer_email*2",email)
            response = ses.send_email(
                Source=SENDER_EMAIL,
                Destination={
                    'ToAddresses': [
                        customer_email,
                    ]
                },
                Message={#NEEDS TO BE A DICTIONRY
                    'Subject': {'Data':'your request is rejected'
                    },
                    'Body': {
                        'Text': {
                            'Data': f"your reservation request to {hotel_name} has been rejected" 
                        }
                    }
                }
            )
            print("response=", response)
            return {#http response to API needs to be a dictionary
                'statusCode': 200,
                'body': json.dumps('email sent to customer successfully')
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

        

