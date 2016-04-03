from flask import send_file, make_response, url_for
from app import app_instance, db
import subprocess, json, os
# from models import Game, Company, Person

# Routes
@app_instance.route('/', methods=['GET'])
def index():
    return send_file('templates/index.html')

@app_instance.route('/about', methods=['GET'])
def about():
    return send_file('templates/about.html')

@app_instance.route('/companies')
def companies():
    return send_file('templates/companies.html')

@app_instance.route('/games')
def games():
    return send_file('templates/games.html')

@app_instance.route('/people')
def people():
    return send_file('templates/people.html')

# @app.route('/company/<id>')
# def company(id):
#     company = Company.query.filter_by(company_id=id)
#     return send_file('templates/company.html', company=company)
#
# @app.route('/game/<id>')
# def game():
#     game = Game.query.filter_by(game_id=id)
#     return send_file('templates/game.html', game=game)
#
# @app.route('/person/<id>')
# def person(id):
#     person = Person.query.filter_by(person_id=id)
#     return send_file('templates/person.html')

# Run unittest
@app_instance.route('/run_unittests')
def run_tests():
    print('GOT HERE')
    output = subprocess.getoutput('make test')
    print(output)
    return json.dumps({'output': str(output)})
