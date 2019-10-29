from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# initializing database
db = SQLAlchemy(app)
bc=Bcrypt(app)
login_manager=LoginManager(app)


# register dashboard app
from VetSys.dashboard.routes import dashboard
app.register_blueprint(dashboard)

# register users app
from VetSys.users.routes import users
app.register_blueprint(users)



