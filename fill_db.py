import os
import json, re
from app import db, app_instance
from app.models import Company, Person, Game, Platform, Rating
from datetime import datetime
from dateutil import parser
import time
import requests

pattern = re.compile('([^\s\w]|_)+')
start_time = time.time()
metacritic_base = '../ggmate-sub/scrape/data/base/gamesData'
games_base = '../ggmate-sub/scrape/data/base/games.json'
companies_base = '../ggmate-sub/scrape/data/base/companies.json'
data = {}
cache = []


with open(games_base, 'r') as games_file:
    games_json = json.loads(games_file.readlines()[0])
print('games.json loaded')

with open(companies_base, 'r') as companies_file:
    companies_json = json.loads(companies_file.readlines()[0])
print('companies.json loaded')

def search_companies(metacritic_company):
    fields = ['name', 'deck', 'date_founded', 'location_city', 'location_country', \
            'image']
    final = ''
    metacritic_company = pattern.sub(',', metacritic_company).lower().split(',')
    headers = {'User-Agent': 'Briz'}
    api_key = '815286655381701f108ee3c2cb907efa84dbfc28'
    fallback_url = 'http://www.giantbomb.com/api/search/?api_key=%s& \
                    format=json&resources=company&query=%s' % (api_key, metacritic_company)
    for id, company in companies_json.items():
        c_values = pattern.sub(',', company['name']).lower().split(',')
        got_it = False
        if all(term in c_values for term in metacritic_company):
            # if metacritic_company in c_values:
            final = companies_json[id]
            print('matched!')
            break
        else:
            r = requests.get(fallback_url, headers=headers)
            parsed = r.json()
            # print(parsed)
            try:
                final = parsed['results'][0]
            except:
                return -1
            break
    try:
        final['date_founded'] = parser.parse(final['date_founded'])
    except:
        final['date_founded'] = parser.parse('1-1-1900')
    for field in fields:
        if final[field] == None:
            final[field] = ''
    return final



# load metacritic games for each console
for f in os.listdir(metacritic_base):
    if f.endswith(".json"):
        with open(os.path.join(metacritic_base, f)) as src:
            short = f.split('.')[0].upper()
            data[short] = json.loads(src.readlines()[0])
print('metacritic games loaded')

# Add metacritic games, platforms and ratings
for console, games in data.items():
    # print(console + " count: " + str(len(games)))

    # Choose any game to pull the full name of current platform
    some_key = next(iter(games))
    full_name = games[some_key]['platforms'][0]

    p = Platform(name=full_name, short=console)
    db.session.add(p)
    db.session.commit()
    for key, game in games.items():
        publishers = []
        developers = []
        for publisher in game['publishers']:
            d = search_companies(publisher)
            if d == -1:
                continue
            c = Company(name=publisher, deck=d['deck'], city=d['location_city'],\
                    country=d['location_country'], date_founded=d['date_founded'],\
                    image=d['image']['medium_url'])
            publishers.append(c)
        for developer in game['developers']:
            d = search_companies(developer)
            if d == -1:
                continue
            c = Company(name=developer, deck=d['deck'], city=d['location_city'],\
                    country=d['location_country'], date_founded=d['date_founded'],\
                    image=d['image']['medium_url'])
            developers.append(c)
        db.session.add_all(publishers)
        db.session.add_all(developers)
        db.session.commit()
        print('Companies added')
        g = 0
        if game['gameName'] not in cache:
            try:
                release = parser.parse(game['dataPublished'])
            except:
                release = parser.parse('1-1-1900')
            g = Game(name=game['gameName'], release_date=release, \
                    deck=game['description'], content_rating=game['contentRating'],
                    genre=game['genre'])
            cache.append(game['gameName'])
            db.session.add(g)
            db.session.commit()
        else:
            g = Game.query.filter_by(name=game['gameName']).first()
            # print('Fetched duplicate game: ' + str(g))

        value = game['ratingValue']
        if value != '':
            value = int(value)
            r = Rating(game_id=g.id, platform_id=p.id, metacritic=value)
            db.session.add(r)

        g.platforms.append(p)
        db.session.add(g)
        db.session.commit()
        print(str(g) + ' committed')        # KEEP, EXECUTION HANGS OTHERWISE...

print("--- %s seconds ---" % (time.time() - start_time))
