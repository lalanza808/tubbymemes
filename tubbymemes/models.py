from uuid import uuid4
from datetime import datetime

from flask import url_for
from flask_login import login_user
from sqlalchemy import inspect

from tubbymemes.factory import db
from tubbymemes import config


def rand_id():
    return uuid4().hex

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    register_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_date = db.Column(db.DateTime, nullable=True)
    verified = db.Column(db.Boolean, default=False)
    moderator = db.Column(db.Boolean, default=False)
    public_address = db.Column(db.String(180))
    nonce = db.Column(db.String(180), default=rand_id())
    nonce_date = db.Column(db.DateTime, default=datetime.utcnow)
    ens_address = db.Column(db.String(80), unique=True)
    memes = db.relationship('Meme', back_populates='user')

    def as_dict(self):
        return {c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs if c.key != 'nonce'}

    def __repr__(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def is_moderator(self):
        return self.moderator

    def get_id(self):
        return self.id

    def generate_nonce(self):
        return rand_id()

    def change_nonce(self):
        self.nonce = rand_id()
        self.nonce_date = datetime.utcnow()
        db.session.commit()

    def login(self):
        self.change_nonce()
        self.last_login_date = datetime.utcnow()
        login_user(self)
        db.session.commit()


class Meme(db.Model):
    __tablename__ = 'memes'

    id = db.Column(db.String(80), default=rand_id, primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_name = db.Column(db.String(200), unique=True)
    meta_ipfs_hash = db.Column(db.String(100), unique=True, nullable=True)
    meme_ipfs_hash = db.Column(db.String(100), unique=True, nullable=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(400), nullable=True)
    minted = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=False)
    synced = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='memes')

    def as_dict(self):
        return {c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return str(f'meme-{self.id}')

    def get_fs_path(self):
        return f'{config.DATA_FOLDER}/uploads/{self.file_name}'


class Remote(db.Model):
    __tablename__ = 'remotes'

    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_sync_date = db.Column(db.DateTime, nullable=True)
    paused = db.Column(db.Boolean, default=False)
    endpoint = db.Column(db.String(120))

    def __repr__(self):
        return str(f'remote-{self.id}')
