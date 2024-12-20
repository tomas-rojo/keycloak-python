from functools import wraps
import logging
from typing import Any

from flask import redirect, session, url_for

from keycloak_auth_manager import KeycloakAuthManager


def role_required(required_roles: list[str], keycloak_manager: KeycloakAuthManager) -> Any:
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_info = session.get('user')
            if not user_info:
                logging.warning("Access denied: No user session found.")
                return redirect(url_for('login'))
            
            # if check_roles(user, required_roles, keycloak_manager):
            if keycloak_manager.validate_user_roles(user_info, required_roles):
                return f(*args, **kwargs)
            else:
                logging.warning("Access denied: Insufficient role permissions.")
                return "403 Forbidden: You do not have access to this resource.", 403
        return wrapper
    return decorator
