data "aws_apigatewayv2_api" "http_api" {
  api_id = local.aws_infra_secrets["GTW_ID"]
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id                 = data.aws_apigatewayv2_api.http_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.lambda.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "hello_route" {
  api_id    = data.aws_apigatewayv2_api.http_api.id
  route_key = "ANY /auth"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${data.aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}
