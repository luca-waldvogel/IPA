# --------------------------------------------------
# Project Configuration
# --------------------------------------------------

terraform {
  backend "s3" {
    bucket               = "jobfit-tf-states"
    workspace_key_prefix = "jobfit-error-summary-service"
    key                  = "state.tfstate"
    region               = "eu-central-1"
    encrypt              = true
    kms_key_id           = "arn:aws:kms:eu-central-1:897729132726:key/e2a824a5-d931-436f-86fd-7d68654dff10"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.24.0"
    }
  }

  required_version = ">= 1.5.2"
}

provider "aws" {
  region = "eu-central-1"

  assume_role {
    role_arn = local.settings.role_arn
  }
}

provider "aws" {
  alias  = "shared"
  region = "eu-central-1"
}

variable "role_to_assume" {
  type = map(object({
    role_arn = string
  }))

  default = {
    dev = {
      role_arn = "arn:aws:iam::407276168849:role/tf-infra-dev-deploy-role"
    }
    prod = {
      role_arn = "arn:aws:iam::304848207041:role/tf-infra-prod-deploy-role"
    }
  }
}


variable "workspace_settings" {
  type = map(object({
    llm_endpoints = map(object({
      url     = string
      api_key = optional(string)
    }))
    llm_default               = string
    tracing                   = bool
    max_concurrent_executions = number
    query_polling_attempts    = number
    query_polling_interval    = number
  }))

  default = {
    dev = {
      llm_endpoints = {
        "gpt-4.1-mini" = {
          url = "https://swedencentral.api.cognitive.microsoft.com/openai/deployments/JobFitMini2/chat/completions?api-version=2024-08-01-preview"
        }
      }
      llm_default               = "gpt-4.1-mini"
      tracing                   = true
      max_concurrent_executions = 2
      query_polling_attempts    = 3
      query_polling_interval    = 5
    }

    prod = {
      llm_endpoints = {
        "gpt-4.1-mini" = {
          url = "https://swedencentral.api.cognitive.microsoft.com/openai/deployments/JobFitMini2/chat/completions?api-version=2024-08-01-preview"
        }
      }
      llm_default               = "gpt-4.1-mini"
      tracing                   = true
      max_concurrent_executions = 2
      query_polling_attempts    = 5
      query_polling_interval    = 5
    }
  }
}


locals {
  env = terraform.workspace
  project = {
    name = "jobfit-error-summary"
  }

  name = "${local.project.name}-${local.env}"

  jobfit_networking_profile_prefix = "jobfit-networking"
  settings = {
    role_arn                  = var.role_to_assume[local.env].role_arn
    tracing                   = var.workspace_settings[local.env].tracing
    llm_endpoints             = var.workspace_settings[local.env].llm_endpoints
    llm_default               = var.workspace_settings[local.env].llm_default
    max_concurrent_executions = var.workspace_settings[local.env].max_concurrent_executions
    query_polling_attempts    = var.workspace_settings[local.env].query_polling_attempts
    query_polling_interval    = var.workspace_settings[local.env].query_polling_interval
  }

  log_groups = [
    data.aws_cloudwatch_log_group.elaboration_log_group.name,
    data.aws_cloudwatch_log_group.extraction_log_group.name,
    data.aws_cloudwatch_log_group.ingestion_log_group.name,
    data.aws_cloudwatch_log_group.pool_ingestion_log_group.name,
    data.aws_cloudwatch_log_group.pipe_enricher_log_group.name,
    data.aws_cloudwatch_log_group.api_log_group.name,
    data.aws_cloudwatch_log_group.pool_api_log_group.name,
    data.aws_cloudwatch_log_group.migrator_log_group.name,
  ]
  sns_topic_arn             = aws_sns_topic.error_summary_sns_topic.arn
}
