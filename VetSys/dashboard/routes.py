from flask import Blueprint
from flask import render_template

dashboard=Blueprint('dashboard',__name__)

@dashboard.route('/')
def dashboard_view():
    return "selam"
