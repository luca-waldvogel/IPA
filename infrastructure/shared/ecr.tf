/*
  IAM permissions for ECR repositories
*/
data "aws_iam_policy_document" "repository_policy_document" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = [
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
    ]
  }

  statement {
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = local.account_ids
    }

    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:BatchGetImage",
      "ecr:DescribeImages",
      "ecr:GetDownloadUrlForLayer",
      "ecr:DescribeRepositories",
    ]
  }

  statement {
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = local.deployment_roles
    }

    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:BatchGetImage",
      "ecr:DescribeImages",
      "ecr:GetDownloadUrlForLayer",
      "ecr:DescribeRepositories",
      "ecr:CompleteLayerUpload",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:PutImage",
    ]
  }
}

/*
  Elaboration Repository
*/
resource "aws_ecr_repository" "elaboration_repository" {
  name = "${local.project.name}/elaboration"

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project = local.project.name
    Name    = "${local.project.name}-elaboration"
  }
}

resource "aws_ecr_repository_policy" "elaboration_repository" {
  repository = aws_ecr_repository.elaboration_repository.name
  policy     = data.aws_iam_policy_document.repository_policy_document.json
}

/*
  Extraction Repository
*/
resource "aws_ecr_repository" "extraction_repository" {
  name = "${local.project.name}/extraction"

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project = local.project.name
    Name    = "${local.project.name}-extraction"
  }
}

resource "aws_ecr_repository_policy" "extraction_repository_policy" {
  repository = aws_ecr_repository.extraction_repository.name
  policy     = data.aws_iam_policy_document.repository_policy_document.json
}

/*
  Ingestion Repository
*/
resource "aws_ecr_repository" "ingestion_repository" {
  name = "${local.project.name}/ingestion"

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project = local.project.name
    Name    = "${local.project.name}-ingestion"
  }
}

resource "aws_ecr_repository_policy" "ingestion_repository_policy" {
  repository = aws_ecr_repository.ingestion_repository.name
  policy     = data.aws_iam_policy_document.repository_policy_document.json
}

resource "aws_ecr_repository" "pool_ingestion_repository" {
  name = "${local.project.name}/pool-ingestion"

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project = local.project.name
    Name    = "${local.project.name}-pool-ingestion"
  }
}


resource "aws_ecr_repository_policy" "pool_ingestion_repository_policy" {
  repository = aws_ecr_repository.pool_ingestion_repository.name
  policy     = data.aws_iam_policy_document.repository_policy_document.json
}

/*
  Migrator Repository
*/
resource "aws_ecr_repository" "migrator_repository" {
  name = "${local.project.name}/migrator"

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project = local.project.name
    Name    = "${local.project.name}-migrator"
  }
}

resource "aws_ecr_repository_policy" "migrator_repository_policy" {
  repository = aws_ecr_repository.migrator_repository.name
  policy     = data.aws_iam_policy_document.repository_policy_document.json
}

/*
  Jobfit API
*/
resource "aws_ecr_repository" "api_repository" {
  name = "${local.project.name}/api"

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project = local.project.name
    Name    = "${local.project.name}-api"
  }
}

resource "aws_ecr_repository_policy" "api_repository_policy" {
  repository = aws_ecr_repository.api_repository.name
  policy     = data.aws_iam_policy_document.repository_policy_document.json
}

/*
  Pool API
*/
resource "aws_ecr_repository" "pool_api_repository" {
  name = "${local.project.name}/pool-api"

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project = local.project.name
    Name    = "${local.project.name}-pool-api"
  }
}

resource "aws_ecr_repository_policy" "pool_api_repository_policy" {
  repository = aws_ecr_repository.pool_api_repository.name
  policy     = data.aws_iam_policy_document.repository_policy_document.json
}

#IPA
/*
  Error Summary Repository
*/
resource "aws_ecr_repository" "error_summary_repository" {
  name = "${local.project.name}/error-summary"

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project = local.project.name
    Name    = "${local.project.name}-error-summary"
  }
}

resource "aws_ecr_repository_policy" "error_summary_repository_policy" {
  repository = aws_ecr_repository.error_summary_repository.name
  policy     = data.aws_iam_policy_document.repository_policy_document.json
}
#IPA

/*
  Dummy Repository to use as a placeholder for new deployments
*/
resource "aws_ecr_repository" "dummy_repository" {
  name                 = "dummy"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_repository_policy" "dummy_repository_policy" {
  repository = aws_ecr_repository.dummy_repository.name
  policy     = data.aws_iam_policy_document.repository_policy_document.json
}

# NOTE: This creates a rule that will never match (we'll never have 999999 images)
# effectively protecting tagged images from lifecycle expiration
locals {
  ecr_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Protect deployed images - never delete"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["deployed-"]
          countType     = "imageCountMoreThan"
          countNumber   = 999999
        }
        action = {
          type = "expire"
        }
      },
      {
        rulePriority = 10
        description  = "Keep last 10 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

/*
   Lifecycle policies for all repositories
 */
resource "aws_ecr_lifecycle_policy" "elaboration_lifecycle" {
  repository = aws_ecr_repository.elaboration_repository.name
  policy     = local.ecr_lifecycle_policy
}

resource "aws_ecr_lifecycle_policy" "extraction_lifecycle" {
  repository = aws_ecr_repository.extraction_repository.name
  policy     = local.ecr_lifecycle_policy
}

resource "aws_ecr_lifecycle_policy" "ingestion_lifecycle" {
  repository = aws_ecr_repository.ingestion_repository.name
  policy     = local.ecr_lifecycle_policy
}

resource "aws_ecr_lifecycle_policy" "pool_ingestion_lifecycle" {
  repository = aws_ecr_repository.pool_ingestion_repository.name
  policy     = local.ecr_lifecycle_policy
}

resource "aws_ecr_lifecycle_policy" "api_lifecycle" {
  repository = aws_ecr_repository.api_repository.name
  policy     = local.ecr_lifecycle_policy
}

resource "aws_ecr_lifecycle_policy" "pool_api_lifecycle" {
  repository = aws_ecr_repository.pool_api_repository.name
  policy     = local.ecr_lifecycle_policy
}

resource "aws_ecr_lifecycle_policy" "migrator_lifecycle" {
  repository = aws_ecr_repository.migrator_repository.name
  policy     = local.ecr_lifecycle_policy
}

#IPA
resource "aws_ecr_lifecycle_policy" "error_summary_lifecycle" {
  repository = aws_ecr_repository.error_summary_repository.name
  policy     = local.ecr_lifecycle_policy
}
#IPA
