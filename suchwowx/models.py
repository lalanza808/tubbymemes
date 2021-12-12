from uuid import uuid4

from suchwowx.factory import db


def rand_id():
    return uuid4().hex


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
