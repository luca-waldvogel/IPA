resource "aws_lambda_function" "error_summary_function" {
  function_name = local.name
  package_type  = "Image"

  # Will be replaced with the actual image during deployment.
  image_uri = "${data.aws_ecr_repository.dummy.repository_url}:latest"

  memory_size = 1028
  timeout     = 180
  publish     = true

  role = aws_iam_role.lambda_role.arn

  vpc_config {
    security_group_ids = [data.aws_security_group.lambda_sg.id]
    subnet_ids         = [data.aws_subnet.private_subnet.id]
  }

  dynamic "tracing_config" {
    for_each = local.settings.tracing ? [1] : []
    content {
      mode = "Active"
    }
  }

  environment {
    variables = {
      TRACING                          = local.settings.tracing
      LLM__ENDPOINTS                   = jsonencode(local.settings.llm_endpoints)
      LLM__DEFAULT                     = local.settings.llm_default
      LOG_GROUPS                       = jsonencode(local.log_groups)
      QUERY_POLLING_ATTEMPTS           = local.settings.query_polling_attempts
      QUERY_POLLING_INTERVAL           = local.settings.query_polling_interval
      SNS_TOPIC_ARN                    = local.sns_topic_arn
    }
  }

  lifecycle {
    ignore_changes        = [image_uri]
    create_before_destroy = true
  }

  depends_on = [aws_iam_role.lambda_role]

  tags = {
    Project = local.project.name
    Env     = local.env
    Name    = local.name
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.error_summary_function.function_name}"
  retention_in_days = 90

  lifecycle {
    create_before_destroy = true
  }
}
