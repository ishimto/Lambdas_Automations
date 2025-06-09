# DevOps Lambda Automations

A unified platform for automating DevOps workflows using AWS Lambda, Flask, Google Sheets, GitLab, and WhatsApp integration. This project provides a web interface for triggering common DevOps tasks, with modular Lambda functions managed via Terraform.

---

## Features

- **Web UI** for triggering DevOps tasks (backups, repo creation, wiki search, etc.)
- **AWS Lambda** for serverless backend processing
- **Google Sheets** integration for GitLab user management and Twilio contacts
- **GitLab** automation (repository creation, backup, etc.)
- **WhatsApp notifications** via Twilio
- **CSV to XLSX conversion** using Lambda
- **Infrastructure as Code** with Terraform for Lambda deployment
- **Unit and integration tests** for Lambda functions (see `modules/lambdas-terraform/tests/`)

---

## Directory Structure

```
├── app.py                      # Flask web server and routes
├── compose.yaml                # Docker Compose configuration
├── Dockerfile                  # Container definition
├── requirements.txt            # Python dependencies
├── credentials.json            # Google Sheets credentials (NOT in version control)
├── README.md
├── modules/
│   ├── __init__.py
│   ├── invoke_lambdas.py       # Lambda invocation utilities 
│   ├── parse.py                # Data parsing helpers
│   ├── secrets.py              # AWS Secrets Manager utilities
│   ├── sheet_auth.py           # Google Sheets authentication
│   └── lambdas-terraform/      # Lambda functions managed with Terraform
│       ├── Backup/
│       ├── CreateRepo/
│       ├── InitGitlab/
│       ├── WhatsappNotify/
│       ├── Wikipedia/
│       ├── xlsx/
│       │   └── main.tf         # Example Terraform file
│       └── tests/              # Unit and integration tests for Lambda functions
│           ├── test_flask_lambda_route_backup.py
│           ├── test_flask_lambda_route_init_gitlab.py
│           ├── test_flask_lambda_route_wiki.py
│           └── test_flask_lambda_route_xlsx.py
└── templates/                  # Flask HTML templates
    ├── backup.html
    ├── createrepo.html
    ├── index.html
    ├── init_gitlab.html
    ├── wiki.html
    └── xlsx.html
```

---

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
   # AWS Configuration
   AWS_REGION=eu-central-1

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

## Testing

All unit and integration tests for Lambda functions are located in `modules/lambdas-terraform/tests/`:

- `test_flask_lambda_route_backup.py`: Tests for the Backup Lambda function.
- `test_flask_lambda_route_init_gitlab.py`: Tests for the InitGitlab Lambda function.
- `test_flask_lambda_route_wiki.py`: Tests for the Wikipedia Lambda function.
- `test_flask_lambda_route_xlsx.py`: Tests for the xlsx Lambda function.

To run all tests:

```bash
pytest modules/lambdas-terraform/tests/
```

For integration tests, ensure all required environment variables and credentials are set.

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

## API Endpoints

- `/` - Dashboard
- `/createrepo` - Create GitLab repository
- `/backup` - Backup files from GitLab to S3
- `/wiki` - Wikipedia summary saved to txt file in GitLab repository
- `/init_gitlab` - Initialize GitLab project
- `/xlsx` - Convert CSV to XLSX and save it in GitLab repository
- `/bot` - WhatsApp bot webhook

---

## Security Best Practices

- Never commit sensitive credentials to version control
- Always use AWS Secrets Manager in production
- Configure IAM roles with least privilege principle
- Monitor Secrets Manager access logs
- Rotate secrets periodically
- Enable AWS CloudTrail for API activity monitoring

---

## Development Workflow

1. Make changes to Lambda functions or core modules
2. Add or update tests in `modules/lambdas-terraform/tests/`
3. Test locally using Flask and `pytest`
4. Deploy Lambda functions using Terraform
5. Update secrets in AWS Secrets Manager as needed

---