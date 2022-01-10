# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from watchlist import db
import time

class User(db.Model, UserMixin):

    __tablename__ = 'webuser'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

class Anguser(db.Model):
    __tablename__ = 'user'
    __bind_key__ = 'angsql'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    analy = db.Column(db.Integer, default=0)
    analy1 = db.Column(db.Integer, default=0)
    analy2 = db.Column(db.Integer, default=0)
    share = db.Column(db.Integer, default=100)
    pt_name = db.Column(db.String(128))
    pt_flag = db.Column(db.Integer)
    pt_api_key = db.Column(db.String(128))
    pt_secret_key = db.Column(db.String(128))
    pt_passphrase = db.Column(db.String(128))
    pt_other = db.Column(db.String(128))
    flag = db.Column(db.Integer, default=1)



class Analy(db.Model):
    __tablename__ = 'analy'
    __bind_key__ = 'angsql'
    id = db.Column(db.Integer, primary_key=True)
    btime = db.Column(db.DateTime)
    atime = db.Column(db.DateTime)
    side = db.Column(db.String(32))  # 触发方向
    bprice = db.Column(db.Float)  # 前一次市场价
    aprice = db.Column(db.Float)  # 本次触发市场价
    bsz = db.Column(db.Float)  # 前一条最新成交数
    asz = db.Column(db.Float)  # 本次最新成交数
    b24H = db.Column(db.Float)    # 前一次总交易量
    a24H = db.Column(db.Float)    # 本次总交易量




class Ethusdt1m(db.Model):
    __tablename__ = 'ethusdt1m'
    __bind_key__ = 'angsql'
    id = db.Column(db.Integer, primary_key=True)
    opentime = db.Column(db.DateTime)
    openpr = db.Column(db.Float)
    hightpr = db.Column(db.Float)
    lowpr = db.Column(db.Float)
    closepr = db.Column(db.Float)
    bustur = db.Column(db.Float)
    closetime = db.Column(db.DateTime)
    busvolu = db.Column(db.Float)
    busnum = db.Column(db.Integer)
    actbustur = db.Column(db.Float)
    actbusvolu = db.Column(db.Float)


class Orders(db.Model):
    __tablename__ = 'orders'
    __bind_key__ = 'angsql'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)  # 下单用户
    pt = db.Column(db.Integer)    # 使用平台 1:okex 2:bianace
    ordertime = db.Column(db.DateTime)  # 成交时间
    avgprice = db.Column(db.Float)  # 成交均价
    orderid = db.Column(db.String(30))  # 订单id
    side = db.Column(db.String(30))  # 订单方向
    price = db.Column(db.Float)  # 下单价格
    origqty = db.Column(db.Float)  # 成交数量
    status = db.Column(db.String(30))  # 订单状态
    fig = db.Column(db.Float)  # 盈亏
    lever = db.Column(db.Integer)  # 杠杆
    acc_ky = db.Column(db.Float)  # 可用资金
    acc_zy = db.Column(db.Float)  # 占用资金
    acc_wsx = db.Column(db.Float)  # 未实现盈利
    pos_ccl = db.Column(db.Float)  # 持仓量
    pos_ccj = db.Column(db.Float)  # 持仓价
    pos_side = db.Column(db.Integer)  # 持仓方向
    amount = db.Column(db.Float)  # 资金总额
