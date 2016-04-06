import json
import os
from app import db, app_instance
from app.models import Company, Person, Game, Platform, Rating
from datetime import datetime
from dateutil import parser

base = '../ggmate-sub/scrape/data/base/gamesData'
data = {}
cache = []

# load games for each console
for f in os.listdir(base):
    if f.endswith(".json"):
        with open(os.path.join(base, f)) as src:
            short = f.split('.')[0].upper()
            data[short] = json.loads(src.readlines()[0])
for console, games in data.items():
    print(console + " length: " + str(len(games)))
    derp = 0
    for k in games:
        derp = k
        break
    full_name = games[derp]['platforms'][0]
    p = Platform(name=full_name, short=console)
    db.session.add(p)
    db.session.commit()
    # print(str(p) + ' committed')
    for key, game in games.items():
        # print(game['gameName'])
        g = Game.query.filter_by(name=game['gameName']).first()
        print('BOOM')
        # if g is None:
        try:
            release = parser.parse(game['dataPublished'])
        except:
            release = parser.parse('1-1-1920')
        if game['gameName'] not in cache:
            g = Game(name=game['gameName'], release_date=release, \
                    deck=game['description'], content_rating=game['contentRating'],
                    genre=game['genre'])
            cache.append(game['gameName'])
            db.session.add(g)
            db.session.commit()
            # print(str(g) + ' committed')
        value = game['ratingValue']
        if value == '':
            value = 0
        else:
            value = int(value)
        r = Rating(game_id=g.id, platform_id=p.id, metacritic=value)
        g.platforms.append(p)
        db.session.add(g)
        db.session.add(r)
        db.session.commit()
        print(str(r) + ' committed')
