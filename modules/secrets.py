import boto3
import json

def get_secrets(secret_name="server/secrets/google/sheetid", region_name="eu-central-1"):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

secrets = get_secrets()
SHEET_ID = secrets["SHEET_ID"]

