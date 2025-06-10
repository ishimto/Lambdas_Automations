import os
import boto3
import base64
import json
import gitlab

def get_secrets(secret_name="lambda/creds", region_name="eu-central-1"):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    secrets = get_secrets()
    gitlab_token = secrets["GITLAB_ADMIN_TOKEN"]
    gitlab_url = os.getenv("GITLAB_URL", "http://3.77.55.171:80")    
    
    file_name = event.get("file_name")
    bucket_name = event.get("bucket_name")
    gitlab_user = event.get("gitlab_user")
    gitlab_repo = event.get("gitlab_repo")
    gitlab_branch = event.get("gitlab_branch")
    
    if not all([gitlab_token, gitlab_url]):
        return {
            "statusCode": 500,
            "body": "Missing required environment variables"
        }
    try:
        gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)
        project_path = f"{gitlab_user}/{gitlab_repo}"
        project = gl.projects.get(project_path)

        file = project.files.get(file_path=file_name, ref=gitlab_branch)
        content_base64 = file.content
        object_data = base64.b64decode(content_base64)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Git backup to s3 lambda failed {str(e)}"
        }
    
    try:
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=object_data)
        return {
            'statusCode': 200,
            'body': f"Successfully uploaded object to S3 bucket: {bucket_name}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error uploading object to S3: {str(e)}"
        }
