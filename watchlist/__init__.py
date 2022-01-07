# -*- coding: utf-8 -*-
import os, sys, json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from controller import testModule

# SQLite URI compatible

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://autotr:pety93033@43.134.61.80:3306/autotr'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQL_PATH")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_BINDS'] = {"angsql":"mysql://root:pety&93033@127.0.0.1:3306/richmak"}
app.config['SQLALCHEMY_BINDS'] = json.loads(os.getenv("ANG_SQL_PATH"))
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import Webuser
    user = Webuser.query.get(int(user_id))
    return user


login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'


@app.context_processor
def inject_user():
    from watchlist.models import Webuser
    user = Webuser.query.first()
    return dict(user=user)

from watchlist import views
#from watchlist import views, errors, commands, privateconfig
