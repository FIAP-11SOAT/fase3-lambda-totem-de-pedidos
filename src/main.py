import boto3

from aws_cognito_idp import AuthService
from aws_secrets_manager import get_aws_secrets


def main():
    cognito_client = boto3.client('cognito-idp')

    secrets = get_aws_secrets("fase3-lambda-totem-de-pedidos-secrets")

    service = AuthService(cognito_client, secrets)

    # result = service.register_user(
    #     email="teteuoliveira12@gmail.com",
    #     password="Testando@12345",
    #     name="Matheus Oliveira Fernandes Ribeiro",
    #     cpf="14756424740"
    # )

    # result = service.authenticate_user(
    #     username="14756424740",
    #     password="Testando@12345"
    # )

    # response = service.authenticate_user("00000000000")
    # print(response)

    # result = service.search_user_by_cpf("00000000000a")
    # print(result)

    result = service.register_user('14756424740', 'Matheus Oliveira', 'teteuoliveira12@gmail.com')
    print(result)


if __name__ == '__main__':
    main()
