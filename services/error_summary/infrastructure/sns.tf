resource "aws_sns_topic" "error_summary_sns_topic" {
  name = local.name
}
