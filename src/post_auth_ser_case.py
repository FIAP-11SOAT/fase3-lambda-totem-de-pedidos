import re

from botocore.exceptions import ClientError

from src.aws_cognito_idp import AuthService
from src.exceptions import HttpException
from src.http_response import http_response


def post_auth_use_case(service: AuthService, data: dict):
    tax_id = data.get("tax_id")
    nome = data.get("nome")
    email = data.get("email")

    if not tax_id or not nome or not email:
        raise HttpException(status_code=400, message="tax_id, nome, and email are required in the request body.")

    if not re.fullmatch(r'\d{11}', tax_id):
        raise HttpException(status_code=400, message="tax_id must be 11 digits.")

    try:
        user = service.search_user_by_cpf(cpf=tax_id)
        if user:
            raise HttpException(status_code=409, message="User with this tax_id already exists.")
        service.register_user(cpf=tax_id, name=nome, email=email)
        return http_response(status_code=200, body={"message": "User created successfully."})
    except ClientError as ce:
        if ce.response["Error"]["Code"] == "UserNotFoundException":
            raise HttpException(status_code=404, message="User not found.")
        raise HttpException(status_code=500, message=f"Internal server error: {str(ce)}")
    except HttpException as he:
        raise he
    except Exception as e:
        raise HttpException(status_code=500, message=f"Internal server error: {str(e)}")
