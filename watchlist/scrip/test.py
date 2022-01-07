#! /www/wwwroot/flask/venv/bin/python3.8
import numpy as np
from watchlist import app, db
from watchlist.models import User, Movie, Ethusdt1m, Order
from watchlist.scrip import binance
from datetime import datetime
import threading
import time

exitFlag = 0
acc = 0
pos = 0
arprday = 0
arprh = 0


class myThread1(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("开启线程：" + self.name)
        while exitFlag == 0:
            binance.geteth1m()
            time.sleep(61)
        print("退出线程：" + self.name)


class myThread2(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("开启线程：" + self.name)
        while exitFlag == 0:
            runbinan()
            time.sleep(61)
        print("退出线程：" + self.name)


def init():
    global acc, pos, arprday, arprh
    acc = binance.getacc()[5]
    pos = binance.getpostion()[0]
    days30 = binance.getstick(interval='1d')[0]
    arprday = round(np.average([a.close for a in days30]), 2)
    h30 = binance.getstick(interval='1h')[0]
    arprh = round(np.average([a.close for a in h30]), 2)
    return


def runbinan(price):
    global acc, pos, arprday, arprh
    # eth1m = Ethusdt1m
    # ethmin = eth1m.query.filter(eth1m.id > (eth1m.query.count() - 30)).all()
    now = datetime.now()
    now = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    print('开始挂机ETH，现在时间是：', now, '开始价格是：', price)

    while True:
        markprice = round(binance.getprice().markPrice, 2)
        time.sleep(0.5)
        ran = (markprice - price) / markprice
        if abs(ran) >= 0.003:
            acc = binance.getacc()[5]
            balanc = acc.balance
            avaibalanc = acc.withdrawAvailable
            blana = avaibalanc * pos.leverage
            if blana > 1000:
                quantity = round(blana / 100 / markprice, 3)
            elif blana < 100:
                time.sleep(10)
                continue
            else:
                quantity = round(7 / price, 3)
            if ran > 0:
                side = "SELL"
            else:
                side = "BUY"
            order_frog = 1
            while order_frog == 1:
                order = binance.trade(ordertype='MARKET', price=None, side=side, quantity=quantity, timeInForce=None)
                time.sleep(1)
                ordered = binance.getordered(orderid=order.orderId)
                while ordered.status == 'PARTIALLY_FILLED' and ordered.status == 'NEW':
                    ordered = binance.getordered(orderid=order.orderId)
                    time.sleep(2)
                if ordered.status == 'FILLED':
                    order_frog = 0
                    price = markprice
                    acc = binance.getacc()[5]
                    profit = round(acc.balance - balanc, 2)
                    orders = Order(ordertime=ordered.updateTime, orderid=ordered.orderId, side=ordered.side,
                                   avgprice=ordered.avgPrice, price=price, origqty=ordered.executedQty,
                                   status=ordered.status, fig=profit)
                    db.session.add(orders)
                    db.session.commit()
                elif ordered.status == 'CANCELED' and ordered.status == 'REJECTED':
                    order_frog = 0

        time.sleep(10)


if __name__ == '__main__':
    init()
    markprice = round(binance.getprice().markPrice, 2)
    time.sleep(10)
    runbinan(markprice)

    print('test')
