import json
import csv
import io
import os
import base64
from openpyxl import Workbook
import gitlab
import boto3

def get_gitlab_secrets(secret_name="lambda/creds", region_name="eu-central-1"):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

def lambda_handler(event, context):
    csv_data = event.get("csv_data")
    output_file_name = event.get("output_file_name", "output.xlsx")
    commit_message = event.get("commit_message", "upload xlsx file")

    if not csv_data:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing csv_data"})
        }
    secrets = get_gitlab_secrets()

    gitlab_token = secrets["CSV_LAMBDA_GITLAB_TOKEN"]
    gitlab_user = secrets["GITLAB_XLSX_USER"]
    gitlab_repo = secrets["GITLAB_XLSX_REPO"]
    gitlab_branch = ("main")
    file_path = output_file_name

    if not all([gitlab_token, gitlab_user, gitlab_repo]):
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Missing required environment variables"})
        }

    project_path = f"{gitlab_user}/{gitlab_repo}"

    csv_file = io.StringIO(csv_data)
    reader = csv.reader(csv_file, delimiter=';')

    wb = Workbook()
    ws = wb.active
    for row in reader:
        ws.append(row)

    output_excel = io.BytesIO()
    wb.save(output_excel)
    output_excel.seek(0)
    encoded_content = base64.b64encode(output_excel.read()).decode('utf-8')

    gl = gitlab.Gitlab('http://3.66.230.140:8000', private_token=gitlab_token)
    project = gl.projects.get(project_path)

    action = "update"

    try:
        f = project.files.get(file_path=file_path, ref=gitlab_branch)
        f.content = encoded_content
        f.encoding = 'base64'
        f.save(branch=gitlab_branch, commit_message=commit_message)
    except gitlab.exceptions.GitlabGetError:
        action = "create"
        project.files.create({
            'file_path': file_path,
            'branch': gitlab_branch,
            'content': encoded_content,
            'encoding': 'base64',
            'commit_message': commit_message
        })

    return {
        "statusCode": 200,
        "body": f"{output_file_name} {action} successfully"
    }

