from flask import Blueprint, render_template, send_from_directory
from flask import redirect, url_for, flash, request
from flask_login import logout_user, current_user

from suchwowx.models import User, Remote
from suchwowx.factory import db
from suchwowx import config


bp = Blueprint('meta', 'meta')


@bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """
    Retrieve an uploaded file from uploads directory.
    """
    return send_from_directory(f'{config.DATA_FOLDER}/uploads', filename)


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/disconnect')
def disconnect():
    logout_user()
    return redirect(url_for('meme.index'))


@bp.route('/remotes', methods=['GET', 'POST'])
def remotes():
    if not current_user.is_authenticated or not current_user.is_moderator():
        flash('You need to be moderator to access that page.', 'warning')
        return redirect(url_for('meme.index'))
    remotes = Remote.query.filter().order_by(Remote.create_date.asc())
    ep = request.form.get('endpoint')
    if ep:
        if ep.startswith('http'):
            if not Remote.query.filter(Remote.endpoint == ep).first():
                r = Remote(endpoint=ep)
                db.session.add(r)
                db.session.commit()
                flash('Added new remote server.', 'success')
            else:
                flash('That remote server already exists.', 'warning')
        else:
            flash('Incorrect endpoint provided, must start with http or https.', 'warning') # noqa
    return render_template('remotes.html', remotes=remotes)


@bp.route('/remotes/delete/<int:remote_id>')
def delete_remote(remote_id):
    existing = Remote.query.get(remote_id)
    if not current_user.is_authenticated or not current_user.is_moderator():
        flash('You need to be moderator to access that page.', 'warning')
        return redirect(url_for('meme.index'))
    if not existing:
        flash('That remote does not exist', 'warning')
        return redirect(url_for('meme.mod'))
    db.session.delete(existing)
    db.session.commit()
    flash(f'Deleted remote server {existing}', 'success')
    return redirect(url_for('meta.remotes'))
