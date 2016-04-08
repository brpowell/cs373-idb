from flask import send_file, make_response, url_for, jsonify, abort, make_response
from ggmate import app_instance, db
import subprocess, json, os
from ggmate.models import Game, Company, Person

# Routes
@app_instance.route('/', methods=['GET'])
def index():
    return send_file('index.html')

# @app_instance.route('/index.html', methods=['GET'])
# def ss():
#     return send_file('templates/index.html')

# @app_instance.route('/nav.html', methods=['GET'])
# def nav():
#     return send_file('templates/nav.html')

# @app_instance.route('/about.html', methods=['GET'])
# def about():
#     return send_file('templates/about.html')

# @app_instance.route('/companies.html')
# def companies():
#     return send_file('templates/companies.html')

# @app_instance.route('/games.html')
# def games():
#     return send_file('templates/games.html')

# @app_instance.route('/people.html')
# def people():
#     return send_file('templates/people.html')

# @app_instance.route('/home.html')
# def home():
#     return send_file('templates/home.html')

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
    output = subprocess.getoutput('python3 tests.py')
    print(output)
    return json.dumps({'output': str(output)})


# ------------------------------------
# RESTful API
# ------------------------------------

@app_instance.route('/api/games/<int:page>', methods=['GET'])
def get_games(page=1):
    request = Game.query.paginate(page=page, per_page=50)
    games = request.items
    return jsonify({'games': [game.to_json() for game in games] })

@app_instance.route('/api/companies/<int:page>', methods=['GET'])
def get_companies(page=1):
    request = Company.query.paginate(page=page, per_page=50)
    companies = request.items
    return jsonify({'companies': [company.to_json() for company in companies]})

@app_instance.route('/api/people/<int:page>', methods=['GET'])
def get_people(page=1):
    request = Person.query.paginate(page=page, per_page=50)
    people = request.items
    return jsonify({'people': [person.to_json() for person in people]})

@app_instance.route('/api/person/<int:id>', methods=['GET'])
def get_person(id):
    request = Person.query.filter_by(id=id).first()
    if request is None:
        abort(404)
    return jsonify(request.to_json(list_view=True))

@app_instance.route('/api/company/<int:id>', methods=['GET'])
def get_company(id):
    request = Company.query.filter_by(id=id).first()
    if request is None:
        abort(404)
    return jsonify(request.to_json(list_view=True))

@app_instance.route('/api/game/<int:id>', methods=['GET'])
def get_game(id):
    request = Game.query.filter_by(id=id).first()
    if request is None:
        abort(404)
    return jsonify(request.to_json())

@app_instance.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)
