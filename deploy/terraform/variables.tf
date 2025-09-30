data "aws_region" "current" {}

locals {
  aws_region       = "us-east-1"
  project_name     = "fase3-lambda-totem-de-pedidos"
  default_password = "MasterDefault@12345"
  default_username = "00000000000"
  default_email    = "anonymous@anonymous.com"
}
