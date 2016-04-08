#!/usr/bin/env python
from ggmate import app_instance, db
from ggmate.models import Game, Platform, Rating, Company, Person
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand
import os

manager = Manager(app_instance)
migrate = Migrate(app_instance, db)

def make_shell_context():
    d = {
        'app': app_instance,
        'db': db,
        'Game': Game,
        'Platform': Platform,
        'Rating': Rating,
        'Company': Company,
        'Person': Person
    }
    return d

@manager.command
def resetdb():
    """ Clear the database """
    choice = input('Are you sure? Y/N: ')
    if choice.lower() == 'y':
        db.session.commit()
        db.drop_all()
        db.create_all()
        print('Done...Dropped tables and recreated db')

@manager.command
def test():
    import subprocess
    output = subprocess.getoutput('python tests.py')
    print(output)

manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('rundebug', Server(host='0.0.0.0', port="5000", use_debugger=True))

if __name__ == "__main__":
    manager.run()
