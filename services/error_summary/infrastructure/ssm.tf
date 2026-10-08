resource "aws_iam_role_policy" "lambda_ssm_access" {
  role = aws_iam_role.lambda_role.id
  name = "${local.project.name}-${local.env}-ssm"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = ["ssm:GetParameter", "ssm:GetParameters"],
        Effect   = "Allow",
        Resource = [
          data.aws_ssm_parameter.config_openai_api_key.arn
        ]
      }
    ]
  })
}
