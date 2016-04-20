import os
import unittest
from ggmate import db, app_instance
from ggmate.models import Company, Person, Game, Platform
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dateutil import parser
from flask import Flask

class DBTestCases(unittest.TestCase):
    def setUp(self):
        db.create_all()
        self.connection = db.engine.connect()
        self.trans = self.connection.begin()
        Session = sessionmaker(bind=db.engine)
        self.session = Session()

    def tearDown(self):
        self.session.rollback()

    # Insert companies
    def test_company_insert(self):
        company_repr = {"name": "SomeCompany", "city": "Austin", "country": "US",
                        "deck": "Specializes in making dope games",
                        "date_founded": parser.parse("2016-02-01 00:00:00")}
        c = Company(**company_repr)
        self.session.add(c)

        r = self.session.query(Company).filter(Company.city == "Austin").first()
        self.assertEqual(r.name, "SomeCompany")
        self.assertEqual(r.country, "US")
        self.assertEqual(r.date_founded, datetime(2016, 2, 1, 0, 0))

    # Insert people
    def test_person_insert(self):
        person_repr = {"name": "Alice Powell", "hometown": "Fairfax", "country": "US",
                        "birth_date": parser.parse("1986-03-12 00:00:00")}
        p = Person(**person_repr)
        self.session.add(p)

        r = self.session.query(Person).filter(Person.name == "Alice Powell").first()
        self.assertEqual(r.hometown, "Fairfax")
        self.assertEqual(r.country, "US")
        self.assertEqual(r.birth_date, datetime(1986, 3, 12, 0, 0))

    # Insert games
    def test_game_insert(self):
        game_repr = {"name": "Bioshock", "deck": "Fight crazy people in an underwater city.",
                    "release_date": parser.parse("2007-08-21 00:00:00")}
        g = Game(**game_repr)
        self.session.add(g)

        r = self.session.query(Game).filter(Game.name == "Bioshock").first()
        self.assertEqual(r.deck, "Fight crazy people in an underwater city.")
        self.assertEqual(r.release_date, datetime(2007, 8, 21, 0, 0))

    # Insert platforms
    def test_platform_insert(self):
        platform_repr = {"name": "Playstation 4", "short": "PS4"}
        p = Platform(**platform_repr)
        self.session.add(p)

        r = self.session.query(Platform).filter(Platform.short == "PS4").first()
        self.assertEqual(r.name, "Playstation 4")

    # Assigning platforms to a game
    def test_game_platforms(self):
        p1 = Platform(name="Commodore 64", short="C64")
        p2 = Platform(name="Game Boy", short="GB")
        self.session.add(p1)
        self.session.add(p2)

        g = Game(name="A Random Game")
        g.platforms.append(p1)
        g.platforms.append(p2)
        self.session.add(g)

        self.assertTrue(len(g.platforms) >= 2)

    # Viewing games of a particular platform
    def test_platform_games(self):
        p1 = Platform(name="Commodore 64", short="C64")
        p2 = Platform(name="Game Boy", short="GB")
        self.session.add(p1)
        self.session.add(p2)

        g1 = Game(name="A Random Game")
        g2 = Game(name="A Random Game 2")
        g3 = Game(name="A Random Game 2: Spinoff")
        g4 = Game(name="A Random Game 3: Return of the Jedi")
        g1.platforms.append(p1)
        g2.platforms.append(p1)
        g3.platforms.append(p2)
        g4.platforms.append(p1)
        g4.platforms.append(p2)

        self.session.add(g1)
        self.session.add(g2)
        self.session.add(g3)
        self.session.add(g4)

        self.assertEqual(len(p1.games.all()), 3)
        self.assertEqual(p2.games[0].name, "A Random Game 2: Spinoff")

    # Assigning people to a company
    def test_company_people(self):
        c = Company(name="CoolCats")
        p = Person(name="Elise")
        self.session.add(c)
        self.session.add(p)

        self.assertTrue(len(c.people) < 1)
        c.people.append(p)
        self.session.add(c)

        result = self.session.query(Company).filter_by(name="CoolCats").first()
        p_again = result.people[0]
        self.assertEqual(p_again.name, "Elise")

    # Add developed games to a company
    def test_company_developed(self):
        c = Company(name="Yeah!")
        g1 = Game(name="Road Fighter")
        g2 = Game(name="Call of gooty 16")
        self.session.add(c)
        self.session.add(g1)
        self.session.add(g2)

        c.developed_games.append(g1)
        c.developed_games.append(g2)
        self.session.add(c)

        result = self.session.query(Company).filter(Company.name == "Yeah!").first()
        self.assertEqual(len(result.developed_games), 2)

    # Add published games to a company
    def test_company_published(self):
        c = Company(name="Righteous")
        g1 = Game(name="Shmalo 2")
        c.published_games.append(g1)
        self.session.add(c)
        self.session.add(g1)

        result = self.session.query(Company).filter(Company.name == "Righteous").first()
        self.assertEqual(result.published_games[0].name, "Shmalo 2")

    # Games a person has worked on
    def test_person_games(self):
        p = Person(name="Andrew")
        g1 = Game(name="Call of DOOOTy")
        g2 = Game(name="Action Pants 2")
        g3 = Game(name="Coffee Dude")
        self.session.add(p)
        self.session.add(g1)
        self.session.add(g2)
        self.session.add(g3)

        p.games.append(g1)
        p.games.append(g2)
        p.games.append(g3)
        self.session.add(p)

        self.assertEqual(len(p.games), 3)

    # People involved with a game
    def test_game_people(self):
        p1 = Person(name="Andrew")
        p2 = Person(name="Rachel")
        p3 = Person(name="Beth")
        g = Game(name="Super Awesome Squad")
        g.people.append(p1)
        g.people.append(p2)
        g.people.append(p3)
        self.session.add(p1)
        self.session.add(p2)
        self.session.add(p3)
        self.session.add(g)

        result = self.session.query(Game).filter_by(name='Super Awesome Squad').first()

        self.assertEqual(len(result.people), 3)

    # View developers and publishers of a game
    def test_game_companies(self):
        dev1 = Company(name="Boss Interactive")
        dev2 = Company(name="Epic Entertainment")
        pub = Company(name="We love money")
        g = Game(name="Call of brewty: Modern coffee")
        dev1.developed_games.append(g)
        dev2.developed_games.append(g)
        pub.published_games.append(g)
        self.session.add(dev1)
        self.session.add(dev2)
        self.session.add(pub)
        self.session.add(g)

        result = self.session.query(Game).filter_by(name="Call of brewty: Modern coffee").first()
        self.assertEqual(len(result.developers), 2)
        self.assertEqual(len(result.publishers), 1)

if __name__ == '__main__':
    app_instance.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/ggmate_test"
    unittest.main()
