import requests
import logging
from typing import Optional, Dict, List


class KeycloakAuthManager:
    def __init__(self, server_url, realm_name, client_id, client_secret, redirect_uri) -> None:
        self.server_url = server_url
        self.realm_name = realm_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorize_url(self) -> str:
        authorize_url = f"{self.server_url}/realms/{self.realm_name}/protocol/openid-connect/auth"
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'openid profile email roles'
        }
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        return f"{authorize_url}?{query_string}"

    def exchange_code_for_tokens(self, code: str) -> Dict:
        token_endpoint = f"{self.server_url}/realms/{self.realm_name}/protocol/openid-connect/token"
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(token_endpoint, data=payload)
        response.raise_for_status()
        return response.json()

    def get_user_info(self, access_token: str) -> Dict:
        userinfo_endpoint = f"{self.server_url}/realms/{self.realm_name}/protocol/openid-connect/userinfo"
        headers = {'Authorization': f"Bearer {access_token}"}
        response = requests.get(userinfo_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def handle_callback(self, code: str) -> Optional[Dict]:
        token_data = self.exchange_code_for_tokens(code)
        userinfo = {}
        if 'access_token' in token_data:
            access_token = token_data['access_token']
            userinfo = self.get_user_info(access_token)
        
        try:
            userinfo['access_token'] = access_token
            userinfo['roles'] = self.get_roles(userinfo)
            userinfo['id_token'] = token_data.get('id_token') or ""
            userinfo['refresh_token'] = token_data.get('refresh_token') or ""
            return userinfo
        except Exception as e:
            logging.error(f"Failed to handle callback: {e}")
            return None

    def logout(self, id_token: str) -> None:
        end_session_endpoint = f"{self.server_url}/realms/{self.realm_name}/protocol/openid-connect/logout"
        redirect_uri = 'http://127.0.0.1:5000/login'
        params = {
            'id_token_hint': id_token,
            'post_logout_redirect_uri': redirect_uri
        }
        response = requests.get(end_session_endpoint, params=params, timeout=5)
        response.raise_for_status()


    def validate_user_roles(self, user_info: Dict, required_roles: List[str]) -> bool:
            user_roles = self.get_roles(user_info)
            return any(role in user_roles for role in required_roles)

    def get_roles(self, userinfo) -> list[str]:
        try:
            return userinfo["resource_access"][self.client_id]["roles"]
        except Exception:
            return []
