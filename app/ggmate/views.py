from flask import send_file, make_response, url_for, jsonify, abort, make_response
from ggmate import app_instance, db
import subprocess, json, os
from ggmate.models import Game, Company, Person

# Routes
@app_instance.route('/', methods=['GET'])
def index():
    return send_file('index.html')

# Run unittest
@app_instance.route('/run_unittests')
def run_tests():
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../tests.py')
    output = subprocess.getoutput('python3 '+path)
    print(output)
    return json.dumps({'output': str(output)})


# ------------
# RESTful API
# ------------
@app_instance.route('/api/games/<int:page>', methods=['GET'])
def get_games(page=1):
    request = Game.query.paginate(page=page, per_page=20)
    games = request.items
    return jsonify({'games': [game.to_json() for game in games] })

@app_instance.route('/api/companies/<int:page>', methods=['GET'])
def get_companies(page=1):
    request = Company.query.paginate(page=page, per_page=20)
    companies = request.items
    return jsonify({'companies': [company.to_json() for company in companies]})

@app_instance.route('/api/people/<int:page>', methods=['GET'])
def get_people(page=1):
    request = Person.query.paginate(page=page, per_page=20)
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
