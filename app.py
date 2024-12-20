from flask import Flask, redirect, url_for, session, request, render_template
import requests
import logging
from keycloak_client import keycloak_manager
from roles import role_required
from basic import bp

app = Flask(__name__)
app.register_blueprint(bp)
app.secret_key = '123456'

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    if 'user' in session:
        return render_template('home.html', username=session["user"]["preferred_username"])
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return redirect(keycloak_manager.get_authorize_url())

@app.route('/callback')
def callback():
    code = request.args.get('code')
    userinfo = keycloak_manager.handle_callback(code)
    if userinfo:
        session['user'] = userinfo
        logging.debug("User logged in successfully.")
        return redirect(url_for('index'))
    else:
        return "Failed to authenticate with Keycloak."

@app.route('/logout')
def logout():
    logging.debug('Attempting to logout...')
    try:
        id_token = session.get('user', {}).get('id_token')
        if id_token:
            keycloak_manager.logout(id_token)
        session.clear()
        return redirect(url_for('login'))
    except requests.exceptions.RequestException as e:
        logging.error(f"Exception during logout: {e}")
        return "Failed to logout. Please try again."


@app.route('/admin')
@role_required(['admin'], keycloak_manager)
def admin_page():
    return "Welcome to the admin page!"


if __name__ == '__main__':
    app.run(debug=True)
