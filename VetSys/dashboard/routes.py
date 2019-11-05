from flask import Blueprint,render_template
from flask_login import login_required


dashboard=Blueprint('dashboard',__name__)

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def profile():
    return render_template('dashboard.html')


# "yeni kayit" on the left panel
@dashboard.route('/add_register', methods=['GET', 'POST'])
def add_register():
    return render_template('add_register.html')

# "randevu yaz" on the left panel
@dashboard.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    return render_template('add_appointment.html')

# "kayitlari goruntule" on the left panel
@dashboard.route('/display_registers', methods=['GET', 'POST'])
def display_registers():
    return render_template('display_registers.html')