import os
import json

company_id = '1'
file_companies = open('companies.json', 'r')
obj_companies = json.loads(file_companies.readlines()[0])
company = obj_companies[company_id]

company_dir = './' + company['name']
games_dir = os.path.join(company_dir, 'games')
people_dir = os.path.join(company_dir, 'people')
os.makedirs(people_dir)
os.makedirs(games_dir)
with open(os.path.join(company_dir, company['name']+'.json'), 'w') as f:
    json.dump(company, f, indent=4, sort_keys=True)

developed_games = company['developed_games']
published_games = company['published_games']
people = company['people']

file_games = open('games.json', 'r')
obj_games = json.loads(file_games.readlines()[0])
for game in developed_games:
    game_detailed = obj_games[str(game['id'])]
    name = 'dev-' + str(game_detailed['id']) + '.json'
    with open(os.path.join(games_dir, name), 'w') as f:
        json.dump(game_detailed, f, indent=4, sort_keys=True)

for game in published_games:
    game_detailed = obj_games[str(game['id'])]
    name = 'pub-' + str(game_detailed['id']) + '.json'
    with open(os.path.join(games_dir, name), 'w') as f:
        json.dump(game_detailed, f, indent=4, sort_keys=True)

file_people = open('people.json', 'r')
file_people2 = open('people2.json', 'r')
obj_people = json.loads(file_people.readlines()[0])
obj_people2 = json.loads(file_people2.readlines()[0])
missing = []
for person in people:
    person_detailed = {}
    try:
        person_detailed = obj_people[str(person['id'])]
    except:
        try:
            person_detailed = obj_people2[str(person['id'])]
        except:
            missing.append(str(person['id']))

    if person_detailed != {}:
        with open(os.path.join(people_dir, person['name']+'.json'), 'w') as f:
            json.dump(person_detailed, f, indent=4, sort_keys=True)
print("Missing people: " + str(missing))
