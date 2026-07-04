# AWS Sample Config

このディレクトリは portfolio sample のための AWS 構成例です。実際の AWS アカウント、Access Key、Secret Key は不要です。

想定構成:

- Application Load Balancer
- Amazon ECS Fargate または AWS App Runner
- Amazon RDS for PostgreSQL
- Amazon S3 for static/report artifacts
- Amazon CloudWatch Logs/Metrics
- AWS Secrets Manager for DB credentials

`sample-architecture.yml` は最小限の CloudFormation skeleton であり、実運用投入には VPC、IAM、WAF、バックアップ、監視アラームなどの詳細設計が必要です。
