resource "aws_cloudwatch_event_rule" "error_summary_schedule_monday" {
  name                = "${local.name}-schedule-monday"
  schedule_expression = "cron(0 4 ? * MON *)"

  tags = {
    Project = local.project.name
    Env     = local.env
    Name    = "${local.name}-schedule-monday"
  }
}

resource "aws_cloudwatch_event_rule" "error_summary_schedule_tue_fri" {
  name                = "${local.name}-schedule-tue-fri"
  schedule_expression = "cron(0 4 ? * TUE-FRI *)"

  tags = {
    Project = local.project.name
    Env     = local.env
    Name    = "${local.name}-schedule-tue-fri"
  }
}

resource "aws_cloudwatch_event_target" "error_summary_target_monday" {
  rule  = aws_cloudwatch_event_rule.error_summary_schedule_monday.name
  arn   = aws_lambda_function.error_summary_function.arn
  input = jsonencode({ is_monday = true })
}

resource "aws_cloudwatch_event_target" "error_summary_target_tue_fri" {
  rule = aws_cloudwatch_event_rule.error_summary_schedule_tue_fri.name
  arn  = aws_lambda_function.error_summary_function.arn
}

resource "aws_lambda_permission" "allow_eventbridge_monday" {
  statement_id  = "AllowExecutionFromEventBridgeMonday"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.error_summary_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.error_summary_schedule_monday.arn
}

resource "aws_lambda_permission" "allow_eventbridge_tue_fri" {
  statement_id  = "AllowExecutionFromEventBridgeTueFri"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.error_summary_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.error_summary_schedule_tue_fri.arn
}
