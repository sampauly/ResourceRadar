"""
Authentication routes for login, logout, and OAuth callback.
"""
from flask import Blueprint, redirect, url_for, current_app
from flask_login import login_user, logout_user
from .models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    """Redirect user to Google OAuth login."""
    redirect_uri = url_for('auth.callback', _external=True)
    return current_app.extensions['authlib.integrations.flask_client'].google.authorize_redirect(redirect_uri)

@auth_bp.route('/callback')
def callback():
    """Handle OAuth callback and log in the user."""
    token = current_app.extensions['authlib.integrations.flask_client'].google.authorize_access_token()
    user_info = token.get('userinfo')
    email = user_info['email']

    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect(url_for('main.unauthorized'))

    login_user(user)
    return redirect(url_for('main.dashboard'))

@auth_bp.route('/logout')
def logout():
    """Log out the user."""
    logout_user()
    return redirect(url_for('main.index'))
