from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY']='mF4k_1tGfeNCxXz7g_mn7_mIfAlPBZ0lwrMCSVqH0BOnQQ75A11jEMrpI6MpmVvcuFG-8OhSnoQV8mH2Yiww4rXf-d5CwlMq'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
# initializing database
db = SQLAlchemy(app)
bc=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='users.login'

# register dashboard app
from VetSys.users.routes import users
app.register_blueprint(users)

# register users app
from VetSys.dashboard.routes import dashboard
app.register_blueprint(dashboard)









