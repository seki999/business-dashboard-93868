resource "aws_sqs_queue" "batch_events_dlq" {
  name                      = "${local.name}-batch-events-dlq"
  message_retention_seconds = 1209600
}

resource "aws_sqs_queue" "batch_events" {
  name                       = "${local.name}-batch-events"
  visibility_timeout_seconds = 60

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.batch_events_dlq.arn
    maxReceiveCount     = 5
  })
}

data "archive_file" "lambda_placeholder" {
  type        = "zip"
  output_path = "${path.module}/lambda-placeholder.zip"

  source {
    filename = "index.py"
    content  = <<-PY
      import json

      def handler(event, context):
          print(json.dumps({"received": event.get("Records", [])}))
          return {"status": "ok"}
    PY
  }
}

resource "aws_lambda_function" "batch_worker" {
  function_name    = "${local.name}-batch-worker"
  role             = aws_iam_role.lambda.arn
  handler          = "index.handler"
  runtime          = "python3.11"
  filename         = data.archive_file.lambda_placeholder.output_path
  source_code_hash = data.archive_file.lambda_placeholder.output_base64sha256
  timeout          = 30

  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      ENVIRONMENT = var.environment
      QUEUE_URL   = aws_sqs_queue.batch_events.url
    }
  }
}

resource "aws_lambda_event_source_mapping" "batch_worker" {
  event_source_arn = aws_sqs_queue.batch_events.arn
  function_name    = aws_lambda_function.batch_worker.arn
  batch_size       = 5
}

resource "aws_cloudwatch_event_rule" "daily_batch" {
  name                = "${local.name}-daily-batch"
  description         = "Sample EventBridge schedule for daily business batch."
  schedule_expression = "cron(0 18 * * ? *)"
}

resource "aws_cloudwatch_event_target" "daily_batch_to_sqs" {
  rule      = aws_cloudwatch_event_rule.daily_batch.name
  target_id = "SendToBatchQueue"
  arn       = aws_sqs_queue.batch_events.arn

  input = jsonencode({
    eventType = "daily-batch"
    source    = "eventbridge"
  })
}

data "aws_iam_policy_document" "eventbridge_to_sqs" {
  statement {
    sid     = "AllowEventBridgeSendMessage"
    actions = ["sqs:SendMessage"]
    resources = [
      aws_sqs_queue.batch_events.arn
    ]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_cloudwatch_event_rule.daily_batch.arn]
    }
  }
}

resource "aws_sqs_queue_policy" "batch_events" {
  queue_url = aws_sqs_queue.batch_events.id
  policy    = data.aws_iam_policy_document.eventbridge_to_sqs.json
}
