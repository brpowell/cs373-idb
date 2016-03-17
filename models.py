from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# Create association tables for many-to-many relationships
company_person = db.Table('company_person',
    db.Column('company_id', db.Integer, db.ForeignKey('companies.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('people.id'))
)
developer_game = db.Table('company_game',
    db.Column('company_id', db.Integer, db.ForeignKey('companies.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'))
)
publisher_game = db.Table('company_game',
    db.Column('company_id', db.Integer, db.ForeignKey('companies.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'))
)
person_game = db.Table('person_game',
    db.Column('person_id', db.Integer, db.ForeignKey('people.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'))
)
worked_with = db.Table('worked_with',
    db.Column('person_id', db.Integer, db.ForeignKey('people.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('people.id'))
)
game_platform = db.Table('game_platform',
    db.Column('game_id', db.Integer, db.ForeignKey('games.id')),
    db.Column('platform_id', db.Integer, db.ForeignKey('platforms.id'))
)

class Platform(db.Model):
    __tablename__ = 'platforms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    short = db.Column(db.String(10))

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    deck = db.Column(db.String(255))
    image = db.Column(db.String(255))
    metacritic = db.Column(db.Integer)
    platforms = db.relationship('Platform', secondary=game_platform,
                    backref=db.backref('games', lazy='dynamic'))
                    
    def __repr__(self):
        return '<Game %r>' % self.name

class Person(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image = db.Column(db.String(255))
    hometown = db.Column(db.String(255))
    country = db.Column(db.String(255))
    birth_date = db.Column(db.DateTime)
    death_date = db.Column(db.DateTime)
    deck = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    first_game_id = db.Column(db.Integer, db.ForeignKey('first_game.id'))
    # twitter = db.Column(db.Text)
    games = db.relationship('Game', secondary=person_game,
                        backref=db.backref('people', lazy='dynamic'))
    people = db.relationship('Person', secondary=worked_with,
                        backref=db.backref('people', lazy='dynamic'))

    def __init__(self, person):
        self.id = person['id']
        self.name = person['name']
        self.image = person['image']
        self.hometown = person['hometown']
        self.country = person['country']
        self.birth_date = person['birth_date']
        self.death_date = person['death_date']
        self.deck = person['deck']
        self.gender = person['gender']
        self.first_game_id = person['first_credited_game']['id']

        # for game in person['games']
            # Create game relationships

        # for person in person['people']
            # Create people relationships

    def __repr__(self):
        return '<Person %r>' % self.name

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image = db.Column(db.String(255))
    city = db.Column(db.String(255))
    country = db.Column(db.String(255))
    deck = db.Column(db.Text)
    date_founded = db.Column(db.DateTime)
    #twitter
    people = db.relationship('Person', secondary=company_person,
                        backref=db.backref('companies', lazy='dynamic'))
    developed_games = db.relationship('Game', secondary=developer_game,
                        backref=db.backref('developers', lazy='dynamic'))
    published_games = db.relationship('Game', secondary=publisher_game,
                        backref=db.backref('publishers', lazy='dynamic'))

    def __init__(self, company):
        self.id = company['id']
        self.name = company['name']
        self.image = company['image']
        self.city = company['city']
        self.country = company['country']
        self.deck = company['deck']
        self.date_founded = company['date_founded']

        # for person in company['people']:
            # populate people table

        # for game in company['developed_games']
            # populate games table

        # for game in company['published_games']
            # populate games table

    def __repr__(self):
        return '<Company %r>' % self.name
