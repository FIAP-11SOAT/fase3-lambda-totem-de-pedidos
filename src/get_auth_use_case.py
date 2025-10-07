from botocore.exceptions import ClientError

from src.aws_cognito_idp import AuthService
from src.exceptions import HttpException
from src.http_response import http_response


def get_auth_use_case(service: AuthService, query: dict):
    tax_id = query.get("tax_id", None)
    if not tax_id:
        raise HttpException(status_code=400, message="tax_id is required in query parameters.")
    try:
        user = service.search_user_by_cpf(cpf=tax_id)
        if not user:
            raise HttpException(status_code=404, message="User not found.")
        response = service.authenticate_user(username=user["Username"])
        body = {
            "message": "User authenticated successfully.",
            "access_token": response.get("AuthenticationResult", {}).get("AccessToken")
        }
        return http_response(status_code=200, body=body)
    except ClientError as ce:
        if ce.response["Error"]["Code"] == "UserNotFoundException":
            raise HttpException(status_code=404, message="User not found.")
        raise HttpException(status_code=500, message=f"Internal server error: {str(ce)}")
    except HttpException as he:
        raise he
    except Exception as e:
        raise HttpException(status_code=500, message=f"Internal server error: {str(e)}")
