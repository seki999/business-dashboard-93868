output "frontend_bucket_name" {
  description = "Private S3 bucket for frontend assets."
  value       = aws_s3_bucket.frontend.bucket
}

output "cloudfront_domain_name" {
  description = "CloudFront domain serving the frontend."
  value       = aws_cloudfront_distribution.frontend.domain_name
}

output "backend_alb_dns_name" {
  description = "Application Load Balancer DNS name for backend ECS service."
  value       = aws_lb.backend.dns_name
}

output "ecr_repository_url" {
  description = "ECR repository URL for backend container images."
  value       = aws_ecr_repository.backend.repository_url
}

output "sqs_queue_url" {
  description = "SQS queue URL used for batch/event processing."
  value       = aws_sqs_queue.batch_events.url
}

output "github_actions_role_arn" {
  description = "IAM role ARN for GitHub Actions OIDC deployment."
  value       = aws_iam_role.github_actions.arn
}
