# Resource Radar

## Overview

Resource Radar is a Flask-based web application designed to help users efficiently manage and track resources. It supports user authentication via Google OAuth and provides an admin panel for managing users. This guide is designed for beginners, particularly undergraduate students, and explains each module in detail.

## Project Structure

```
resource_radar/
├── LICENSE
├── README.md
├── app
│   ├── __init__.py
│   ├── admin.py
│   ├── auth.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/dashboard.js
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── login.html
│       ├── manage_users.html
│       └── unauthorized.html
├── config.py
├── pyproject.toml
├── requirements.txt
├── run.py
```

## Files and Directories

- `app`: Contains the main application code.
  - `__init__.py`: Initializes the Flask app, sets up extensions, and registers blueprints.
  - `admin.py`: Configures Flask-Admin, which provides an admin interface for managing users.
  - `auth.py`: Handles user authentication via Google OAuth, including login and logout routes.
  - `models.py`: Defines the database schema, including the `User` model.
  - `routes.py`: Defines the main application routes, such as the dashboard and user management views.
  - `static/`: Contains static files such as CSS and JavaScript for styling and interactivity.
  - `templates/`: Contains HTML templates used to render pages dynamically.
- `config.py`: Stores configuration settings such as database URI and authentication credentials.
- `requirements.txt`: Lists the dependencies required to run the project.
- `run.py`: Entry point for running the Flask application.

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/resource_radar.git
   ```
2. Navigate to the project directory:
   ```bash
   cd resource_radar
   ```
3. Create a virtual environment:
   ```bash
   /opt/python3/bin/python3.13 -m venv venv
   source venv/bin/activate
   ```
   `/opt/bin/python3.13` is the python you have installed in your server. However, you might have python installed at another location in your own computer, so specify python accordingly.

4. Install pip using ensurepip (if you don't have pip already installed)
   ```bash
   /opt/bin/python3.13 -m ensurepip
   ```
   
6. Install dependencies:
   ```bash
   /opt/bin/python3.13 -m pip install -r requirements.txt
   ```

## Setting Up Google Authentication Credentials

To enable Google authentication:

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project. You can do this from top left where it says **Select a Project.** If you already have a project, your project name will be in place of **Select a Project.**
3. In **APIs & Services > Oauth consent screen** setup the details of your app. Make sure you set your **Audience** as **External**.
4. Go to **APIs & Services > Credentials** and click on Create credentials, and create **OAuth Client ID**.
5. Make sure the Application type is **Web Application** and the Authorized redirect URIs is set as ```http://127.0.0.1:8000/callback```
6. This creates an Oauth2.0 application, which you can open to see the **Client ID** and **Client Secret**.
7. Create a `.env` file in the project root (the base project folder) and add following credentials. Make sure you replace your-client-id and your-client-secret with the keys given by Oauth2.0.
   ```bash
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

## Database Migrations

Since the project uses Flask-Migrate, you need to initialize and apply database migrations when making changes to the schema.

1. Initialize migrations (only needed the first time):
   ```bash
   flask db init
   ```
2. Generate a migration script whenever the database schema changes:
   ```bash
   flask db migrate -m "Describe changes here"
   ```
3. Apply the migration to update the database:
   ```bash
   flask db upgrade
   ```

## Usage

To run the application, execute:

```bash
python run.py
```
Open the link shown in the terminal (usually http://127.0.0.1:8000) to see your Flask app.
If it's running on a different port (e.g. http://localhost:5000), make sure your callback URL matches it, like http://localhost:5000/callback.

Also, add https://yourwebsite.me/callback to the callback list so it works online too.

## Managing Users via Flask Shell
Now you’ll see a Login with Google button.
If you log in, you’ll probably get an Unauthorized message.
That’s because your app doesn’t know who you are yet—your email isn’t in the database.

To manually add a user to the database, in your terminal:

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
Once your email is added, Google verifies you, and the app lets you in as admin.
To add more users, just use the Manage Users link in the app.
## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or suggestions, open an issue or contact the project maintainer at [prms.regmi@gmail.com](mailto\:prms.regmi@gmail.com).
