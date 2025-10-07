
resource "aws_lambda_function" "lambda" {
  function_name = "${local.project_name}-lambda-function"
  package_type  = "Image"
  image_uri     = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.region}.amazonaws.com/default-lambda-image:latest"
  role          = aws_iam_role.lambda_exec_role.arn

  memory_size = 512

  lifecycle {
    ignore_changes = [
      image_uri
    ]
  }

  environment {
    variables = {
      EXAMPLE_VAR = "example_value"
    }
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.lambda.function_name}"
  retention_in_days = 30

  tags = {
    Name = "${local.project_name}-${data.aws_region.current.region}-lambda-log-group"
  }
}