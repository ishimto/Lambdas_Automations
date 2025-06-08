import json
import os
from twilio.rest import Client



def get_secrets(secret_name="lambda/creds", region_name="eu-central-1"):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

def lambda_handler(event, context):
    secrets = get_secrets()
    account_sid = secrets["TWILIO_ACCOUNT_SID"]
    auth_token = secrets["TWILIO_AUTH_TOKEN"]
    from_whatsapp = secrets["TWILIO_WHATSAPP_FROM"]
    client = Client(account_sid, auth_token)



    try:
        data = event.get("data")
        numbers = event.get("numbers", [])

        if not data or not numbers:
            return {
                "statusCode": 400,
                "body": json.dumps("Missing 'data' or 'numbers'")
            }

        for number in numbers:
            if number == None:
                continue
            client.messages.create(
                body=data,
                from_=f"whatsapp:{from_whatsapp}",
                to=f"whatsapp:{number}"
            )

        return {
            "statusCode": 200,
            "body": json.dumps("Messages sent successfully")
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }


