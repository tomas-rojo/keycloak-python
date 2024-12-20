from keycloak_auth_manager import KeycloakAuthManager


keycloak_manager = KeycloakAuthManager(
    server_url='http://localhost:8180',
    realm_name='myapp',
    client_id='my-client',
    client_secret='MbhTDHXDFe9zIBRy9BjHZ0C0krBMZMKc',
    redirect_uri='http://127.0.0.1:5000/callback'
)
