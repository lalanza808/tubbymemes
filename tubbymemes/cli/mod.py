import click
from flask import Blueprint

from tubbymemes.models import User
from tubbymemes.factory import db


bp = Blueprint('mod', 'mod')


@bp.cli.command('list')
def list():
    """
    List current server moderators.
    """
    for mod in User.query.filter(User.moderator == True):
        click.echo(f'{mod.id} - {mod.public_address}')


@bp.cli.command('add')
@click.argument('address')
def add(address):
    """
    Add server moderators by address.
    """
    user = User.query.filter(User.public_address == address).first()
    if user:
        if not user.moderator:
            user.moderator = True
            db.session.commit()
            click.echo(f'[+] Added moderator status to {address}')
        else:
            click.echo('[.] User is already a moderator')
    else:
        click.echo('[!] No user with that address.')


@bp.cli.command('remove')
@click.argument('address')
def remove(address):
    """
    Remove server moderator by address.
    """
    user = User.query.filter(User.public_address == address).first()
    if user:
        if user.moderator:
            user.moderator = False
            db.session.commit()
            click.echo(f'[-] Removed moderator status from {address}')
        else:
            click.echo('[.] That user is not a moderator.')
    else:
        click.echo('[!] No user with that address.')
