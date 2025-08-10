import json
import boto3 
import os
import requests
from requests_aws4auth import AWS4Auth
import smtplib
from email.mime.text import MIMEText

open_search = os.environ['open_search']#url of opensearch db
index =os.environ['index']#the index in the db (like table in sql db)
region = 'us-east-1'
service = 'es' #using sigV4 #this type of authentication "AWS4AUTH" uses es as a name ofor opensearch service
credentials = boto3.Session().get_credentials() #credentials needed to push into opensearch
awsauth = AWS4Auth(credentials.access_key,
                   credentials.secret_key,
                   region,
                   service,
                   session_token=credentials.token) #auth into the opensearch 
ses = boto3.client('ses' , region_name='us-east-1') #creating a client for SES
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "sajabilal69@gmail.com").strip()

def lambda_handler(event, context): 
    url = open_search + index + '/_doc/' #prepare arguments for post request which is the link into opensearch into the wanted index
    print(event)
    print("Final URL:", url)
    # access the record in sqs , e is json record, lambda is reading from a json record
    for e in event['Records']:
        #access the body of the record (the part which has the data we need for reservation)
        record = e['body']
        #convert the record to python
        py_record = json.loads(record)#turned the json string into a python dic
        print(py_record)
        print (py_record.get("doc"))
        process = py_record.get("process", "")#get the process from the record
        if process == "":
            process = py_record.get("doc").get("process")#get the process from the record
        print("process is:", process)
        #send data to opensearch
        message = ""
        try:
            if process == "add to database":
                py_record.pop("process")#delete the process from the record
                response_add = requests.post(url, auth = awsauth , json = py_record, headers={"Content-Type": "application/json"})#send post request to opensearch 
                print("the pushing into db took place")
                recipient_emails = py_record.get("customer_email", [])
                #recipient_emails = [recipient_emails]
                #response_add = response_add.json()
                #response_add_str =json.dumps(response_add)
                response_add_str = response_add.text
                print(response_add_str)
                id = (response_add.json()).get("_id")
                message = f"Your reservation was received. Reference #: {id}"
                SMTP_USERNAME = os.environ['SMTP_USERNAME']  # from SES
                SMTP_PASSWORD = os.environ['SMTP_PASSWORD']  # from SES
                SMTP_HOST = 'email-smtp.us-east-1.amazonaws.com'
                SMTP_PORT = 587  # required for STARTTLS

                msg = MIMEText(message)
                msg['Subject'] = "your booking reference"
                msg['From'] = recipient_emails #from and to are the same because i am using sandbox and i am using one email for customer and reservationsbackup system
                msg['To'] = recipient_emails

                with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:#This opens a connection to the SES SMTP server.
                    server.starttls()#This upgrades the connection to use TLS encryption Without starttls(), SES will reject your connection attempt.
                    server.login(SMTP_USERNAME, SMTP_PASSWORD)
                    server.sendmail(msg['From'], [msg['To']], msg.as_string())

                print("Email sent via SMTP")

            elif process == "edit to database":
                id = py_record["doc"].get("id", "")
                print("id is :", id)
                url = open_search + index +'/_update/'+ id
                print("edit URL:", url)
                py_record["doc"].pop("process")#delete the process from the record
                py_record["doc"].pop("id")#delete the id from the record
                print(py_record)
                response_edit = requests.post(url, auth = awsauth , json = py_record, headers={"Content-Type": "application/json"})
                print("the editing into db took place")
                recipient_emails = py_record["doc"].get("customer_email", [])
                #recipient_emails = [recipient_emails]
                response_edit = response_edit.json()
                response_edit_str =json.dumps(response_edit)
                print("response edit id:" +response_edit_str)
                print (recipient_emails)
                message = f"Your reservation was updates. Reference #: {id}"
                SMTP_USERNAME = os.environ['SMTP_USERNAME']  # from SES
                SMTP_PASSWORD = os.environ['SMTP_PASSWORD']  # from SES
                SMTP_HOST = 'email-smtp.us-east-1.amazonaws.com'
                SMTP_PORT = 587  # required for STARTTLS

                msg = MIMEText(message)
                msg['Subject'] = "update confirmation"
                msg['From'] = recipient_emails #from and to are the same because i am using sandbox and i am using one email for customer and reservationsbackup system
                msg['To'] = recipient_emails

                with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:#This opens a connection to the SES SMTP server.
                    server.starttls()#This upgrades the connection to use TLS encryption Without starttls(), SES will reject your connection attempt.
                    server.login(SMTP_USERNAME, SMTP_PASSWORD)
                    server.sendmail(msg['From'], [msg['To']], msg.as_string())

                print("Confirmation email sent via SMTP")

            elif process == "delete":
                print ("got to delete section")
                #py_record.pop("process")
                #delete the process from the record
                idd = py_record.get("reservationId", "")#get the id from the record
                print("hello")
                print(idd)
                url_delete = open_search + index +'/_doc/'+ idd #prepare arguments for post request which is the link into opensearch into the wanted index
                print (url_delete)
                # py_record.pop("id")
                response_delete = requests.delete(url_delete, auth = awsauth, headers={"Content-Type": "application/json"})#send post request to opensearch
                print("the deleting from db took place")

        except Exception as ex:
            error_result = {
                'statusCode': 500,
                'body': json.dumps('Error: {} record failed to be sent to db'.format(str(ex)))
            }
            print("record failed to be sent to db return result: " + str(error_result))
            return error_result
        
        
        

        
    result =  {
                    'statusCode': 200,
                    'body': json.dumps('records sent to database')
                }
            
    #print("records sent to database return result: " + str(result)+ "response is: " + str(response.text) )

    return result 


