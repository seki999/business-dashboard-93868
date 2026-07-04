variable "project_name" {
  description = "Neutral sample project name used as an AWS resource prefix."
  type        = string
  default     = "sample-business-dashboard"
}

variable "aws_region" {
  description = "AWS region for regional resources."
  type        = string
  default     = "ap-northeast-1"
}

variable "environment" {
  description = "Deployment environment label."
  type        = string
  default     = "sample"
}

variable "vpc_cidr" {
  description = "CIDR block for the sample VPC."
  type        = string
  default     = "10.40.0.0/16"
}

variable "availability_zones" {
  description = "Two availability zones for high availability sample layout."
  type        = list(string)
  default     = ["ap-northeast-1a", "ap-northeast-1c"]
}

variable "container_image" {
  description = "Backend container image. CI/CD should replace this with an ECR image tag."
  type        = string
  default     = "public.ecr.aws/docker/library/python:3.11-slim"
}

variable "container_port" {
  description = "Backend container port."
  type        = number
  default     = 8000
}

variable "desired_count" {
  description = "Desired number of ECS tasks."
  type        = number
  default     = 2
}

variable "github_repository" {
  description = "GitHub repository allowed to assume the CI/CD OIDC role. Example: owner/repo."
  type        = string
  default     = "example-owner/example-repository"
}

variable "allowed_admin_cidr" {
  description = "Optional CIDR allowed for administrative access examples. Keep narrow in real use."
  type        = string
  default     = "203.0.113.10/32"
}
