"""
Main application routes.
"""
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required
from .models import User, db
from .metric_collector import latest_metrics

main_bp = Blueprint('main', __name__)
api = Blueprint('api', __name__)

@main_bp.route('/')
def index():
    """Render the login page."""
    return render_template('login.html')

@api.route('/api/current_metrics', methods=['GET'])
def current_metrics():
    """ get the latest metrics for each server and return as json """
    try:
        current = latest_metrics()
        return jsonify(current) 
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Render the dashboard page."""
    return render_template('dashboard.html')

@main_bp.route('/unauthorized')
def unauthorized():
    """Render the unauthorized access page."""
    return render_template('unauthorized.html')

@main_bp.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    """Manage user roles."""
    if request.method == 'POST':
        email = request.form.get('email')
        user_type = request.form.get('user_type', 'User')
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                user.type = user_type
            else:
                user = User(username=email.split('@')[0], email=email, type=user_type)
                db.session.add(user)
            db.session.commit()
            flash('User updated successfully.', 'success')
    users = User.query.all()
    return render_template('manage_users.html', users=users)
