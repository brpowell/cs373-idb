"""

cascade.py
desc: Provide a company and parse data for their related people and games

"""

import os
import json
from json_generator import get_json, save_json

game_set = set()
total_games = 0
# file_companies = open('companies.json', 'r')
# obj_companies = json.loads(file_companies.readlines()[0])

# obj_companies = get_json('./data/base/companies.json')
# company = obj_companies[company_id]
file_games = open('./data/base/games.json', 'r')
obj_games = json.loads(file_games.readlines()[0])
file_people = open('./data/base/people.json', 'r')
file_people2 = open('./data/base/people(FinalPart).json', 'r')
obj_people = json.loads(file_people.readlines()[0])
obj_people2 = json.loads(file_people2.readlines()[0])

company_path = './data/robust-developers'
for company_file in os.listdir(company_path):
    company = get_json(os.path.join(company_path, company_file))
    company_dir = os.path.join('./data/cascade_results', company['name'])
    games_dir = os.path.join(company_dir, 'games')
    people_dir = os.path.join(company_dir, 'people')
    os.makedirs(people_dir)
    os.makedirs(games_dir)
# with open(os.path.join(company_dir, company['name']+'.json'), 'w') as f:
#     json.dump(company, f, indent=4, sort_keys=True)
    developed_games = company['developed_games']
    published_games = company['published_games']
    people = company['people']

    for game in developed_games:
        total_games += 1
        game_set.add(game['id'])
        game_detailed = obj_games[str(game['id'])]
        name = 'dev-' + str(game_detailed['id']) + '.json'
        with open(os.path.join(games_dir, name), 'w') as f:
            json.dump(game_detailed, f, indent=4, sort_keys=True)

    for game in published_games:
        game_detailed = obj_games[str(game['id'])]
        name = 'pub-' + str(game_detailed['id']) + '.json'
        with open(os.path.join(games_dir, name), 'w') as f:
            json.dump(game_detailed, f, indent=4, sort_keys=True)

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

    percent_missing = str(round(len(missing) / len(people) * 100)) + '%'
    print(company['name'] + " - missing people: " + percent_missing)

print(str(total_games) + " total games")
print(str(len(game_set)) + " unique games")
