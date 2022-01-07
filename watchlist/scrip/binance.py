from binance_f import RequestClient
from watchlist import app, db
from watchlist.models import User, Movie, Ethusdt1m
# import logging
# from binance_f import SubscriptionClient
# from binance_f.constant.test import *
# from binance_f.model import *
# from binance_f.exception.binanceapiexception import BinanceApiException
from datetime import datetime
import time

request_client = RequestClient(api_key='', secret_key='')

def getstick(symbol='ETHUSDT', interval="1m", starttime=None, endtime=None, limit=30):

    if isinstance(starttime,str):
        starttime = datetime.strptime(starttime,'%Y-%m-%dT%H:%M')
        starttime = int(starttime.timestamp()*1000)

    if isinstance(endtime,str):
        endtime = datetime.strptime(endtime,'%Y-%m-%dT%H:%M')
        endtime = int(endtime.timestamp()*1000)


    result = request_client.get_candlestick_data(symbol=symbol, interval=interval, startTime=starttime, endTime=endtime,
                                                 limit=limit)
    #PrintMix.print_data(result)
    rt = []
    for r in result:
        r.openTime = datetime.fromtimestamp(int(r.openTime / 1000))
        r.closeTime = datetime.fromtimestamp(int(r.closeTime / 1000))
        r.close = float(r.close)
        r.high = float(r.high)
        r.low = float(r.low)
        r.open = float(r.open)
        r.quoteAssetVolume = float(r.quoteAssetVolume)
        r.takerBuyBaseAssetVolume = float(r.takerBuyBaseAssetVolume)
        r.takerBuyQuoteAssetVolume = float(r.takerBuyQuoteAssetVolume)
        a = (r.close - r.open)
        if a != 0:
            a = abs(a)/a
        r.zhenfu = round((r.high - r.low)/r.close*100*a, 2)
        rt.append(r)
    # print("======= Kline/Candlestick Data =======")
    # PrintMix.print_data(rt)
    # print("======================================")
    time.sleep(0.5)
    return rt,symbol


def getprice():
    result = request_client.get_mark_price(symbol="ETHUSDT")
    # r = result
    #
    # print("======= Mark Price =======")
    # PrintBasic.print_obj(result)
    time.sleep(0.5)
    return result


def getpostion(symbol='ETHUSDT'):
    # request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    result = request_client.get_position(symbol=symbol)
    time.sleep(0.5)
    return result


def getacc():
    result = request_client.get_balance()
    time.sleep(0.5)
    return result


def trade(quantity, price, side, symbol="ETHUSDT", ordertype="LIMIT", timeInForce="GTC"):
    result = request_client.post_order(symbol=symbol, side=side, ordertype=ordertype, quantity=quantity,
                                       price=price, timeInForce=timeInForce)
    time.sleep(0.5)
    return result

def getorder():
    result = request_client.get_open_orders()
    rt = []
    for r in result:
        r.updateTime = datetime.fromtimestamp(int(r.updateTime / 1000))
        rt.append(r)
    time.sleep(0.5)
    return rt
def getordered(orderid,symbol='ETHUSDT'):
    result = request_client.get_order(symbol=symbol,orderId=orderid)
    #result.time = datetime.fromtimestamp(int(result.time / 1000))
    result.updateTime = datetime.fromtimestamp(int(result.updateTime / 1000))
    time.sleep(0.5)
    return result
def geteth1m():
    last = Ethusdt1m.query.get(Ethusdt1m.query.count()).closetime

    if last is not None:
        now = datetime.now()
        a = 0
        while (now - last).seconds > 60 or (now - last).days > 0:
            starttime = int(last.timestamp()*1000) + 1
            endtime = int(now.timestamp()*1000)
            res = getstick(starttime=starttime,endtime=endtime,limit=600)
            coun = len(res)
            for r in res:

                eth = Ethusdt1m(opentime=r.openTime, openpr=r.open, hightpr=r.high, lowpr=r.low, closepr=r.close,
                                bustur=r.quoteAssetVolume, closetime=r.closeTime, busvolu=r.numTrades, busnum=r.volume,
                                actbustur=r.takerBuyBaseAssetVolume, actbusvolu=r.takerBuyQuoteAssetVolume)
                db.session.add(eth)
            db.session.commit()
            starstr = last
            last = Ethusdt1m.query.get(Ethusdt1m.query.count()).closetime
            now = datetime.now()
            endstr = datetime.strftime(last,'%Y-%m-%d %H:%M:%S')
            starstr = datetime.strftime(starstr, '%Y-%m-%d %H:%M:%S')
            print('增加时间从：%s到%s'%(starstr,endstr),"共%d条"%coun)
            a = a+coun

        endstr = datetime.strftime(last,'%Y-%m-%d %H:%M:%S')
        print('最新数据记录是：',endstr,' 本次共更新%d条数据'%a)
        return a
    print('没有查询到记录，运行flask forge构建数据库')


