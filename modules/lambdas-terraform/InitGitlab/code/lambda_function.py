import os
import json
import gitlab
import boto3

def get_secrets(secret_name="lambda/creds", region_name="eu-central-1"):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


def lambda_handler(event, context):
    secrets = get_secrets()
    gitlab_token = secrets["GITLAB_ADMIN_TOKEN"]
    gitlab_url = os.getenv("GITLAB_URL", "http://3.77.55.171:80")
    GROUP_NAME = os.getenv("GITLAB_GROUP", "main-group")
    users = event.get("users", [])
    
    gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)


    if not users:
        return {
            "statusCode": 400,
            "body": "No users provided"
        }

    results = []

    for first_name, user_name, password, email in users:
        try:
            user_data = {
                'name': first_name,
                'username': user_name,
                'password': password,
                'email': email,
                'skip_confirmation': True
            }
            new_user = gl.users.create(user_data)

            group = gl.groups.get(GROUP_NAME)
            group.members.create({
                'user_id': new_user.id,
                'access_level': gitlab.const.AccessLevel.REPORTER
            })

            project = gl.projects.create({
                'name': f"{first_name}-project",
                'namespace_id': group.id
            })

            results.append({
                "user": user_name,
                "project_url": project.web_url,
                "status": "success"
            })

        except Exception as e:
            results.append({
                "user": user_name,
                "status": "failed",
                "error": str(e)
            })

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }


