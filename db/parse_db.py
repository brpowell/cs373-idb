import os
import json, re
from ggmate import db, app_instance
from ggmate.models import Company, Person, Game, Platform
from datetime import datetime
from dateutil import parser
import time
import requests

pattern = re.compile('([^\s\w]|_)+')
base = '../../ggmate-sub/scrape/data/base'
metacritic_base = '../../ggmate-sub/scrape/data/base/gamesData'
games_base = '../../ggmate-sub/scrape/data/base/games.json'
companies_base = '../../ggmate-sub/scrape/data/base/companies.json'
data = {}
cache = []
fields = ['name', 'image', 'deck', 'original_release_date', 'original_game_rating', 'genres']
platform_cache = []
company_cache = []
person_cache = []
game_cache = []

db.session.commit()
start_time = time.time()
with open(os.path.join(base, 'games.json'), 'r') as games_file:
    games_json = json.loads(games_file.readlines()[0])
print('games.json loaded')

with open(os.path.join(base, 'gamesUpdate.json'), 'r') as games_file:
    games_updated_json = json.loads(games_file.readlines()[0])
print('gamesUpdated.json loaded')

with open(os.path.join(base, 'companies.json'), 'r') as companies_file:
    companies_json = json.loads(companies_file.readlines()[0])
print('companies.json loaded')

with open(os.path.join(base, 'people.json'), 'r') as people_file:
    people_json = json.loads(people_file.readlines()[0])
print('people.json loaded')

# for id, game in games_json.items():
#     try:
#         release = parser.parse(game['original_release_date'])
#     except:
#         release = parser.parse('1-1-1900')
#     try:
#         genre = game['genres'][0]['name']
#     except:
#         genre = 'No genre'
#     rating = game['original_game_rating']
#     image = game['image']
#     if image:
#         image = image['medium_url']
#     else:
#         image = 'https://s3.amazonaws.com/clarityfm-production/attachments/1354/default/Objects-Joystick-icon.png?1401047397'
#     if rating:
#         rating = rating[0]['name'].replace('ESRB: ', '')
#     else:
#         rating = 'No Rating'
#     g = Game(name=game['name'], deck=game['deck'], image=image, \
#         release_date=release, content_rating=rating, genre=genre)
#     if game['platforms']:
#         for platform in game['platforms']:
#             p = 0
#             if platform['id'] not in platform_cache:
#                 p = Platform(name=platform['name'], short=platform['abbreviation'])
#             else:
#                 p = Platform.query.filter_by(id=platform['id']).first()
#             g.platforms.append(p)
#             db.session.add(p)
#             print(p)
#     db.session.add(g)
#     print(g)
# db.session.commit()
# print('Games Committed')
def just_companies():
    for f in os.listdir('../../ggmate-sub/scrape/data/robust-developers'):
        company = companies_json[f.split('.')[0]]
        c = 0
        try:
            founded = parser.parse(company['date_founded'])
        except:
            founded = parser.parse('1-1-1900')
        image = company['image']
        if image:
            image = image['medium_url']
        else:
            image = 'http://icons.iconarchive.com/icons/custom-icon-design/mono-business/256/company-building-icon.png'
        c = Company(name=company['name'], image=image,\
            city=company['location_city'], country=company['location_country'],\
            deck=company['deck'], date_founded=founded)
        db.session.add(c)
        print(c)
    db.session.commit()
    print('Companies Committed')

def just_platforms():
    with open('../../ggmate-sub/scrape/data/base/platforms.json', 'r') as f:
        platforms_json = json.loads(f.readlines()[0])
    platforms_list = platforms_json['results']
    for platform in platforms_list:
        p = Platform(name=platform['name'], short=platform['abbreviation'])
        db.session.add(p)
    db.session.commit()

