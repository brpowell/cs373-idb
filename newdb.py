import os
import json, re
from app import db, app_instance
from app.models import Company, Person, Game, Platform, Rating
from datetime import datetime
from dateutil import parser
import time
import requests

pattern = re.compile('([^\s\w]|_)+')
base = '../ggmate-sub/scrape/data/base'
metacritic_base = '../ggmate-sub/scrape/data/base/gamesData'
games_base = '../ggmate-sub/scrape/data/base/games.json'
companies_base = '../ggmate-sub/scrape/data/base/companies.json'
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
    for f in os.listdir('../ggmate-sub/scrape/data/robust-developers'):
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
    with open('../ggmate-sub/scrape/data/base/platforms.json', 'r') as f:
        platforms_json = json.loads(f.readlines()[0])
    platforms_list = platforms_json['results']
    for platform in platforms_list:
        p = Platform(name=platform['name'], short=platform['abbreviation'])
        db.session.add(p)
    db.session.commit()

def just_dev_games():
    for f in os.listdir('../ggmate-sub/scrape/data/robust-developers'):
        company = companies_json[f.split('.')[0]]
        c = Company.query.filter_by(name=company['name']).first()
        for game in company['developed_games']:
            try:
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
            c.developed_games.append(g)
            print(g)
        db.session.commit()

def just_pub_games():
    for f in os.listdir('../ggmate-sub/scrape/data/robust-developers'):
        company = companies_json[f.split('.')[0]]
        c = Company.query.filter_by(name=company['name']).first()
        for game in company['published_games']:
            g = Game.query.filter_by(name=game['name']).first()
            if g is None:
                try:
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
    for f in os.listdir('../ggmate-sub/scrape/data/robust-developers'):
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

just_people()

#         print
    # c = 0
    # try:
    #     founded = parser.parse(company['date_founded'])
    # except:
    #     founded = parser.parse('1-1-1900')
    # image = company['image']
    # if image:
    #     image = image['medium_url']
    # else:
    #     image = 'http://icons.iconarchive.com/icons/custom-icon-design/mono-business/256/company-building-icon.png'
    # c = Company(name=company['name'], image=image,\
    #     city=company['location_city'], country=company['location_country'],\
    #     deck=company['deck'], date_founded=founded)
    # db.session.add(c)
    # print(c)
# db.session.commit()
# print('Companies Committed')

# for id, person in people_json.items():
#     p = 0
#     try:
#         birth = parser.parse(person['birth_date'])
#     except:
#         birth = parser.parse('1-1-1900')
#     try:
#         death = parser.parse(person['death_date'])
#     except:
#         death = parser.parse('1-1-1900')
#     # if person['first_credited_game']['id'] not in game_cache:
#
#     p = Person(name=person['name'], hometown=person['hometown'], country=person['country'],\
#                 deck=person['deck'], birth_date=birth, death_date=death)
#     db.session.add(p)
#     print(p)
# db.session.commit()
# print('People Committed')

# for id, game in games_json:
#     all = True
#     g = 0
#     for field in fields:
#         if game[field] == '' or game[field] is None:
#             all = False
#             break
#     if all:
#         release = parser.parse(game['original_release_date'])
#         genre = game['genres'][0]['name'].replace('ESRB: ', '')
#         g = Game(name=game['name'], deck=game['deck'], image=game['image']['medium_url'], \
#             release_date=release, content_rating=game['original_game_rating'], \
#             genre=genre)
#         for platform in game['platforms']:
#             p = 0
#             if platform['abbreviation'] not in platform_cache:
#                 p = Platform(name=platform['name'], short=platform['abbreviation'])
#                 db.session.add(p)
#             else:
#                 p = Platform.query.filter_by(name=platform['name']).first()
#             g.platforms.append(p)
#         for developer in game['developers']:
#             c = 0
#             dev_details = companies[developer['id']]
#             if developer['name'] not in company_cache:
#                 try:
#                     founded = parser.parse(developer['date_founded'])
#                 except:
#                     founded = parser.parse('1-1-1900')
#                 c = Company(name=developer['name'], image=developer['image']['medium_url'],\
#                     city=developer['location_city'], country=developer['location_country'],\
#                     deck=developer['deck'])
#                 company_cache.append(c)
#                 db.session.add(c)
#             else:
#                 c = Company.query.filter_by(name=developer['name']).first()
#             c.developed_games.append(g)
#             db.session.add(c)
#         for publisher in game['publishers']:
#             c = 0
#             dev_details = companies[publisher['id']]
#             if publisher['name'] not in company_cache:
#                 try:
#                     founded = parser.parse(publisher['date_founded'])
#                 except:
#                     founded = parser.parse('1-1-1900')
#                 c = Company(name=publisher['name'], image=publisher['image']['medium_url'],\
#                     city=publisher['location_city'], country=publisher['location_country'],\
#                     deck=publisher['deck'])
#                 company_cache.append(c)
#                 db.session.add(c)
#             else:
#                 c = Company.query.filter_by(name=publisher['name']).first()
#             c.published_games.append(g)
#             db.session.add(c)
#         for person in game['people']:
#             c = 0
#             person_details = companies[person['id']]
#             if person['id'] not in person_cache:
#                 try:
#                     birth = parser.parse(person['birth_date'])
#                 except:
#                     birth = parser.parse('1-1-1900')
#                 try:
#                     death = parser.parse(person['death_date'])
#                 except:
#                     death = parser.parse('1-1-1900')
#                 # if person['first_credited_game']['id'] not in game_cache:
#
#                 p = Person(name=person['name'], hometown=person['hometown'],\
#                 country=person['country'], deck=person['deck'])
#                 person_cache.append(person['id'])
#                 db.session.add(p)
#             else:
#                 p = Person.query.filter_by(id=person['id']).first()
#             p.games.append(g)
#             db.session.add(p)





    # d = companies_json[int(f.split('.')[0])]
    # d['date_founded'] = parser.parse(d['date_founded'])
    # c = Company(name=publisher, deck=d['deck'], city=d['location_city'],\
    #         country=d['location_country'], date_founded=d['date_founded'],\
    #         image=d['image']['medium_url'])
    # for game in d['developed_games']:
    #     game_details = games_json[game['id']]
    #     g = Game()

print("--- %s seconds ---" % (time.time() - start_time))
