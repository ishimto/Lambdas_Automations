import boto3
import json
import base64
from modules.sheet_auth import sheet
from modules.parse import gitlab_user_data, get_column_by_name



lambda_client = boto3.client('lambda', region_name='eu-central-1')


def create_repo(repo_name, repo_visibility):
    payload = {
        "repo_name": repo_name
    }

    response = lambda_client.invoke(
        FunctionName="CreateGitRepo",
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    
    response_payload = response['Payload'].read().decode('utf-8')
    res = json.loads(response_payload)
    
    return res
    

def backup_git(file_name, bucket_name, gitlab_user, gitlab_repo, gitlab_branch):

    payload = {
        "file_name": file_name,
        "bucket_name": bucket_name,
        "gitlab_user": gitlab_user,
        "gitlab_repo": gitlab_repo,
        "gitlab_branch": gitlab_branch
    }

    response = lambda_client.invoke(
        FunctionName="Backup_Lambda",
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )

    response_payload = response['Payload'].read().decode('utf-8')
    res = json.loads(response_payload)
    return res["body"], res["statusCode"]


def send_whatsapp_messages(data):
    numbers = get_column_by_name(sheet)

    payload = {
        "data": data,
        "numbers": numbers
    }

    response = lambda_client.invoke(
        FunctionName="Twilio_Lambda",
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )

    res = json.loads(response['Payload'].read().decode("utf-8"))
    return res


def call_wiki_lambda(title):
    payload = json.dumps({"title": title})

    response = lambda_client.invoke(
        FunctionName="Wikipedia_Lambda",
        InvocationType="RequestResponse",
        Payload=payload
    )

    response_payload = response['Payload'].read().decode('utf-8')
    res = json.loads(response_payload)
    return res["body"], res["statusCode"]

def send_users_to_lambda(sheet):
    init_data = gitlab_user_data(sheet)
    payload = {
        "users": init_data
    }

    response = lambda_client.invoke(
        FunctionName='Init_Gitlab_Lambda',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )

    response_payload = response['Payload'].read().decode('utf-8')
    res = json.loads(response_payload)
    return res["body"], res["statusCode"]


def csv_to_xlsx(csv_data, commit_message, output_file_name):
    payload = {
        "output_file_name": output_file_name or "default.xlsx",
        "commit_message": commit_message or "default commit message",
        "csv_data": csv_data
    }

    json_payload = json.dumps(payload)

    response = lambda_client.invoke(
        FunctionName='CSV_TO_XLSX_LAMBDA',
        InvocationType='RequestResponse',
        Payload=json_payload
    )
    
    response_payload = response['Payload'].read().decode('utf-8')
    res = json.loads(response_payload)

    return res["body"], res["statusCode"]
