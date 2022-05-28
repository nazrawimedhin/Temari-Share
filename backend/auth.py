import functools
from flask import (
    Blueprint, request, redirect, url_for, flash, render_template, session,
    g
)
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import User, Role

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        profile_pic = request.form['profile_pic']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'

        if error is None:
            user_role = Role.query.filter(Role.name == 'user').one()
            user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                profile_pic=profile_pic,
                role_id=user_role.id
            )
            db.session.add(user)
            return redirect(url_for("auth.login"))
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter(User.username == username).first_or_404()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """loads user data before request"""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.id == user_id).one()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
