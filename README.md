# DevOps Lambda All-in-One

This repository provides a unified platform for DevOps automation using AWS Lambda, Flask, Google Sheets, GitLab, and WhatsApp integration. It streamlines common DevOps workflows through a web interface and modular Lambda functions.

## Features

- **Web UI** for triggering DevOps tasks (backups, repo creation, wiki search, etc.)
- **AWS Lambda** integration for serverless backend processing 
- **Google Sheets** integration in order to init gitlab users management and twilio contacts
- **GitLab** automation (repo creation, backup, etc.)
- **WhatsApp notifications** via Twilio
- **CSV to XLSX conversion** using Lambda

## Directory Structure

```
├── app.py                # Flask web server and routes
├── requirements.txt         # Python dependencies
├── credentials.json         # Google Sheets credentials (NOT in version control)
├── README.md
├── modules/
│   ├── envs.py             # Environment variables handling (NOT in version control)
│   ├── invoke_lambdas.py   # Lambda invocation utilities
│   ├── parse.py            # Data parsing helpers
│   ├── sheet_auth.py       # Google Sheets authentication
│   └── lambdas/            # Lambda function packages
│       ├── backup_package/
│       ├── create_repo_package/
│       ├── init_gitlab_package/
│       ├── whatsapp_notify/
│       ├── wikipedia_package/
│       └── xlsx_package/
└── templates/              # Flask HTML templates
    ├── backup.html
    ├── index.html
    ├── createrepo.html
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
   The following secrets are managed in AWS Secrets Manager:

   ```json
   {
     "CSV_LAMBDA_GITLAB_TOKEN": "your_gitlab_token",
     "GITLAB_XLSX_USER": "gitlab_username",
     "GITLAB_XLSX_REPO": "repository_name",
     "GITLAB_ADMIN_TOKEN": "admin_access_token",
     "TWILIO_AUTH_TOKEN": "twilio_auth_token",
     "TWILIO_ACCOUNT_SID": "account_sid",
     "TWILIO_WHATSAPP_FROM": "whatsapp_number"
   }
   ```

   - Ensure Lambda functions have appropriate IAM roles to access these secrets
   - Use AWS SDK to fetch secrets in your code:
   ```python
   import boto3
   
   def get_secret(secret_name):
       session = boto3.session.Session()
       client = session.client('secretsmanager')
       response = client.get_secret_value(SecretId=secret_name)
       return response['SecretString']
   ```

5. **Local Development Setup:**
   - Create `.env` file for local development (do not commit):
   ```bash
   # AWS Configuration
   AWS_REGION=your_region
   AWS_SECRET_NAME=your_secret_name
   
   # AWS credentials (if not using IAM role)
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key

   # Google
   SHEET_ID=your_google_sheet_id
   ```


6. **Run the server:**
   ```bash
   python server.py
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
- Use `.env` file only for local development
- Configure IAM roles with least privilege principle
- Monitor Secrets Manager access logs
- Rotate secrets periodically
- Enable AWS CloudTrail for API activity monitoring

## Lambda Functions

Each package in `modules/lambdas/` contains:
- Lambda function code
- Dependencies

## Development

1. Make changes to Lambda functions in their respective directories
2. Test locally using the Flask server
3. Deploy Lambda functions using AWS CLI or console
4. Update secrets in AWS Secrets Manager as needed