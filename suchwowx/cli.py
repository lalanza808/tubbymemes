from flask import Blueprint

from suchwowx.factory import db


bp = Blueprint('cli', 'cli', cli_group=None)

@bp.cli.command('init')
def init():
    import suchwowx.models
    db.create_all()