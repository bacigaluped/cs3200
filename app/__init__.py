from flask import Flask
from flask_bootstrap import Bootstrap
from os import environ

app = Flask(__name__)
bootstrap = Bootstrap(app)

aws_user_name = environ.get('AWS_USERNAME')
database_password = environ.get('DB_PASSWORD')
api_key = environ.get('API_KEY')

from app import routes
