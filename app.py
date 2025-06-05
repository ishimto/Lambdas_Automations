import io
import json
import base64
from flask import request, Flask, send_file, render_template
from twilio.twiml.messaging_response import MessagingResponse
from modules.invoke_lambdas import csv_to_xlsx, send_users_to_lambda, call_wiki_lambda, send_whatsapp_messages, backup_git, create_repo
from modules.sheet_auth import sheet
from modules.parse import get_contacts


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/createrepo', methods=["GET", "POST"])
def createrepo():
    if request.method == "GET":
        return render_template("createrepo.html")
    repo_name = request.form.get("repo_name")
    repo_visibility = request.form.get("repo_visibility")
    response = create_repo(repo_name, repo_visibility)
    return response

@app.route('/backup', methods=["GET", "POST"])
def backup():
    if request.method == "GET":
        return render_template("backup.html")
    
    file_name = request.form.get("file_name")
    bucket_name = request.form.get("bucket_name")
    gitlab_user = request.form.get("gitlab_user")
    gitlab_repo = request.form.get("gitlab_repo")
    gitlab_branch = request.form.get("gitlab_branch")
    response = backup_git(file_name, bucket_name, gitlab_user, gitlab_repo, gitlab_branch)
    send_whatsapp_messages(response)
    return response



@app.route('/wiki', methods=["GET", "POST"])
def wiki():
    if request.method == "GET":
        return render_template("wiki.html")
    title = request.form.get("title")
    response = call_wiki_lambda(title)
    send_whatsapp_messages(response)
    return response

@app.route('/init_gitlab', methods=["GET", "POST"])
def init_gitlab():
    if request.method == "GET":
        return render_template("init_gitlab.html")
    
    response = send_users_to_lambda(sheet)
    send_whatsapp_messages(response)
    return response

@app.route('/xlsx', methods=["GET", "POST"])
def xlsx():
    if request.method == "GET":
        return render_template("xlsx.html")

    csv_data = request.form.get("csv_data")
    commit_message = request.form.get("commit_message")
    output_file_name = request.form.get("output_file_name")
    if not csv_data:
        send_whatsapp_messages("not found csv data")
        return "No found csv data", 400

    response = csv_to_xlsx(csv_data=csv_data, commit_message=commit_message, output_file_name=output_file_name)
    send_whatsapp_messages(response)
    return response


@app.route('/bot', methods=["POST"])
def bot_system():    
    
    user_msg = request.values.get('Body', '').lower()
    reply = False

    if user_msg == "contacts":
        contacts = get_contacts(sheet)
        reply = "\n".join([f"{first} {last}" for first, last in contacts]) 
    
    if reply is False:
        reply = "Sorry, we can't handle this."

    response = MessagingResponse()
    response.message(reply)

    return str(response)

if __name__ == "__main__":
    app.run()

