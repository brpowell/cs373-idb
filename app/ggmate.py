from loader import app_instance, db
from flask import send_file, make_response, url_for, jsonify, abort, \
                    make_response, request, redirect
from models import Game, Company, Person
from sqlalchemy_searchable import parse_search_query
from sqlalchemy_searchable import search
import requests


# ------------------
# Views
# ------------------


@app_instance.route('/', methods=['GET'])
def index():
    return send_file('index.html')

@app_instance.route('/run_unittests')
def run_tests():
    from subprocess import getoutput
    from os import path
    p = path.join(path.dirname(path.realpath(__file__)), 'tests.py')
    output = getoutput('python '+p)
    print(output)
    return jsonify({'output': str(output)})

@app_instance.route('/lucky')
def lucky():
    from random import randint
    rnd = randint(0, 2)
    if rnd == 0:
        query = Game.query.all()
        model_id = query[randint(0, len(query) - 1)].id
        model_text = 'game'
    elif rnd == 1:
        query = Company.query.all()
        model_id = query[randint(0, len(query) - 1)].id
        model_text = 'company'
    elif rnd == 2:
        query = Person.query.all()
        model_id = query[randint(0, len(query) - 1)].id
        model_text = 'person'
    return redirect('/#/'+model_text+'/'+str(model_id))


# ------------
# RESTful API
# ------------

@app_instance.route('/search')
def search():
    search_text = request.args.get('searchbar', '')
    game_query = Game.query.search(search_text).limit(15)
    company_query = Company.query.search(search_text).limit(15)
    person_query = Person.query.search(search_text).limit(15)
    results = {
        'games': [x.to_json() for x in game_query.all()],
        'companies': [x.to_json() for x in company_query.all()],
        'people': [x.to_json() for x in person_query.all()]
    }
    return jsonify(results)

@app_instance.route('/api/games/<int:page>', methods=['GET'])
@app_instance.route('/api/games', methods=['GET'])
def get_games(page=1):
    request = Game.query.paginate(page=page, per_page=25)
    games = request.items
    return jsonify({'games': [game.to_json() for game in games] })

@app_instance.route('/api/companies/<int:page>', methods=['GET'])
@app_instance.route('/api/companies', methods=['GET'])
def get_companies(page=1):
    request = Company.query.paginate(page=page, per_page=25)
    companies = request.items
    return jsonify({'companies': [company.to_json() for company in companies]})

@app_instance.route('/api/people/<int:page>', methods=['GET'])
@app_instance.route('/api/people', methods=['GET'])
def get_people(page=1):
    request = Person.query.paginate(page=page, per_page=25)
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

@app_instance.route('/books', methods=['GET'])
def get_books_data():
    headers = {'User-Agent' : 'GGMATE'}
    r = requests.get('http://ibdb.me/api/books', headers=headers)
    return jsonify({'books' : r.json()})

@app_instance.route('/authors', methods=['GET'])
def get_authors_data():
    headers = {'User-Agent' : 'GGMATE'}
    r = requests.get('http://ibdb.me/api/authors', headers=headers)
    return jsonify({'authors' : r.json()})


@app_instance.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)
