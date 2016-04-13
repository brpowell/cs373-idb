# app module
# Responsible for creating the app instance and initializing the database

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

# Create an app instance defined by config_name
app_instance = Flask(__name__, static_url_path='')
app_instance.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app_instance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_instance.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('GGMATE_DB')
db = SQLAlchemy(app_instance)

import ggmate.views
