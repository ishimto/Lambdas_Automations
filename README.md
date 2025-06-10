# DevOps Lambda Automations Platform

A comprehensive DevOps automation platform integrating AWS Lambda, Flask, Google Sheets, GitLab, and WhatsApp to streamline common DevOps workflows.

--- 

## Project Structure

```
.
├── app.py                  # Flask application entry point
├── compose.yaml            # Docker Compose configuration
├── Dockerfile             # Container definition
├── Jenkinsfile           # CI/CD pipeline definition
├── requirements.txt       # Python dependencies
├── credentials.json       # Google Sheets credentials (gitignored)
├── modules/
│   ├── __init__.py
│   ├── invoke_lambdas.py  # Lambda invocation utilities
│   ├── parse.py           # Data parsing helpers
│   ├── secrets.py         # AWS Secrets Manager utilities
│   ├── sheet_auth.py      # Google Sheets authentication
│   └── lambdas-terraform/ # Lambda functions with Terraform
│       ├── Backup/ # Example directory
│       │   ├── code/
│       │   │   ├── lambda_function.py
│       │   │   └── requirements.txt
│       │   ├── main.tf
│       │   ├── provider.tf
│       │   └── variables.tf
│       ├── CreateRepo/
│       ├── InitGitlab/
│       ├── WhatsappNotify/
│       ├── wikipedia/
│       └── xlsx/
├── templates/             # Flask HTML templates
│   ├── backup.html
│   ├── createrepo.html
│   ├── index.html
│   ├── init_gitlab.html
│   ├── wiki.html
│   └── xlsx.html
└── tests/
    ├── pytest/
    │   ├── compose.yaml
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   ├── test_flask_lambda_route_backup.py
    │   ├── test_flask_lambda_route_init_gitlab.py
    │   ├── test_flask_lambda_route_wiki.py
    │   └── test_flask_lambda_route_xlsx.py
    └── trivy/
        └── compose.yaml
```
---

## Features

- **Web Interface**: Flask-based dashboard for DevOps tasks
- **Serverless Backend**: AWS Lambda functions
- **Google Sheets Integration**: GitLab users and Twilio contacts management
- **GitLab Automation**: Repository creation, backups, wiki management
- **WhatsApp Notifications**: Real-time alerts via Twilio
- **File Processing**: CSV to XLSX conversion

---

## Setup Instructions

1. **Create and activate virtual environment (if you use docker, skip):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies (if you use docker, skip):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Sheets credentials:**
   - Obtain Google Sheets API credentials from Google Cloud Console
   - Save as `credentials.json` in the project root
   - Add to `.gitignore`:
     ```bash
     echo "credentials.json" >> .gitignore
     ```

4. **AWS Secrets Manager Configuration:**
   Store the following secrets in AWS Secrets Manager:
   ```json
   {
     "CSV_LAMBDA_GITLAB_TOKEN": "your_gitlab_token",
     "GITLAB_XLSX_USER": "gitlab_username",
     "GITLAB_XLSX_REPO": "repository_name",
     "GITLAB_ADMIN_TOKEN": "admin_access_token",
     "GITLAB_WIKI_TOKEN": "wiki_repo_access_token",
     "TWILIO_AUTH_TOKEN": "twilio_auth_token",
     "TWILIO_ACCOUNT_SID": "account_sid",
     "TWILIO_WHATSAPP_FROM": "whatsapp_number"
   }
   ```

5. **Environment Variables:**
   Set the following environment variables:
   ```bash

   # GitLab
   GITLAB_URL=http://your.gitlab.url
   GITLAB_USER=your_user
   GITLAB_REPO=your_repo
   GITLAB_BRANCH=main
   ```

6. **Run the Application:**
   - Using Docker:
     ```bash
     docker compose up --build
     ```
   - Or locally:
     ```bash
     python app.py
     ```

---

## API Endpoints

- `/` - Dashboard
- `/createrepo` - Create GitLab repository
- `/backup` - Backup files from GitLab to S3
- `/wiki` - Wikipedia summary saved to txt file in GitLab repository
- `/init_gitlab` - Initialize GitLab project
- `/xlsx` - Convert CSV to XLSX and save it in GitLab repository
- `/bot` - WhatsApp bot webhook

---

## Terraform Deployment

Each Lambda function in `modules/lambdas-terraform/` contains:

- Terraform configuration files (`main.tf`, `variables.tf`, etc.)
- Lambda function code and dependencies
- IAM role and policy definitions

To deploy or update Lambda functions:

```bash
cd modules/lambdas-terraform/<LambdaName>
terraform init
terraform apply
```

---

## Lambda Functions

Each Lambda function in `modules/lambdas-terraform/` contains:
- `code/lambda_function.py`: Main function logic
- `code/requirements.txt`: Function dependencies
- `main.tf`: Terraform infrastructure definition
- `provider.tf`: AWS provider configuration
- `variables.tf`: Terraform variables

Available functions:
- Backup: GitLab to S3 backup
- CreateRepo: GitLab repository creation
- InitGitlab: Project initialization
- WhatsappNotify: Twilio notifications
- Wikipedia: Wiki content management
- XLSX: CSV to XLSX conversion

---

## Testing

### Integration Tests
Located in `tests/pytest/`:
- `test_flask_lambda_route_backup.py`: Tests backup functionality
- `test_flask_lambda_route_init_gitlab.py`: Tests GitLab initialization
- `test_flask_lambda_route_wiki.py`: Tests wiki summary functionality
- `test_flask_lambda_route_xlsx.py`: Tests XLSX conversion

Run tests using Docker Compose:
```bash
cd tests/pytest
docker compose run tests
```

### Security Tests
Located in `tests/trivy/`:
- Container vulnerability scanning configuration

Run security tests:
```bash
cd tests/trivy
docker compose run trivy
```


### Jenkins 
Jenkinsfile run the tests for you, use automation!!

---

## Security Best Practices

- Never commit sensitive credentials to version control
- Always use AWS Secrets Manager in production
- Configure IAM roles with least privilege principle
- Monitor Secrets Manager access logs
- Rotate secrets periodically
- Enable AWS CloudTrail for API activity monitoring