def just_dev_games():
    for f in os.listdir('../../ggmate-sub/scrape/data/robust-developers'):
        company = companies_json[f.split('.')[0]]
        c = Company.query.filter_by(name=company['name']).first()
        for game in company['developed_games']:
            try:
                details = games_updated_json[str(game['id'])]
            except KeyError:
                details = games_json[str(game['id'])]
            except:
                break
            try:
                release = parser.parse(details['release_date'])
            except:
                release = parser.parse('1-1-1900')
            # try:
            #     genre = details['genres'][0]['name']
            # except:
            #     genre = 'No genre'
            # rating = details['original_game_rating']
            image = details['image']
            if image:
                image = image['medium_url']
            else:
                image = 'https://s3.amazonaws.com/clarityfm-production/attachments/1354/default/Objects-Joystick-icon.png?1401047397'
            # if rating:
            #     rating = rating[0]['name'].replace('ESRB: ', '')
            # else:
            #     rating = 'No Rating'
            g = Game(name=details['name'], deck=details['deck'], image=image, \
                release_date=release)
            if details['platforms']:
                for platform in details['platforms']:
                    p = Platform.query.filter_by(short=platform['abbreviation']).first()
                    g.platforms.append(p)
            db.session.add(g)
            c.developed_games.append(g)
            print(g)
        db.session.commit()

def just_pub_games():
    for f in os.listdir('../../ggmate-sub/scrape/data/robust-developers'):
        company = companies_json[f.split('.')[0]]
        c = Company.query.filter_by(name=company['name']).first()
        for game in company['published_games']:
            g = Game.query.filter_by(name=game['name']).first()
            if g is None:
                try:
                    details = games_updated_json[str(game['id'])]
                except KeyError:
                    details = games_json[str(game['id'])]
                except:
                    break
                try:
                    release = parser.parse(details['original_release_date'])
                except:
                    release = parser.parse('1-1-1900')
                # try:
                #     genre = details['genres'][0]['name']
                # except:
                #     genre = 'No genre'
                # rating = details['original_game_rating']
                image = details['image']
                if image:
                    image = image['medium_url']
                else:
                    image = 'https://s3.amazonaws.com/clarityfm-production/attachments/1354/default/Objects-Joystick-icon.png?1401047397'
                # if rating:
                #     rating = rating[0]['name'].replace('ESRB: ', '')
                # else:
                #     rating = 'No Rating'
                g = Game(name=details['name'], deck=details['deck'], image=image, \
                    release_date=release)
                if details['platforms']:
                    for platform in details['platforms']:
                        p = Platform.query.filter_by(short=platform['abbreviation']).first()
                        g.platforms.append(p)
                db.session.add(g)
            c.published_games.append(g)
            print(g)
        db.session.commit()

def just_people():
    for f in os.listdir('../../ggmate-sub/scrape/data/robust-developers'):
        company = companies_json[f.split('.')[0]]
        c = Company.query.filter_by(name=company['name']).first()
        for game in company['developed_games']:
            g = Game.query.filter_by(name=game['name']).first()
            print('fetch %s', str(g))
            g_p = games_json[str(game['id'])]
            if g_p['people']:
                for person in g_p['people']:
                    p = Person.query.filter_by(id=person['id']).first()
                    if p is None:
                        details = people_json[str(person['id'])]
                        try:
                            birth = parser.parse(person['birth_date'])
                        except:
                            birth = parser.parse('1-1-1900')
                        try:
                            death = parser.parse(person['death_date'])
                        except:
                            death = parser.parse('1-1-1900')
                        if not details['country']:
                            details['country'] = ''
                        if not details['hometown']:
                            details['hometown'] = ''
                        if not details['deck']:
                            details['deck'] = 'Worked on ' + g.name
                        p = Person(id=person['id'], name=details['name'], birth_date=birth, death_date=death,\
                            country=details['country'], hometown=details['hometown'], deck=details['deck'])
                        db.session.add(p)
                    g.people.append(p)
                    c.people.append(p)
                    db.session.add(g)
                    db.session.add(c)
                    print(p)
        db.session.commit()

# just_companies()
# just_platforms()
# just_dev_games()
# just_pub_games()
just_people()

print("--- %s seconds ---" % (time.time() - start_time))
