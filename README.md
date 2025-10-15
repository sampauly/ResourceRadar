## UPDATE OCTOBER 2025: Resource Radar 2.0 in development 
<img width="1440" height="732" alt="Screenshot 2025-10-15 at 5 25 48 PM" src="https://github.com/user-attachments/assets/1b7bbc2d-df81-4549-bb70-0097a0262de0" />
(only one server currrently available, but supports multi-system monitoring)

## Overview

Resource Radar is a Flask-based web application designed to monitor and visualize real-time metrics for distributed systems. It supports user authentication via Google OAuth, provides role-based access control (RBAC), and includes an admin panel for user management.

## Features

- **Real-time Monitoring**: Visualizes system metrics for distributed systems
- **Historical Data**: Admin-only access to historical performance metrics
- **User Management**: Administrative interface for managing users
- **Authentication**: Secure login via Google OAuth
- **Role-Based Access Control**: Different permission levels for various users
- **Data Visualization**: Interactive charts for metric display

## Project Structure

```
.
├── app/                      # Contains the main application code
│   ├── __init__.py           # Initializes the Flask app, sets up extensions, and registers blueprints
│   ├── admin.py              # Configures Flask-Admin for user management
│   ├── auth.py               # Handles user authentication via Google OAuth
│   ├── data_retrieval.py     # Manages data collection from systems
│   ├── metric_collector.py   # Collects system metrics
│   ├── models.py             # Defines the database schema, including the User model
│   ├── routes.py             # Defines the main application routes
│   ├── tasks.py              # Handles background tasks for data collection
│   ├── static/               # Contains static files (CSS, JavaScript)
│   └── templates/            # Contains HTML templates
├── config.py                 # Stores configuration settings
└── requirements.txt          # Lists project dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+ installed on your system
- SQLite for the database (pre-installed with Python)
- Web browser with JavaScript enabled

### Installation

1. Fork and clone the repository:
   ```bash
   git clone https://gitlab.com/sampauly/cop4521-flask.git
   cd cop4521-flask
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   > **Note**: Use the path to your Python installation if different

3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

### Setting Up Google Authentication

1. Go to Google Cloud Console and create a new project
2. In **APIs & Services > OAuth consent screen**, set up your app with **External** audience
3. Go to **APIs & Services > Credentials** and create a new **OAuth Client ID**
4. Set Application type as **Web Application** and add `http://127.0.0.1:8000/callback` as an Authorized redirect URI
5. Create a `.env` file in the project root with:
   ```
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   SECRET_KEY=unique-flask-app-identifier
   ```
6. Generate a secure SECRET_KEY with:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### Database Setup

Initialize and apply database migrations:
```bash
flask db init
flask db migrate -m "Initial migration" 
flask db upgrade
```

## Running the Application

To run the application with Gunicorn:
```bash
gunicorn --workers 1 --bind unix:/run/flask.sock "app:create_app()"
```

For development purposes:
```bash
flask run --debug
```

## Background Services

The application runs background tasks that:
- Collect system metrics every 10 minutes
- Log data to the SQLite database

## Accessing the Application

- **Dashboard**: Available to all authenticated users
- **Historical Data**: Available to admin users only
- **User Management**: Available to admin users only

## Managing Users via Flask Shell

When you first launch the application, you'll see a "Login with Google" button. After logging in, you may receive an "Unauthorized" message because your email isn't recognized in the database yet.

To manually add the first admin user:

1. Open the Flask shell:
   ```bash
   flask shell
   ```

2. Import the necessary modules:
   ```python
   from app.models import db, User
   ```

3. Create and add a user:
   ```python
   user = User(username="new_username", email="youremail@gmail.com", type="Admin")
   db.session.add(user)
   db.session.commit()
   ```

Once your email is added, Google authentication will verify you, and the app will grant you admin access. To add more users, you can use the "Manage Users" link within the application.

## Images 
<img width="1440" height="732" alt="Screenshot 2025-10-15 at 5 25 25 PM" src="https://github.com/user-attachments/assets/37742827-868e-4878-9737-17ec998f3587" />
<img width="1440" height="732" alt="Screenshot 2025-10-15 at 5 31 03 PM" src="https://github.com/user-attachments/assets/72ac6f02-77c3-4800-bd31-86486215681a" />
<img width="1440" height="732" alt="Screenshot 2025-10-15 at 5 39 49 PM" src="https://github.com/user-attachments/assets/3ed27c32-5f7d-4589-9200-fb722e486574" />
