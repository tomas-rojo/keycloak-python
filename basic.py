from flask import Blueprint

from roles import role_required
from keycloak_client import keycloak_manager


bp = Blueprint("basic", __name__, url_prefix='/basic')

@bp.get('/')
@role_required(['basic'], keycloak_manager)
def user_page():
    return "Welcome to the Basic page!"
