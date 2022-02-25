import time
import logging
from binance.error import ClientError
from binance.futures import Futures as Client
from binance.lib.utils import config_logging
from datetime import datetime
from sqlalchemy import extract
from watchlist.models import User, Movie, Orders, Anguser

config_logging(logging, logging.DEBUG)
futures_client = Client()
def getmprice():
    eth = futures_client.ticker_24hr_price_change("ETHUSDT")
    btc = futures_client.ticker_24hr_price_change("BTCUSDT")
    doge = futures_client.ticker_24hr_price_change("DOGEUSDT")
    logging.info('\n eth=%s \n btc=%s \n doge=%s' % (eth, btc, doge))
    time.sleep(0.5)

def wp():

    key = "oK8MPcduJ05ej3drFXWmXI7M4N9UZAmwkHqrDXwTL01oeHFN0WXfjWwcbS2mlsqF"
    secret = "yilX8DnKHOVgqVEurOpn8lHE7YuWXgkK0a5l1wl8qCbcj6sw6uKTJe0zcBFNM0ME"

    client = Client(key, secret)

    try:
        response = client.account(recvWindow=6000)
        logging.info(response)
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )
    print('ok')
def getfig():
    today = datetime.now()
    userid = 3
    if userid:
        order = Orders.query.filter(extract('year', Orders.ordertime) == today.year,
                                    extract('month', Orders.ordertime) == today.month,
                                    extract('day', Orders.ordertime) == today.day,
                                    Orders.userid == userid).all()
    print('ll')

if __name__=='__main__':
    getfig()
    #wp()
    #getmprice()

