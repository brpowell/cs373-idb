import os
import unittest
from ggmate import db, app_instance
from ggmate.models import Company, Person, Game, Platform, Rating
from flask.ext.testing import TestCase
from datetime import datetime
from dateutil import parser

TEST_DATABASE_URI = "sqlite://"
class DBTestCases(TestCase):
    def create_app(self):
        app_instance.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
        return app_instance

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Insert companies
    def test_company_insert(self):

        company_repr = {"id": 1, "name": "SomeCompany", "city": "Austin", "country": "US",
                        "deck": "Specializes in making dope games",
                        "date_founded": parser.parse("2016-02-01 00:00:00")}
        c = Company(**company_repr)
        db.session.add(c)
        db.session.commit()
        r = db.session.query(Company).filter(Company.city == "Austin").first()
        self.assertEqual(r.id, 1)
        self.assertEqual(r.name, "SomeCompany")
        self.assertEqual(r.country, "US")
        self.assertEqual(r.date_founded, datetime(2016, 2, 1, 0, 0))

    # Insert people
    def test_person_insert(self):
        person_repr = {"id": 1, "name": "Alice Powell", "hometown": "Fairfax", "country": "US",
                        "birth_date": parser.parse("1986-03-12 00:00:00")}
        p = Person(**person_repr)
        db.session.add(p)
        db.session.commit()
        r = db.session.query(Person).filter(Person.name == "Alice Powell").first()
        self.assertEqual(r.hometown, "Fairfax")
        self.assertEqual(r.id, 1)
        self.assertEqual(r.country, "US")
        self.assertEqual(r.birth_date, datetime(1986, 3, 12, 0, 0))

    # Insert games
    def test_game_insert(self):
        game_repr = {"id": 1, "name": "Bioshock", "deck": "Fight crazy people in an underwater city.",
                    "release_date": parser.parse("2007-08-21 00:00:00")}
        g = Game(**game_repr)
        db.session.add(g)
        db.session.commit()
        r = db.session.query(Game).filter(Game.name == "Bioshock").first()
        self.assertEqual(r.id, 1)
        self.assertEqual(r.deck, "Fight crazy people in an underwater city.")
        self.assertEqual(r.release_date, datetime(2007, 8, 21, 0, 0))

    # Insert platforms
    def test_platform_insert(self):
        platform_repr = {"id": 1, "name": "Playstation 4", "short": "PS4"}
        p = Platform(**platform_repr)
        db.session.add(p)
        db.session.commit()
        r = db.session.query(Platform).filter(Platform.short == "PS4").first()
        self.assertEqual(r.name, "Playstation 4")
        self.assertEqual(r.id, 1)

    # Insert ratings
    def test_rating_insert(self):
        game_repr = {"id": 3, "name": "Timesplitters", "deck": "Such a great game",
                    "release_date": parser.parse("2002-07-16")}
        g = Game(**game_repr)
        p1 = Platform(name="Fake Console")
        p2 = Platform(name="Fake Console 2")
        db.session.add(g)
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        r1 = Rating(game_id=g.id, platform_id=p2.id, metacritic=76)
        r2 = Rating(game_id=g.id, platform_id=p1.id, metacritic=85)
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        r = Game.query.filter_by(id=3).first()
        self.assertEqual(len(r.ratings), 2)

    # Test for the best metacritic rating a game has
    def test_game_ratings(self):
        game_repr = {"id": 2, "name": "Mass Effect 2"}
        items = [   Game(**game_repr),
                    Platform(id=1, name="PC", short="PC"),
                    Platform(id=2, name="Xbox 360", short="X360"),
                    Platform(id=3, name="Playstation 3", short="X360"),
                    Rating(game_id=2, platform_id=1, metacritic=94),
                    Rating(game_id=2, platform_id=2, metacritic=96),
                    Rating(game_id=2, platform_id=3, metacritic=94) ]
        for i in items:
            db.session.add(i)
        db.session.commit()

        g = Game.query.filter_by(name="Mass Effect 2").first()
        r = g.best_rating()
        self.assertEqual(r.metacritic, 96)
        self.assertEqual(r.platform.short, "X360")

    # Assigning platforms to a game
    def test_game_platforms(self):
        p1 = Platform(name="Commodore 64", short="C64")
        p2 = Platform(name="Game Boy", short="GB")
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        g = Game(name="A Random Game")
        g.platforms.append(p1)
        g.platforms.append(p2)
        db.session.add(g)
        db.session.commit()
        self.assertTrue(len(g.platforms) >= 2)

    # Assigning people to a company
    def test_company_people(self):
        c = Company(name="CoolCats")
        p = Person(name="Elise")
        db.session.add(c)
        db.session.add(p)
        db.session.commit()
        self.assertTrue(len(c.people) < 1)
        c.people.append(p)
        db.session.add(c)
        db.session.commit()
        result = Company.query.filter_by(name="CoolCats").first()
        p_again = result.people[0]
        self.assertEqual(p_again.name, "Elise")

    # Add developed and published games to a company
    def test_company_games(self):
        c = Company(name="Yeah!", city="Boston", country="US")
        g1 = Game(name="Road Fighter")
        g2 = Game(name="Call of gooty 16")
        g3 = Game(name="Shmalo 2")
        items = [c, g1, g2, g3]
        for i in items:
            db.session.add(i)
        db.session.commit()
        c.published_games.append(g1)
        c.developed_games.append(g2)
        c.developed_games.append(g3)
        db.session.add(c)
        db.session.commit()
        result = db.session.query(Company).filter(Company.name == "Yeah!").first()
        self.assertEqual(len(result.developed_games), 2)
        self.assertEqual(len(result.published_games), 1)

    # Get ratings on a platform
    def test_platform_ratings(self):
        p = Platform(name="Nintendo 3DS", short="3DS")
        g1 = Game(name="Kiddo")
        g2 = Game(name="Spitto")
        g1.platforms.append(p)
        g2.platforms.append(p)
        db.session.add(p)
        db.session.add(g1)
        db.session.add(g2)
        db.session.commit()
        r1 = Rating(game_id=g1.id, platform_id=p.id, metacritic=87)
        r2 = Rating(game_id=g2.id, platform_id=p.id, metacritic=92)
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        r = Platform.query.filter_by(short="3DS").first()
        self.assertEqual(len(r.ratings), 2)
        best_rating = r.best_rating()
        self.assertEqual(best_rating.metacritic, 92)

    # Test the coworker assignment method
    def test_coworkers(self):
        p1 = Person(name="John")
        p2 = Person(name="Carol")
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        p1.coworker(p2)
        self.assertEqual(p1.people[0].name, "Carol")
        self.assertEqual(p2.people[0].name, "John")

    # People a person has worked with
    def test_person_associates(self):
        p1 = Person(name="John")
        p2 = Person(name="Carol")
        p3 = Person(name="Doug")
        p4 = Person(name="Rachel")
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.commit()

        p1.coworker(p2)
        p1.coworker(p3)
        p2.coworker(p3)
        p3.coworker(p4)
        p4.coworker(p1)

        self.assertEqual(len(p1.people.all()), 3)
        self.assertEqual(len(p2.people.all()), 2)
        self.assertEqual(len(p3.people.all()), 3)
        self.assertEqual(len(p4.people.all()), 2)

    # Games a person has worked on
    def test_person_games(self):
        p = Person(name="Andrew")
        g1 = Game(name="Call of DOOOTy")
        g2 = Game(name="Action Pants 2")
        g3 = Game(name="Coffee Dude")
        db.session.add(p)
        db.session.add(g1)
        db.session.add(g2)
        db.session.add(g3)
        db.session.commit()
        p.games.append(g1)
        p.games.append(g2)
        p.games.append(g3)
        db.session.add(p)
        db.session.commit()
        self.assertEqual(len(p.games), 3)

    # First credited game for a person
    def test_first_game(self):
        g = Game(name="Game of Kyle")
        db.session.add(g)
        db.session.commit()
        p = Person(name="Kyle", first_credited_game=g.id)
        db.session.add(p)
        db.session.commit()
        self.assertEqual(p.first_game.name, "Game of Kyle")

    def test_first_game_multiple(self):
        g = Game(name="2 People")
        db.session.add(g)
        db.session.commit()
        p1 = Person(name="Kyle", first_credited_game=g.id)
        p2 = Person(name="Naomi", first_credited_game=g.id)
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        self.assertEqual(len(g.first_for), 2)

if __name__ == '__main__':
    unittest.main()
