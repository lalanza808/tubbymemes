from logging.config import dictConfig

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mobility import Mobility
from web3 import Web3

from suchwowx import config


db = SQLAlchemy()
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:9650')) # todo


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
    login_manager = LoginManager(app)
    login_manager.login_view = 'meme.index'
    login_manager.logout_view = 'meta.disconnect'

    @login_manager.user_loader
    def load_user(user_id):
        from suchwowx.models import User
        user = User.query.get(user_id)
        return user

    with app.app_context():
        from suchwowx import filters, cli
        from suchwowx.routes import api, meme, meta
        app.register_blueprint(filters.bp)
        app.register_blueprint(cli.bp)
        app.register_blueprint(api.bp)
        app.register_blueprint(meme.bp)
        app.register_blueprint(meta.bp)
        return app
