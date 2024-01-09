from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager

flightapp = Flask(__name__)
flightapp.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/flightdb?charset=utf8mb4" % quote ("Linh1019@")
flightapp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
flightapp.secret_key = "jef764544768%#%&$"

db = SQLAlchemy(app=flightapp)
login_manager = LoginManager(app=flightapp)
login_manager.init_app(app=flightapp)
login_manager.login_view = 'login'