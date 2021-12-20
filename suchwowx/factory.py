from logging.config import dictConfig

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mobility import Mobility

from suchwowx import config


db = SQLAlchemy()


def setup_db(app: Flask, db:SQLAlchemy=db):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.DATA_FOLDER}/sqlite.db' # noqa
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return db

def create_app_huey():
    app = Flask(__name__)
    db = SQLAlchemy()
    dictConfig(config.LOGGING_CONFIG)
    setup_db(app, db)
    return app

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('FLASK_SECRETS')
    setup_db(app)
    Mobility(app)

    with app.app_context():
        from suchwowx import filters, routes, cli
        app.register_blueprint(filters.bp)
        app.register_blueprint(routes.bp)
        app.register_blueprint(cli.bp)
        return app
