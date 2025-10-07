data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
data "aws_ecr_authorization_token" "ecr_auth" {}

data "aws_secretsmanager_secret" "master_secrets" {
  name = "terraform-master-credentials"
}

data "aws_secretsmanager_secret_version" "master_secrets" {
  secret_id = data.aws_secretsmanager_secret.master_secrets.id
}

data "aws_secretsmanager_secret" "infra_secrets" {
  name = "fase3-infra-totem-de-pedidos-secrets"
}

data "aws_secretsmanager_secret_version" "infra_secrets" {
  secret_id = data.aws_secretsmanager_secret.infra_secrets.id
}

locals {
  aws_infra_secrets = jsondecode(data.aws_secretsmanager_secret_version.infra_secrets.secret_string)
  aws_master_secrets = jsondecode(data.aws_secretsmanager_secret_version.master_secrets.secret_string)
  aws_ecr_auth_proxy_endpoint = replace(data.aws_ecr_authorization_token.ecr_auth.proxy_endpoint, "https://", "")
}

locals {
  aws_region   = "us-east-1"
  project_name = "fase3-lambda-totem-de-pedidos"
}

locals {
  default_password = "MasterDefault@12345"
  default_username = "00000000000"
  default_email    = "anonymous@anonymous.com"
}
