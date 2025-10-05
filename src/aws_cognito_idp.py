class AuthService:
    def __init__(self, client, secrets):
        self.client = client
        self.user_pool_id = secrets['COGNITO_USER_POOL_ID']
        self.client_id = secrets['COGNITO_USER_POOL_CLIENT_ID']
        self.default_username = secrets['COGNITO_DEFAULT_USERNAME']
        self.default_password = secrets['COGNITO_DEFAULT_PASSWORD']

    def authenticate_anonymous(self):
        return self._authenticate_user(self.default_username, self.default_password)

    def authenticate_user(self, username):
        return self._authenticate_user(username, self.default_password)

    def _authenticate_user(self, username, password):
        return self.client.admin_initiate_auth(
            UserPoolId=self.user_pool_id,
            ClientId=self.client_id,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

    def register_user(self, cpf, password, name, email):
        response = self.client.admin_create_user(
            UserPoolId=self.user_pool_id,
            Username=cpf,
            TemporaryPassword=password,
            UserAttributes=[
                {'Name': 'name', 'Value': name},
                {'Name': 'email', 'Value': email},
            ],
            MessageAction='SUPPRESS'
        )
        self.client.admin_set_user_password(
            UserPoolId=self.user_pool_id,
            Username=cpf,
            Password=password,
            Permanent=True
        )
        return response

    def search_user_by_cpf(self, cpf):
        response = self.client.list_users(
            UserPoolId=self.user_pool_id,
            Filter=f'username = "{cpf}"'
        )
        if user := response.get('Users'):
            return user[0]
        return None
