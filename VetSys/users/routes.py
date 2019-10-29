from flask import Blueprint
from flask import render_template,redirect,url_for,request
from .models import Staff
from flask_login import login_required,login_user,current_user,logout_user
from .forms import LoginForm
from VetSys import bc

users=Blueprint('users',__name__)


@users.route('/createstaff')
def create_staff():
    pass

@users.route('/',methods=['GET','POST'])
@users.route('/login',)
def login():

    if current_user.is_authenticated:
        redirect(url_for('dashboard.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        staff=Staff.query.filter_by(email=form.email.data).first()
        if staff and bc.check_password_hash(staff.email,form.password.data):
            login_user(staff)
            next_page=request.args.get('next')
            if next_page:
                return redirect(url_for(next_page))
            else:
                return redirect(url_for('dashboard.profile'))

    return render_template('login.html',form=form)




@users.route('/logout')
def logout():
    pass




