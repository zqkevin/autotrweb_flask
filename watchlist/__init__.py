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
from watchlist.models import User

# @app.context_processor
# def inject_user(user):
#     return dict(user=user)
#获取客户端的请求中的Userid,和数据库中的比对，一致则，内置类UserMixin == 对应的user,对应变量curren_user
#否则，对应curret_user.is_anonymous = True:
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user
login_manager.login_view = 'login'
login_manager.login_message = '请先登录或者注册！'


from watchlist import views, commands, models
#from watchlist import views, errors, commands, privateconfig