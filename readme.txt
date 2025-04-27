steps to setup:
1. create venv 
    /opt/python3/bin/python3.13 -m venv venv
    source venv/bin/activate

2. install requirements: 
    pip install -r requirements

3. run gunicorn 
    gunicorn --workers 1 --bind unix:/run/flask.sock "app:create_app()"

running tests:
1. enter venv
2. in root directory: run python3 -m unittest tests/test_data_retrieval.py
or whatever test i want to run 

Viewing databse:
sqlite3 ./instance/sqlite.db