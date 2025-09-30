import json

import boto3


def get_aws_secrets(secret_name):
    client = boto3.client('secretsmanager')
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise e
    else:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
