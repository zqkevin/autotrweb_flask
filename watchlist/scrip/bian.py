import time
import logging
from binance.error import ClientError
from binance.futures import Futures as Client
from binance.lib.utils import config_logging
config_logging(logging, logging.INFO)
futures_client = Client()

def getprice(symbol: str = None):
    try:
        symbol = symbol+'USDT'
        re = futures_client.ticker_24hr_price_change(symbol)

        return re
    except:
        return False
def getacc(key, secret):
    client = Client(key, secret)
    try:
        response = client.account(recvWindow=6000)
        if response:
            return response
        return False
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )
        return False
# if __name__=='__main__':
#     eth = getprice('ETHUSDT')
#     logging.info(eth)
