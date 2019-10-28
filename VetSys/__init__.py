from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# initializing database
db = SQLAlchemy(app)

# register dashboard app
from VetSys.dashboard.routes import dashboard
app.register_blueprint(dashboard)

# register login app
from VetSys.login.routes import login
app.register_blueprint(login)

