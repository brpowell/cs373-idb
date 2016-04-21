# ------------------
# Init application
# ------------------
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app_instance = Flask(__name__, static_url_path='')
app_instance.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app_instance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_instance.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('GGMATE_DB')

db = SQLAlchemy(app_instance)

import ggmate
