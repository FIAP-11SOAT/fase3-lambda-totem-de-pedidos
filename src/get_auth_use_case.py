import logging

from botocore.exceptions import ClientError

from src.aws_cognito_idp import AuthService
from src.http_response import http_response


def get_auth_use_case(service: AuthService, query: dict):
    tax_id = query.get("tax_id", None)
    if not tax_id:
        logging.error("tax_id is required in query parameters.")
        return http_response(status_code=400, body={"message": "tax_id is required."})
    try:
        user = service.search_user_by_cpf(cpf=tax_id)
        if not user:
            logging.error(f"User not found for tax_id: {tax_id}")
            return http_response(status_code=404, body={"message": "User not found."})
        response = service.authenticate_user(username=user["Username"])
        return http_response(status_code=200,
                             body={"message": "Authentication successful.",
                                   "access_token": response.get("AuthenticationResult", {}).get("AccessToken")})
    except ClientError as ce:
        if ce.response["Error"]["Code"] == "UserNotFoundException":
            logging.error(f"User not found for tax_id: {tax_id}")
            return http_response(status_code=404, body={"message": "User not found."})
        else:
            logging.error(f"AWS ClientError: {str(ce)}")
            return http_response(status_code=500, body={"message": "Internal server error."})
    except Exception as e:
        logging.error(f"Error during authentication: {str(e)}")
        return http_response(status_code=500, body={"message": "Internal server error."})
