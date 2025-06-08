resource "aws_iam_role" "lambda_role" {
  name = "xlsx_secrets_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_permissions_policy" {
  name = "xlsx_secrets_and_logs_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "arn:aws:secretsmanager:eu-central-1:664418959298:secret:lambda/creds-e67YHH"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}



resource "aws_iam_role_policy_attachment" "secrets_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_permissions_policy.arn
}


module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "CSV_TO_XLSX_LAMBDA"
  description   = "Convert CSV to XLSX and save it in gitlab repo"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  create_role     = false
  lambda_role = aws_iam_role.lambda_role.arn
  timeout = 20

  source_path = [
    "./code/lambda_function.py",
    {
    path             = "./code/requirements.txt",
    pip_requirements = true
    }
  ]

  tags = {
    Name = "XLSX"
  }
}
