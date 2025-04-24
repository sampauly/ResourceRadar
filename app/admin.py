"""
Initialize Flask-Admin and configure models.
"""
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import db, User

admin = Admin()

def init_admin(app):
    """Initialize the admin interface."""
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session, name='Users'))