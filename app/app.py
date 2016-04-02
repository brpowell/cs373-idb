from flask import Flask, render_template, send_file
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager, Server
import subprocess
from flask.ext.migrate import Migrate, MigrateCommand

SQLALCHEMY_DATABASE_URI = \
    '{engine}://{username}:{password}@{host}:{port}/{database}'.format(
        engine='mysql+pymysql',
        username=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        host=os.getenv('MYSQL_HOST'),
        port=os.getenv('MYSQL_PORT'),
        database=os.getenv('MYSQL_DATABASE'))


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db  # <-- this needs to be placed after app is created
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host="0.0.0.0", use_debugger=True))

db = SQLAlchemy(app)


# Routes
@app.route('/index.html')
@app.route('/')
def index():
    return send_file('templates/index.html')

@app.route('/about.html')
def about():
    return send_file('templates/about.html')

@app.route('/companies.html')
def companies():
    return send_file('templates/companies.html')

@app.route('/company.html')
def company():
    return send_file('templates/company.html')

<<<<<<< HEAD
@app.route('/company1.html')
def company1():
    return send_file('templates/company1.html')

@app.route('/company2.html')
def company2():
    return send_file('templates/company2.html')

@app.route('/company3.html')
def company3():
    return send_file('templates/company3.html')    

@app.route('/game.html')
def game1():
    return send_file('templates/game.html')

@app.route('/game2.html')
def game2():
    return send_file('templates/game2.html')

@app.route('/game3.html')
def game3():
    return send_file('templates/game3.html')

@app.route('/games.html')
def games():
    return send_file('templates/games.html')

@app.route('/people.html')
def people():
    return send_file('templates/people.html')

@app.route('/person.html')
def person1():
    return send_file('templates/person.html')

# Run unittest
@app.route('/run_unittests')
def run_tests():
    output = subprocess.getoutput("make test")
    return json.dumps({'output': str(output)})


if __name__ == "__main__":
    manager.run()
