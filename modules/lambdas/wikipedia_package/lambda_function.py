import json
import wikipedia
import requests
import base64
import boto3
import urllib.parse
import os

def get_secrets(secret_name="lambda/creds", region_name="eu-central-1"):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


def lambda_handler(event, context):
    title = event.get("title")
    if not title:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing title"})}
    
    secrets = get_secrets()
    gitlab_token = secrets["GITLAB_WIKI_TOKEN"]

    gitlab_user = os.getenv("GITLAB_USER")
    gitlab_repo = os.getenv("GITLAB_REPO")
    gitlab_branch = os.getenv("GITLAB_BRANCH", "main")
    file_path = os.getenv("GITLAB_FILE_PATH", "wiki_summaries.txt")

    try:
        summary = wikipedia.summary(title)
        new_entry = f"\n\n## {title}\n{summary}"

        
        if not all([gitlab_token, gitlab_user, gitlab_repo]):
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Missing required environment variables"})
            }

        project = urllib.parse.quote(f"{gitlab_user}/{gitlab_repo}", safe="")
        encoded_path = urllib.parse.quote(file_path, safe="")
        headers = {"PRIVATE-TOKEN": gitlab_token}

        get_url = f"http://3.66.230.140:8000/api/v4/projects/{project}/repository/files/{encoded_path}?ref={gitlab_branch}"
        r = requests.get(get_url, headers=headers)

        if r.status_code == 200:
            file_data = r.json()
            current_content = base64.b64decode(file_data["content"]).decode()
            updated_content = current_content + new_entry
            action = "update"
        elif r.status_code == 404:
            updated_content = new_entry.strip()
            action = "create"
        else:
            return {"statusCode": r.status_code, "body": r.text}

        put_url = f"http://3.66.230.140:8000/api/v4/projects/{project}/repository/files/{encoded_path}"
        payload = {
            "branch": gitlab_branch,
            "content": updated_content,
            "commit_message": f"{action.capitalize()} wiki summary for {title}"
        }

        put_func = requests.post if action == "create" else requests.put
        res = put_func(put_url, headers=headers, json=payload)

        if res.status_code in [200, 201]:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": f"Summary {action}d successfully",
                    "summary": summary
                })
            }
        else:
            return {
                "statusCode": res.status_code,
                "body": res.text
            }

    except wikipedia.exceptions.PageError:
        return {"statusCode": 404, "body": json.dumps({"error": f"Page '{title}' not found"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

