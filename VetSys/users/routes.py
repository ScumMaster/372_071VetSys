from flask import Blueprint, flash
from flask import render_template, redirect, url_for, request
from .models import User
from flask_login import login_required, login_user, current_user, logout_user
from .forms import LoginForm
from VetSys import bc, db
from flask_user import roles_required

users = Blueprint('users', __name__)


@users.route('/', methods=['GET', 'POST'])
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('dashboard.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bc.check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.is_admin:
                return redirect('/admin')
            else:
                return redirect("/dashboard")
            next_page = request.args.get('next')
            if next_page:
                return redirect(url_for(next_page))
            else:
                return redirect(url_for('dashboard.profile'))
        else:
            flash('Incorrect email or password!')
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))
