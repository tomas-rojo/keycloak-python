import os
from keycloak_auth_manager import KeycloakAuthManager


keycloak_manager = KeycloakAuthManager(
    server_url=os.environ["KEYCLOAK_SERVER_URL"],
    realm_name=os.environ["KEYCLOAK_REALM_NAME"],
    client_id=os.environ["KEYCLOAK_CLIENT_ID"],
    client_secret=os.environ["KEYCLOAK_CLIENT_SECRET"],
    redirect_uri=os.environ["REDIRECT_URI"]
)
