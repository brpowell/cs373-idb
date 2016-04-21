from loader import db
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable
from flask.ext.sqlalchemy import BaseQuery

make_searchable()

# Association tables for many-to-many relationships
company_person = db.Table('company_person',
    db.Column('company_id', db.Integer, db.ForeignKey('companies.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('people.id'))
)
developer_game = db.Table('developer_game',
    db.Column('company_id', db.Integer, db.ForeignKey('companies.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'))
)
publisher_game = db.Table('publisher_game',
    db.Column('company_id', db.Integer, db.ForeignKey('companies.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'))
)
person_game = db.Table('person_game',
    db.Column('person_id', db.Integer, db.ForeignKey('people.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'))
)
game_platform = db.Table('game_platform',
    db.Column('game_id', db.Integer, db.ForeignKey('games.id')),
    db.Column('platform_id', db.Integer, db.ForeignKey('platforms.id'))
)


class GameQuery(BaseQuery, SearchQueryMixin):
    pass

class CompanyQuery(BaseQuery, SearchQueryMixin):
    pass

class PersonQuery(BaseQuery, SearchQueryMixin):
    pass


class Platform(db.Model):
    __tablename__ = 'platforms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    short = db.Column(db.String(10))

    def __repr__(self):
        return '<Platform %s>' % self.short


class Game(db.Model):
    query_class = GameQuery
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    deck = db.Column(db.Text)
    image = db.Column(db.String(255))
    release_date = db.Column(db.DateTime)
    platforms = db.relationship('Platform', secondary=game_platform,
                    backref=db.backref('games', lazy='dynamic'))
    search_vector = db.Column(TSVectorType('name'))

    def to_json(self):
        json_game = {
            'id': self.id,
            'name': self.name,
            'deck': self.deck,
            'image': self.image
            # 'release_date': self.release_date
        }
        developers = []
        for dev in self.developers:
            details = {'id': dev.id, 'name': dev.name}
            developers.append(details)
        publishers = []
        for pub in self.publishers:
            details = {'id': pub.id, 'name': pub.name}
            publishers.append(details)
        platforms = []
        for plat in self.platforms:
            details = {'id': plat.id, 'name': plat.name, 'short': plat.short}
            platforms.append(details)
        json_game['developers'] = developers
        json_game['publishers'] = publishers
        json_game['platforms'] = platforms
        return json_game

    def __repr__(self):
        return '<Game %r>' % self.name


class Person(db.Model):
    query_class = PersonQuery
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image = db.Column(db.String(255))
    hometown = db.Column(db.String(255))
    country = db.Column(db.String(255))
    birth_date = db.Column(db.DateTime)
    death_date = db.Column(db.DateTime)
    deck = db.Column(db.Text)
    first_credited_game = db.Column(db.Integer, db.ForeignKey('games.id'))
    games = db.relationship('Game', secondary=person_game, backref='people')
    search_vector = db.Column(TSVectorType('name'))

    def to_json(self, list_view=False):
        json_person = {
            'id': self.id,
            'name': self.name,
            'deck': self.deck,
            'image': self.image,
            'hometown': self.hometown,
            'country': self.country,
            'birth_date': self.birth_date,
            'death_date': self.death_date,
            'games_created': len(self.games)
        }
        if list_view:
            games = []
            for game in self.games:
                details = {'id': game.id, 'name': game.name}
                games.append(details)
            json_person['games'] = games
        return json_person

    def __repr__(self):
        return '<Person %s>' % self.name


class Company(db.Model):
    query_class = CompanyQuery
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image = db.Column(db.String(255))
    city = db.Column(db.String(255))
    country = db.Column(db.String(255))
    deck = db.Column(db.Text)
    date_founded = db.Column(db.DateTime)
    people = db.relationship('Person', secondary=company_person,
                        backref='companies')
    developed_games = db.relationship('Game', secondary=developer_game,
                        backref='developers')
    published_games = db.relationship('Game', secondary=publisher_game,
                        backref='publishers')
    search_vector = db.Column(TSVectorType('name'))

    def to_json(self, list_view=False):
        json_company = {
            'id': self.id,
            'name': self.name,
            'deck': self.deck,
            'image': self.image,
            'city': self.city,
            'country': self.country,
            'date_founded': self.date_founded
        }
        if list_view:
            dev_games = []
            for game in self.developed_games:
                details = {'id': game.id, 'name': game.name}
                dev_games.append(details)
            pub_games = []
            for game in self.published_games:
                details = {'id': game.id, 'name': game.name}
                pub_games.append(details)
            people = []
            people_cache = []   # removes duplicates
            for person in self.people:
                if person.id not in people_cache:
                    details = {'id': person.id, 'name': person.name}
                    people.append(details)
                    people_cache.append(person.id)
            json_company['developed_games'] = dev_games
            json_company['published_games'] = pub_games
            json_company['people'] = people
        return json_company

    def __repr__(self):
        return '<Company %s>' % self.name
