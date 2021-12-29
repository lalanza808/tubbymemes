import click
from flask import Blueprint

from suchwowx.models import Moderator, User
from suchwowx.factory import db


bp = Blueprint('mod', 'mod')


@bp.cli.command('list')
def list():
    """
    List current server moderators.
    """
    for mod in Moderator.query.all():
        click.echo(mod.user.handle)


@bp.cli.command('add')
@click.argument('moderator_handle')
def add(moderator_handle):
    """
    Add server moderators by user handle.
    """
    user = User.query.filter(User.handle == moderator_handle).first()
    if user:
        mod = Moderator.query.filter(Moderator.user_id == user.id).first()
        if mod is None:
            m = Moderator(user_id=user.id)
            db.session.add(m)
            db.session.commit()
            click.echo(f'[+] Added moderator status to `{moderator_handle}`')
    else:
        click.echo('[.] That is not a valid user.')


@bp.cli.command('remove')
@click.argument('moderator_handle')
def remove(moderator_handle):
    """
    Remove server moderator by user handle.
    """
    user = User.query.filter(User.handle == moderator_handle).first()
    if user:
        mod = Moderator.query.filter(Moderator.user_id == user.id).first()
        if mod:
            db.session.delete(mod)
            db.session.commit()
            click.echo(f'[-] Removed moderator status from `{moderator_handle}`') # noqa
        else:
            click.echo('[.] That user is not a moderator.')
    else:
        click.echo('[.] That is not a valid user.')
