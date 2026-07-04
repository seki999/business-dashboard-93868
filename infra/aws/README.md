# AWS Sample Config

This directory contains neutral AWS architecture samples for this portfolio project.
No real AWS account, access key, secret key, company name, customer name, or production data is required.

## Available Samples

- `sample-architecture.yml`: minimal CloudFormation skeleton.
- `terraform/`: Terraform sample covering frontend, backend, networking, security, observability, async processing, and CI/CD IAM.

## Terraform Sample Coverage

The Terraform version is designed to show a realistic deployment direction:

- Frontend: Amazon S3 private bucket and Amazon CloudFront with Origin Access Control.
- Backend: Amazon ECS Fargate container service behind an Application Load Balancer.
- Network: VPC, public/private subnets, Internet Gateway, NAT Gateway, and route tables.
- Security: security groups, private ECS tasks, S3 public access block, CloudFront HTTPS redirect, IAM roles and policies.
- Operations: CloudWatch log groups, metrics dashboard, and sample alarms.
- Async processing: Amazon SQS queue with dead-letter queue.
- Scheduling: Amazon EventBridge daily batch rule.
- Serverless: AWS Lambda sample worker connected to SQS.
- CI/CD: GitHub Actions OIDC IAM role sample and `.github/workflows/aws-sample-deploy.yml`.

## Notes

This is a portfolio sample, not a production-ready baseline. Before real use, review:

- domain and TLS certificate strategy
- AWS WAF and rate limiting
- RDS or Aurora design, backup, and encryption
- private VPC endpoints
- secret rotation with AWS Secrets Manager
- least-privilege IAM review
- cost controls and deletion protection
- audit logs and incident runbooks
