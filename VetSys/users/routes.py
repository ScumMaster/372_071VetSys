from flask import Blueprint
from flask import render_template

users=Blueprint('users',__name__)


@users.route('/createstaff')
def create_staff():
    pass

@users.route('/login')
def login():
    pass

@users.route('/logout')
def logout():
    pass




