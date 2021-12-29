from uuid import uuid4
from datetime import datetime

from flask_login import login_user

from suchwowx.factory import db
from suchwowx import config


def rand_id():
    return uuid4().hex

class Moderator(db.Model):
    __tablename__ = 'moderators'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='moderator')

    def __rep__(self):
        return self.user.handle

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    register_date = db.Column(db.DateTime, default=datetime.utcnow())
    last_login_date = db.Column(db.DateTime, nullable=True)
    verified = db.Column(db.Boolean, default=False)
    public_address = db.Column(db.String(180))
    nonce = db.Column(db.String(180), default=rand_id())
    nonce_date = db.Column(db.DateTime, default=datetime.utcnow())
    handle = db.Column(db.String(40), unique=True)
    bio = db.Column(db.String(600), nullable=True)
    profile_image = db.Column(db.String(300), nullable=True)
    website_url = db.Column(db.String(120), nullable=True)
    moderator = db.relationship('Moderator', back_populates='user')

    def __repr__(self):
        return str(self.handle)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        return self.admin

    def is_moderator(self):
        return len(self.moderator) > 0

    def get_id(self):
        return self.id

    def get_profile_image(self, full=True):
        if self.profile_image:
            if full:
                return url_for('meta.uploaded_file', filename=self.profile_image)
            else:
                return self.profile_image
        else:
            return '/static/img/logo.png'

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
    create_date = db.Column(db.DateTime, default=datetime.utcnow())
    file_name = db.Column(db.String(200), unique=True)
    meta_ipfs_hash = db.Column(db.String(100), unique=True, nullable=True)
    meme_ipfs_hash = db.Column(db.String(100), unique=True, nullable=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(400), nullable=True)
    creator_handle = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return str(f'meme-{self.id}')

    def get_fs_path(self):
        return f'{config.DATA_FOLDER}/uploads/{self.file_name}'
