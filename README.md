# DevOps Lambda Automations

This repository provides a unified platform for DevOps automation using AWS Lambda, Flask, Google Sheets, GitLab, and WhatsApp integration. It streamlines common DevOps workflows through a web interface and modular Lambda functions.

## Features

- **Web UI** for triggering DevOps tasks (backups, repo creation, wiki search, etc.)
- **AWS Lambda** integration for serverless backend processing 
- **Google Sheets** integration for GitLab users management and Twilio contacts
- **GitLab** automation (repo creation, backup, etc.)
- **WhatsApp notifications** via Twilio
- **CSV to XLSX conversion** using Lambda

## Directory Structure

```
├── app.py                # Flask web server and routes
├── compose.yaml          # Docker compose configuration
├── Dockerfile           # Container definition
├── requirements.txt     # Python dependencies
├── credentials.json     # Google Sheets credentials (NOT in version control)
├── README.md
├── modules/
│   ├── __init__.py
│   ├── invoke_lambdas.py   # Lambda invocation utilities 
│   ├── parse.py            # Data parsing helpers
│   ├── secrets.py          # AWS Secrets Manager utilities
│   ├── sheet_auth.py       # Google Sheets authentication
│   └── lambdas-terraform/  # Lambda functions with Terraform
│       ├── Backup/
│       ├── CreateRepo/
│       ├── InitGitlab/
│       ├── WhatsappNotify/
│       ├── Wikipedia/
│       └── xlsx/
└── templates/           # Flask HTML templates
    ├── backup.html
    ├── createrepo.html
    ├── index.html
    ├── init_gitlab.html
    ├── wiki.html
    └── xlsx.html
```

## Setup Instructions

1. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Sheets credentials:**
   - Get your Google Sheets API credentials from Google Cloud Console
   - Save them as `credentials.json` in the project root
   - Add to `.gitignore`:
   ```bash
   echo "credentials.json" >> .gitignore
   ```

4. **AWS Secrets Manager Configuration:**
   The following secrets are required in AWS Secrets Manager:

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
   Required environment variables:
   ```bash
   # AWS Configuration
   AWS_REGION=eu-central-1
   
   # GitLab
   GITLAB_URL=http://your.gitlab.url
   GITLAB_USER=your_user
   GITLAB_REPO=your_repo
   GITLAB_BRANCH=main
   ```

6. **Run the Application:**
   
   Using Docker:
   ```bash
   docker compose up --build
   ```

   Or locally:
   ```bash
   python app.py
   ```

## API Endpoints

- `/` - Dashboard
- `/createrepo` - Create GitLab repository
- `/backup` - Backup files from GitLab to S3
- `/wiki` - Wikipedia summary saved to txt file in GitLab repository
- `/init_gitlab` - Initialize GitLab project
- `/xlsx` - Convert CSV to XLSX and save it in GitLab repository
- `/bot` - WhatsApp bot webhook

## Security Best Practices

- Never commit sensitive credentials to version control
- Always use AWS Secrets Manager in production
- Configure IAM roles with least privilege principle
- Monitor Secrets Manager access logs
- Rotate secrets periodically
- Enable AWS CloudTrail for API activity monitoring

## Lambda Functions

Each Lambda function in `modules/lambdas-terraform/` contains:
- Terraform configuration files
- Lambda function code
- Dependencies in requirements.txt
- IAM role and policy definitions

## Development

1. Make changes to Lambda functions in their respective directories
2. Test locally using the Flask server
3. Deploy Lambda functions using Terraform
4. Update secrets in AWS Secrets Manager as needed