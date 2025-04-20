steps to setup:
1. create venv 
    /opt/python3/bin/python3.13 -m venv venv
    source venv/bin/activate

2. install requirements: 
    pip install -r requirements

3. run gunicorn 
    gunicorn --workers 3 --bind unix:/run/flask.sock "app:create_app()"