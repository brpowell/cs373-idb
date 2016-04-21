#!/usr/bin/env python
from loader import app_instance, db
from models import Game, Platform, Company, Person
from flask.ext.script import Manager, Shell, Server
import os

manager = Manager(app_instance)

def make_shell_context():
    d = {
        'app': app_instance,
        'db': db,
        'Game': Game,
        'Platform': Platform,
        'Company': Company,
        'Person': Person
    }
    return d

@manager.command
def builddb():
    """ Clear the database """
    choice = input('Are you sure you want to replace? Y/N: ')
    if choice.lower() == 'y':
        db.drop_all()
        db.configure_mappers()
        db.create_all()
        db.session.commit()
        # subprocess.getoutput('psql ggmate < ../ggmate.sql')
        print('Done...Dropped tables and recreated db')

@manager.command
def test():
    import subprocess
    output = subprocess.getoutput('python tests.py')
    print(output)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('rundebug', Server(host='0.0.0.0', port="5000", use_debugger=True))
manager.add_command('runserver', Server(host='0.0.0.0', port="5000"))

if __name__ == "__main__":
    manager.run()
