# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: manager.py
#   Author:JiangLin
#   Mail:mail@honmaple.com
#   Created Time: 2016-02-11 13:34:38
# *************************************************************************
# !/usr/bin/env python
# -*- coding=UTF-8 -*-
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from run import app, db
import os

migrate = Migrate(app, db)
manager = Manager(app)


@manager.command
def run():
    return app.run()

@manager.command
def init_db():
    """
    Drops and re-creates the SQL schema
    """
    db.drop_all()
    db.configure_mappers()
    db.create_all()
    db.session.commit()


@manager.command
def babel_init():
    pybabel = 'pybabel'
    os.system(pybabel +
              ' extract -F babel.cfg -k lazy_gettext -o messages.pot maple')
    os.system(pybabel + ' init -i messages.pot -d maple/translations -l zh')
    os.unlink('messages.pot')


@manager.command
def babel_update():
    pybabel = 'pybabel'
    os.system(pybabel +
              ' extract -F babel.cfg -k lazy_gettext -o messages.pot maple')
    os.system(pybabel + ' update -i messages.pot -d maple/translations')
    os.unlink('messages.pot')


@manager.command
def babel_compile():
    pybabel = 'pybabel'
    os.system(pybabel + ' compile -d maple/translations')


@manager.option('-h', '--host', dest='host', default='127.0.0.1')
@manager.option('-p', '--port', dest='port', type=int, default=8000)
@manager.option('-w', '--workers', dest='workers', type=int, default=2)
def gunicorn(host, port, workers):
    """use gunicorn"""
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            return {'bind': '{0}:{1}'.format(host, port), 'workers': workers}

        def load(self):
            return app

    application = FlaskApplication()
    return application.run()


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
