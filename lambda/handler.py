import json


def lambda_handler(event, context):
    body = {
        "message": "Hello from Lambda!",
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
