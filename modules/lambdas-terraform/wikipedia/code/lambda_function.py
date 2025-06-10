import json
import wikipedia
import requests
import base64
import boto3
import gitlab
import os

def get_secrets(secret_name="lambda/creds", region_name="eu-central-1"):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

def lambda_handler(event, context):
    title = event.get("title")
    if not title:
        return {"statusCode": 400, "body": "Missing title"}

    try:
        summary = wikipedia.summary(title)
        new_entry = f"\n\n## {title}\n{summary}"
    except wikipedia.exceptions.PageError:
        return {"statusCode": 404, "body": "Page '{title}' not found"}
    except Exception as e:
        return {"statusCode": 500, "body":  str(e) }

    secrets = get_secrets()
    gitlab_token = secrets["GITLAB_ADMIN_TOKEN"]
    gitlab_user = os.getenv("GITLAB_USER", "main-group")
    gitlab_repo = os.getenv("GITLAB_REPO", "wikipedia")
    gitlab_branch = os.getenv("GITLAB_BRANCH", "main")
    file_path = os.getenv("GITLAB_FILE_PATH", "wiki_summaries.txt")
    gitlab_url = os.getenv("GITLAB_URL", "http://3.77.55.171:80")

    if not all([gitlab_token, gitlab_user, gitlab_repo]):
        return {
            "statusCode": 500,
            "body": "Missing required environment variables"
        }

    try:
        gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)
        project_path = f"{gitlab_user}/{gitlab_repo}"
        project = gl.projects.get(project_path)

        action = "updated"

        try:
            file = project.files.get(file_path=file_path, ref=gitlab_branch)
            current_content = base64.b64decode(file.content).decode()
            updated_content = current_content + new_entry
            file.content = updated_content
            file.encoding = "text"
            file.save(branch=gitlab_branch, commit_message=f"Update wiki summary for {title}")
        except gitlab.exceptions.GitlabGetError:
            action = "created"
            project.files.create({
                'file_path': file_path,
                'branch': gitlab_branch,
                'content': new_entry.strip(),
                'encoding': 'text',
                'commit_message': f"Create wiki summary for {title}"
            })

        return {
            "statusCode": 200,
            "body": f"Summary {action} successfully"
        }

    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
