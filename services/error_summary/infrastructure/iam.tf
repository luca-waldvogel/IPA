resource "aws_iam_role" "lambda_role" {
  name = "${local.name}-function-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      },
    ]
  })

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Project = local.project.name
    Env     = local.env
    Name    = "${local.name}-function-role"
  }
}

resource "aws_iam_role_policy" "lambda_policy_cloudwatch" {
  name = "${local.name}-function-policy-cloudwatch"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Resource = [
          aws_cloudwatch_log_group.lambda_log_group.arn,
          "${aws_cloudwatch_log_group.lambda_log_group.arn}:log-stream:*",
        ]
      }
    ]
  })

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_iam_role_policy" "lambda_policy_cloudwatch_query" {
  name = "${local.name}-function-policy-cloudwatch-query"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:StartQuery",
          "logs:StopQuery",
          "logs:GetQueryResults"
        ]
        Resource = [
          aws_cloudwatch_log_group.lambda_log_group.arn,
          "${aws_cloudwatch_log_group.lambda_log_group.arn}:log-stream:*",
          data.aws_cloudwatch_log_group.elaboration_log_group.arn,
          "${data.aws_cloudwatch_log_group.elaboration_log_group.arn}:log-stream:*",
          data.aws_cloudwatch_log_group.extraction_log_group.arn,
          "${data.aws_cloudwatch_log_group.extraction_log_group.arn}:log-stream:*",
          data.aws_cloudwatch_log_group.ingestion_log_group.arn,
          "${data.aws_cloudwatch_log_group.ingestion_log_group.arn}:log-stream:*",
          data.aws_cloudwatch_log_group.pool_ingestion_log_group.arn,
          "${data.aws_cloudwatch_log_group.pool_ingestion_log_group.arn}:log-stream:*",
          data.aws_cloudwatch_log_group.pipe_enricher_log_group.arn,
          "${data.aws_cloudwatch_log_group.pipe_enricher_log_group.arn}:log-stream:*",
          data.aws_cloudwatch_log_group.api_log_group.arn,
          "${data.aws_cloudwatch_log_group.api_log_group.arn}:log-stream:*",
          data.aws_cloudwatch_log_group.pool_api_log_group.arn,
          "${data.aws_cloudwatch_log_group.pool_api_log_group.arn}:log-stream:*",
          data.aws_cloudwatch_log_group.migrator_log_group.arn,
          "${data.aws_cloudwatch_log_group.migrator_log_group.arn}:log-stream:*",
        ]
      }
    ]
  })

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_iam_role_policy" "lambda_policy_manage_network_interfaces" {
  name = "${local.name}-function-manage-network-interfaces"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface"
        ]
        Resource = aws_lambda_function.error_summary_function.arn
      },
    ]
  })

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_iam_role_policy" "lambda_policy_xray" {
  name = "${local.name}-xray"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "xray:PutTraceSegments",
          "xray:PutTelemetryRecords",
          "xray:GetSamplingRules",
          "xray:GetSamplingTargets"
        ],
        Resource = "*"
      }
    ]
  })

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_iam_role_policy" "lambda_policy_sns" {
  name = "${local.name}-lambda-sns"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]

        Resource = [
            aws_sns_topic.error_summary_sns_topic.arn
        ]
      },
    ]
  })
}
