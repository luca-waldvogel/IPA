# Error Summary Service

This repository contains an error-summary service developed as part of my IPA for the completion of my EFZ. It was extracted from a larger, non-public codebase and is published here to document the project and its implementation.

The service runs as a scheduled AWS Lambda function. It:

1. queries application logs with Amazon CloudWatch Logs Insights;
2. groups recurring application errors and counts HTTP errors;
3. uses an LLM to turn the error patterns into short, readable explanations; and
4. publishes the resulting report to an Amazon SNS topic.

Reports cover the previous 24 hours from Tuesday to Friday and the previous 72 hours on Monday, providing a single summary for the weekend.

## Technology

- Python 3.14, Pydantic, and pytest
- AWS Lambda, CloudWatch Logs Insights, EventBridge, SNS, SSM, and ECR
- OpenAI-compatible LLM endpoint
- Terraform for infrastructure

## Repository structure

- `services/error_summary/` – service implementation, tests, and Terraform configuration
- `libs/model/` – data models used by the service
- `github/workflows/` – extracted deployment workflows

> [!NOTE]
> This is not a standalone distribution. Some shared libraries, build tooling, infrastructure, and configuration belong to the original private codebase and are therefore not included. The repository is intended primarily as a focused showcase of the IPA service.
