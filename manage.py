#!/usr/bin/env python
from app import app_instance, db
from app.models import Game
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app_instance)
migrate = Migrate(app_instance, db)
db.session.commit()
db.create_all()

def make_shell_context():
    return dict(app=app_instance, db=db, Game=Game)

@manager.command
def resetdb():
    choice = input('Are you sure? Y/N: ')
    if choice.lower() == 'y':
        db.session.commit()
        db.drop_all()
        db.create_all()
        print('Done...Dropped tables and recreated db')

manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('rundebug', Server(host='0.0.0.0', use_debugger=True))

if __name__ == "__main__":
    manager.run()
