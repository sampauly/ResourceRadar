"""
Initialize Flask-Admin and configure models.
"""
from functools import wraps
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from .models import db, User

admin = Admin()

def init_admin(app):
    """Initialize the admin interface."""
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session, name='Users'))

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.type == 'Admin':
            return f(*args, **kwargs)
        else:
            return redirect(url_for('main.unauthorized'))
    return decorated_function
