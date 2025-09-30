
resource "aws_cognito_user_pool" "user_pool" {
  name = "${local.project_name}-user-pool"

  mfa_configuration        = "OFF"
  auto_verified_attributes = []

  admin_create_user_config {
    allow_admin_create_user_only = true
  }

  schema {
    name                = "email"
    attribute_data_type = "String"
    required            = true
    mutable             = true
    string_attribute_constraints {
      min_length = 1
      max_length = 256
    }
  }

  schema {
    name                = "name"
    attribute_data_type = "String"
    required            = true
    mutable             = true
    string_attribute_constraints {
      min_length = 1
      max_length = 256
    }
  }

  password_policy {
    require_lowercase = true
    minimum_length    = 8
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

}

resource "aws_cognito_user_pool_client" "user_pool_client" {
  name                = "${local.project_name}-pool-client"
  user_pool_id        = aws_cognito_user_pool.user_pool.id
  explicit_auth_flows = ["ALLOW_ADMIN_USER_PASSWORD_AUTH"]
}


# Default users in Cognito User Pool
resource "aws_cognito_user" "anonymous_user" {
  user_pool_id = aws_cognito_user_pool.user_pool.id
  username     = local.default_username

  attributes = {
    email = local.default_email
    name  = "Anonymous User"
  }

  password       = local.default_password
  message_action = "SUPPRESS"
}

resource "aws_cognito_user" "employee_user" {
  user_pool_id = aws_cognito_user_pool.user_pool.id
  username     = "11111111111"

  attributes = {
    email = "employee@employee.com"
    name  = "Employee 01"
  }

  password       = local.default_password
  message_action = "SUPPRESS"
}


# User Groups in Cognito User Pool
resource "aws_cognito_user_group" "customers_group" {
  name         = "customers"
  user_pool_id = aws_cognito_user_pool.user_pool.id
  description  = "Group for customers users"
}

resource "aws_cognito_user_group" "employees_group" {
  name         = "employees"
  user_pool_id = aws_cognito_user_pool.user_pool.id
  description  = "Group for employees users"
}


# Assign users to groups
resource "aws_cognito_user_in_group" "customers_group_assigned_to_anonymous_user" {
  user_pool_id = aws_cognito_user_pool.user_pool.id
  username     = aws_cognito_user.anonymous_user.username
  group_name   = aws_cognito_user_group.customers_group.name
}

resource "aws_cognito_user_in_group" "employees_group_assigned_to_employee_user" {
  user_pool_id = aws_cognito_user_pool.user_pool.id
  username     = aws_cognito_user.employee_user.username
  group_name   = aws_cognito_user_group.employees_group.name
}