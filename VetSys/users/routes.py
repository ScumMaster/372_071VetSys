from flask import Blueprint
from flask import render_template, redirect, url_for, request
from .models import Staff
from flask_login import login_required, login_user, current_user, logout_user
from .forms import LoginForm,AdminLoginForm
from VetSys import bc,db
from flask_user import roles_required

users = Blueprint('users', __name__)


@users.route('/createstaff',methods=['POST','GET'])
def create_staff():
    pass




@users.route('/', methods=['GET', 'POST'])
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('dashboard.profile'))
    form = LoginForm()
    print('hey')
    if form.validate_on_submit():
        staff = Staff.query.filter_by(email=form.email.data).first()
        if staff and bc.check_password_hash(staff.password, form.password.data):
            login_user(staff)
            if staff.is_admin:
                return redirect('/admin')
            next_page = request.args.get('next')
            if next_page:
                return redirect(url_for(next_page))
            else:
                return redirect(url_for('dashboard.profile'))
        else:
            err = {'err_msg': 'Email or password is incorrect.'}
            return render_template('login.html', form=form, context=err)


    return render_template('login.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))



