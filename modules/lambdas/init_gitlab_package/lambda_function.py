import os
import json
import gitlab

def get_secrets(secret_name="lambda/creds", region_name="eu-central-1"):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


def lambda_handler(event, context):
    users = event.get("users", [])
    GITLAB_URL = os.getenv('GITLAB_URL')
    secrets = get_secrets()
    gitlab_token = secrets["GITLAB_ADMIN_TOKEN"]
    GROUP_NAME = "main-group"
    
    gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)


    if not users:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No users provided"})
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


