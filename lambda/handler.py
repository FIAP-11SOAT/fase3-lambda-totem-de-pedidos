import json
import logging

import boto3

from aws_cognito_idp import AuthService
from aws_secrets_manager import get_aws_secrets


def default_handler(event, context):
    body = {
        "message": "Pipeline funcionando com sucesso !",
        "input": event,
        "context_function_name": context.function_name,
        "context_memory_limit_in_mb": context.memory_limit_in_mb,
        "context_invoked_function_arn": context.invoked_function_arn,
        "context_request_id": context.aws_request_id,
        "method": event.get("httpMethod"),
        "path": event.get("path"),
        "headers": event.get("headers"),
        "queryStringParameters": event.get("queryStringParameters"),
        "body": event.get("body"),
        "isBase64Encoded": event.get("isBase64Encoded")
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response


def lambda_handler(event, context):
    cognito_client = boto3.client('cognito-idp')

    secrets = get_aws_secrets("fase3-lambda-totem-de-pedidos-secrets")

    service = AuthService(cognito_client, secrets)

    response = service.authenticate_anonymous()

    logging.info(json.dumps(response, indent=4, default=str))

    return {
        "statusCode": 200,
        "body": json.dumps(secrets)
    }
