locals {
  name       = "${var.project_name}-${var.environment}"
  short_name = "sbd-${var.environment}"

  public_subnet_cidrs  = ["10.40.0.0/24", "10.40.1.0/24"]
  private_subnet_cidrs = ["10.40.10.0/24", "10.40.11.0/24"]

  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    Purpose     = "PortfolioSample"
  }
}

data "aws_caller_identity" "current" {}
