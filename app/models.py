"""
Database models for the application.
"""
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User model for authentication and role management."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False, default='User')  # 'Admin' or 'User'

class MetricLogs(db.Model):
    """Model to store metrics logged from machines via Netdata API."""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    machine_name = db.Column(db.String(45), nullable=False)
    cpu_usage = db.Column(db.Float, nullable=True)
    memory_usage = db.Column(db.Float, nullable=True)
    disk_usage = db.Column(db.Float, nullable=True)
    network_usage = db.Column(db.Float, nullable=True)

