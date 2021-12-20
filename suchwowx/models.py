from uuid import uuid4
from datetime import datetime

from suchwowx.factory import db


def rand_id():
    return uuid4().hex


class Meme(db.Model):
    __tablename__ = 'memes'

    id = db.Column(db.String(80), default=rand_id, primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow())
    upload_path = db.Column(db.String(200), unique=True)
    meta_ipfs_hash = db.Column(db.String(100), unique=True)
    meme_ipfs_hash = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(400))
    creator_handle = db.Column(db.String(50))

    def __repr__(self):
        return str(f'meme-{self.id}')
