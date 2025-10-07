import json
import logging

import boto3

from src.aws_cognito_idp import AuthService
from src.aws_secrets_manager import get_aws_secrets
from src.exceptions import HttpException
from src.get_auth_use_case import get_auth_use_case
from src.http_response import http_response
from src.post_auth_ser_case import post_auth_use_case


def lambda_handler(event, context):
    logging.getLogger().setLevel(logging.INFO)

    cognito_client = boto3.client('cognito-idp')

    secrets = get_aws_secrets("fase3-lambda-totem-de-pedidos-secrets")

    service = AuthService(cognito_client, secrets)

    method = event.get("requestContext", {}).get("http", {}).get("method")

    if method == "OPTIONS":
        return http_response(200, {"message": "CORS preflight check successful"})

    try:
        if method == "GET":
            query = event.get("queryStringParameters", {})
            return get_auth_use_case(service=service, query=query)

        if method == "POST":
            body = json.loads(event.get("body", "{}"))
            return post_auth_use_case(service=service, data=body)

    except HttpException as e:
        return http_response(e.status_code, {"message": e.message})

    return http_response(status_code=404, body={"message": "Not Found"})
