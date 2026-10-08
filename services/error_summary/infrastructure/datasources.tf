data "aws_subnet" "private_subnet" {
  filter {
    name   = "tag:Name"
    values = ["${local.jobfit_networking_profile_prefix}-${local.env}-private-subnet-0"]
  }
}

data "aws_security_group" "lambda_sg" {
  filter {
    name   = "tag:Name"
    values = ["${local.jobfit_networking_profile_prefix}-${local.env}-sg-lambda"]
  }
}

data "aws_ecr_repository" "dummy" {
  provider = aws.shared
  name     = "dummy"
}

data "aws_ssm_parameter" "config_openai_api_key" {
  name  = "/jobfit-services-shared/OPENAI_API_KEY"
}

data "aws_cloudwatch_log_group" "extraction_log_group" {
    name = "/aws/lambda/jobfit-extraction-${local.env}"
}

data "aws_cloudwatch_log_group" "elaboration_log_group" {
    name = "/aws/lambda/jobfit-elaboration-${local.env}"
}

data "aws_cloudwatch_log_group" "ingestion_log_group" {
    name = "/aws/lambda/jobfit-ingestion-${local.env}"
}

data "aws_cloudwatch_log_group" "pool_ingestion_log_group" {
    name = "/aws/lambda/jobfit-pool-ingestion-${local.env}"
}

data "aws_cloudwatch_log_group" "pipe_enricher_log_group" {
    name = "/aws/lambda/jobfit-pipe-enricher-${local.env}"
}

data "aws_cloudwatch_log_group" "api_log_group" {
    name = "/ecs/jobfit-api-${local.env}"
}

data "aws_cloudwatch_log_group" "pool_api_log_group" {
    name = "/ecs/jobfit-pool-api-${local.env}"
}

data "aws_cloudwatch_log_group" "migrator_log_group" {
    name = "/ecs/jobfit-migrator-${local.env}"
}
