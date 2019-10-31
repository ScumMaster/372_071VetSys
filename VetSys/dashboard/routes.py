from flask import Blueprint,render_template
from flask_login import login_required


dashboard=Blueprint('dashboard',__name__)

@dashboard.route('/dashboard')
@login_required
def profile():
    return render_template('dashboard.html')
