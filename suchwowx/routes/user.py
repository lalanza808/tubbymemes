from flask import Blueprint, render_template
from flask import redirect, url_for

from suchwowx.models import User


bp = Blueprint('user', 'user')


@bp.route('/user/<handle>')
def show(handle):
    user = User.query.filter(User.handle == handle).first()
    if not user:
        return redirect(url_for('meme.index'))
    return render_template('profile.html', user=user)
