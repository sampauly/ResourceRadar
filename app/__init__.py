"""
Initialize the Flask application, configure extensions, and register blueprints.
"""
from flask import Flask
from config import Config
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from flask_migrate import Migrate
from .models import db, User
from .routes import main_bp
from .auth import auth_bp
from .admin import init_admin
from flask_apscheduler import APScheduler
from .data_retrieval import schedule_logging

migrate = Migrate()
login_manager = LoginManager()
oauth = OAuth()
scheduler = APScheduler()

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id))

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    login_manager.init_app(app)
    oauth.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    init_admin(app)
    scheduler.init_app(app)

    # start scheduler
    scheduler.start()
    
    # Configure OAuth provider
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        access_token_url='https://oauth2.googleapis.com/token',
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )
    
    with app.app_context():
        db.create_all()
        schedule_logging(scheduler)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    return app