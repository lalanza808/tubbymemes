from flask import Blueprint, render_template, send_from_directory
from flask import redirect, url_for
from flask_login import logout_user

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
