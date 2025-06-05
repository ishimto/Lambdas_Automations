import os
import json
import gitlab

def get_secrets(secret_name="lambda/creds", region_name="eu-central-1"):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


def lambda_handler(event, context):
    repo_name = event.get("repo_name")
    repo_visibility = event.get("repo_visibility")
    GITLAB_URL = os.getenv('GITLAB_URL')

    secrets = get_secrets()
    GITLAB_TOKEN = secrets["GITLAB_ADMIN_TOKEN"]
    
    gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)
    gl.auth()
    project_data = {
            'name': repo_name,
            'visibility': repo_visibility,
            }
    project = gl.projects.create(project_data)


    if not project:
        return {
            'statusCode': 500,
            "body": "Failed to create project"
        }
    return {
        'statusCode': 200,
        "body": "Repo Created"
    }
