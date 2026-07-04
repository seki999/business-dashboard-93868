resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/sample/${local.name}/ecs"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${local.name}-batch-worker"
  retention_in_days = 14
}

resource "aws_cloudwatch_metric_alarm" "alb_5xx" {
  alarm_name          = "${local.name}-alb-5xx"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "HTTPCode_ELB_5XX_Count"
  namespace           = "AWS/ApplicationELB"
  period              = 60
  statistic           = "Sum"
  threshold           = 5
  treat_missing_data  = "notBreaching"

  dimensions = {
    LoadBalancer = aws_lb.backend.arn_suffix
  }
}

resource "aws_cloudwatch_metric_alarm" "sqs_dlq_visible" {
  alarm_name          = "${local.name}-sqs-dlq-visible"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = 300
  statistic           = "Maximum"
  threshold           = 0
  treat_missing_data  = "notBreaching"

  dimensions = {
    QueueName = aws_sqs_queue.batch_events_dlq.name
  }
}

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "${local.name}-operations"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        width  = 12
        height = 6
        properties = {
          region = var.aws_region
          title  = "ALB 5XX"
          metrics = [
            ["AWS/ApplicationELB", "HTTPCode_ELB_5XX_Count", "LoadBalancer", aws_lb.backend.arn_suffix]
          ]
          period = 60
          stat   = "Sum"
        }
      },
      {
        type   = "metric"
        width  = 12
        height = 6
        properties = {
          region = var.aws_region
          title  = "SQS Visible Messages"
          metrics = [
            ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", aws_sqs_queue.batch_events.name]
          ]
          period = 300
          stat   = "Maximum"
        }
      }
    ]
  })
}
