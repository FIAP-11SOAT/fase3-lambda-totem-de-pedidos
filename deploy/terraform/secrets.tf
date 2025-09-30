resource "aws_secretsmanager_secret" "secrets" {
  name                    = "${local.project_name}-secrets"
  description             = "Secrets for ${local.project_name} project"
  recovery_window_in_days = 0

  tags = {
    Name = "${local.project_name}-secrets"
  }
}

data "http" "cognito_jwks" {
  url = "https://${aws_cognito_user_pool.user_pool.endpoint}/.well-known/jwks.json"

  request_headers = {
    Accept = "application/json"
  }

  depends_on = [
    aws_cognito_user_pool.user_pool
  ]
}

resource "aws_secretsmanager_secret_version" "secrets" {
  secret_id = aws_secretsmanager_secret.secrets.id
  secret_string = jsonencode({
    COGNITO_USER_POOL_ID        = aws_cognito_user_pool.user_pool.id,
    COGNITO_USER_POOL_CLIENT_ID = aws_cognito_user_pool_client.user_pool_client.id,
    COGNITO_JWKS_JSON           = data.http.cognito_jwks.response_body,
    COGNITO_DEFAULT_USERNAME    = local.default_username,
    COGNITO_DEFAULT_PASSWORD    = local.default_password
  })

  depends_on = [
    data.http.cognito_jwks
  ]
}