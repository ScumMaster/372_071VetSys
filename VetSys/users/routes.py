from flask import Blueprint
from flask import render_template, redirect, url_for, request
from .models import Staff
from flask_login import login_required, login_user, current_user, logout_user
from .forms import LoginForm,RegistrationForm
from VetSys import bc,db

users = Blueprint('users', __name__)


@users.route('/createstaff',method=['POST','GET'])
def create_staff():
    form=RegistrationForm()
    if form.validate_on_submit():
        new_staff=Staff(email=form.email.data,
                        password=bc.generate_password_hash(form.password.data),
                        salary=form.salary.data,
                        phone_number=form.phone_number.data,
                        name=form.name.data,
                        address=form.address.data,
                        start_at=form.start_at.data,
                        finish_at=form.finish_at.data,
        )
        db.Session.add(new_staff)
        db.Session.commit()
        return redirect(url_for('dashboard.profile'))

    return render_template('create_staff.html',form=form)



@users.route('/', methods=['GET', 'POST'])
@users.route('/login', )
def login():
    if current_user.is_authenticated:
        redirect(url_for('dashboard.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(email=form.email.data).first()
        if staff and bc.check_password_hash(staff.email, form.password.data):
            login_user(staff)
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


