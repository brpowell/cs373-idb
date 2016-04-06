from flask import send_file, make_response, url_for, jsonify, abort, make_response
from app import app_instance, db
import subprocess, json, os
# from models import Game, Company, Person

# Routes
@app_instance.route('/', methods=['GET'])
def index():
    return send_file('templates/index.html')

@app_instance.route('/index.html', methods=['GET'])
def ss():
    return send_file('templates/index.html')

@app_instance.route('/nav.html', methods=['GET'])
def nav():
    return send_file('templates/nav.html')

@app_instance.route('/about.html', methods=['GET'])
def about():
    return send_file('templates/about.html')

@app_instance.route('/companies.html')
def companies():
    return send_file('templates/companies.html')

@app_instance.route('/games.html')
def games():
    return send_file('templates/games.html')

@app_instance.route('/people.html')
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
    output = subprocess.getoutput('make test')
    print(output)
    return json.dumps({'output': str(output)})


# ------------------------------------
# RESTful API
# ------------------------------------

games = [
	{
		'id': 1,
		'name': 'Mario Kart'
	},
	{
		'id': 2,
		'name': 'Pokemon'
	}
]

@app_instance.route('/api/games', methods=['GET'])
def get_games():
	return jsonify({'games': games})

@app_instance.route('/api/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
	game = [game for game in games if game['id'] == game_id]
	if len(game) == 0:
		abort(404)
	return jsonify({'games': games[0]})

@app_instance.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)
