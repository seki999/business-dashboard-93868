# Terraform AWS Sample Architecture

This directory contains a portfolio-oriented Terraform sample for a neutral business dashboard.
It is intentionally not wired to real secrets, real account IDs, or real customer data.

## Covered AWS Components

- Frontend: S3 private bucket + CloudFront Origin Access Control
- Backend: ECS Fargate service behind an Application Load Balancer
- Network: VPC, public/private subnets, Internet Gateway, NAT Gateway, route tables
- Security: security groups, private ECS tasks, least-privilege IAM examples
- Operations: CloudWatch log groups, dashboard, alarms
- Async processing: SQS queue and dead-letter queue
- Scheduling/eventing: EventBridge rule for batch trigger
- Serverless helper: Lambda sample consumer/maintenance function
- CI/CD: GitHub OIDC IAM role and policies for Terraform/deploy pipeline

## Files

- `versions.tf`: provider and Terraform version constraints
- `variables.tf`: configurable sample inputs
- `main.tf`: local values and common tags
- `network.tf`: VPC, subnets, gateways, routing
- `security.tf`: security groups
- `frontend.tf`: S3 + CloudFront
- `backend_ecs.tf`: ECR, ECS cluster, task definition, ALB, service
- `iam.tf`: ECS, Lambda, GitHub Actions OIDC roles
- `sqs_eventbridge_lambda.tf`: SQS, EventBridge, Lambda sample
- `cloudwatch.tf`: logs, dashboard, alarms
- `outputs.tf`: useful output values

## Usage

```bash
terraform init
terraform plan -var="github_repository=owner/repository"
```

This is a sample configuration. Review CIDR ranges, IAM permissions, WAF, backup, secrets,
domain names, cost controls, and compliance requirements before using any part of it in production.
