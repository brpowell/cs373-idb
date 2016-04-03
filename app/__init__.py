# app module
# Responsible for creating the app instance and initializing the database

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app_instance = Flask(__name__)
app_instance.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app_instance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_instance.config['SQLALCHEMY_DATABASE_URI'] = \
    '{engine}://{username}:{password}@{host}:{port}/{database}'.format(
        engine='mysql+pymysql',
        username=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        host=os.getenv('MYSQL_HOST'),
        port=os.getenv('MYSQL_PORT'),
        database=os.getenv('MYSQL_DATABASE'))

db = SQLAlchemy(app_instance)

import app.views
