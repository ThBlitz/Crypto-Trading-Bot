import json
import urllib
import time
import requests
import datetime
import hmac
import hashlib
import dateparser
import pytz
import pandas as pd

exchangeendpoint='https://api.binance.com'

querystring={
    'GetServerStatus':'/wapi/v3/systemStatus.html',
    'GetPriceTicker':'/api/v3/ticker/price',
    'GetCandleStickData':'/api/v3/klines',
    'GetAccountSnapshot':'/sapi/v1/accountSnapshot',
    'PlaceNewMarketOrder':'/api/v3/order',
    'PlaceNewLimitOrder':'/api/v3/order',
    'CancelaOrder':'/api/v3/order',
    'CancelAllOrders':'api/v3/openOrders',
    'CheckOrderStatus':'/api/v3/order',
    'CheckForCurrentOpenOrders':'/api/v3/openOrders',
    'GetAccountInfo':'/api/v3/account'
}

def delete(exchangeendpoint, querystring, parameter,header):
    info = requests.delete(f'{exchangeendpoint}{querystring}', params=parameter, headers=header)
    info = json.loads(info.text)
    return info

def post(exchangeendpoint,querystring,parameter,header):
    info=requests.post(f'{exchangeendpoint}{querystring}',params=parameter,headers=header)
    info=json.loads(info.text)
    return info

def sign(message,keys):
    message=urllib.parse.urlencode(message)
    hashed = hmac.new(keys['secretkey'].encode(), message.encode(), digestmod=hashlib.sha256)
    signedmessage = hashed.hexdigest()
    return signedmessage

def date_to_milliseconds(date_str):
    """Convert UTC date to milliseconds

    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/

    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)

def get(exchangeendpoint,querystring,parameter,header):
    info = requests.get(f'{exchangeendpoint}{querystring}', params=parameter, headers=header)
    info = json.loads(info.text)
    return info

def GetServerStatus():
    try:
        status = get(exchangeendpoint,querystring['GetServerStatus'],parameter=None,header=None)
    except:
        status=1

    return status

def GetPriceTicker(ListOfCoins):
    info=[]
    for everycoin in ListOfCoins:
        parameter={
            'symbol':everycoin
        }
        info.append(get(exchangeendpoint,querystring['GetPriceTicker'],parameter,header=None))
        time.sleep(0.08)

    return info

def GetCandleStickData(ListOfCoins,ListOfIntervals,fromwhen_date_string,tillwhen_date_string):


    if isinstance(fromwhen_date_string,list):
        fromwhen_date_string=fromwhen_date_string[0]
    if isinstance(tillwhen_date_string,list):
        tillwhen_date_string=tillwhen_date_string[0]
    if isinstance(fromwhen_date_string,str):
        fromwhen=date_to_milliseconds(fromwhen_date_string)
    else:
        fromwhen=fromwhen_date_string
    if isinstance(tillwhen_date_string,str):
        tillwhen=date_to_milliseconds(tillwhen_date_string)
    else:
        tillwhen=tillwhen_date_string
    intervalsinmilli = {'1m': 1 * 60 * 1000, '3m': 3 * 60 * 1000, '5m': 5 * 60 * 1000, '15m': 15 * 60 * 1000,
                        '30m': 30 * 60 * 1000, '1h': 1 * 60 * 60 * 1000, '2h': 2 * 60 * 60 * 1000,
                        '4h': 4 * 60 * 60 * 1000,
                        '6h': 6 * 60 * 60 * 1000, '8h': 8 * 60 * 60 * 1000, '12h': 12 * 60 * 60 * 1000,
                        '1d': 1 * 24 * 60 * 60 * 1000,
                        '3d': 3 * 24 * 60 * 60 * 1000, '1w': 1 * 7 * 24 * 60 * 60 * 1000
                        }
    info={}
    for everycoin in ListOfCoins:
        for everyintervals in ListOfIntervals:
            data=[]
            parameter={
                'symbol':everycoin,
                'interval':everyintervals,
                'startTime':fromwhen,
                'endTime':tillwhen,
                'limit':1000
            }
            inter = parameter['interval']
            intervals = (parameter['endTime'] - parameter['startTime']) / intervalsinmilli[f'{inter}']
            # print(f'Total_intervals : {intervals}')
            if intervals >= 1000:
                if (intervals / 1000) < (intervals % 1000):
                    order = (int(intervals / 1000)) + 1
                else:
                    order = int(intervals / 1000)
                diff = parameter['endTime'] - parameter['startTime']
                addition = int(diff / order)
                end = parameter['endTime']
                parameter['endTime'] = parameter['startTime']
                for i in range(order):
                    if i%2 ==0 and i!=0:
                        print(f'Intervals_downloaded --->> {(i/order)*100}%')
                    parameter['endTime'] = parameter['endTime'] + addition
                    if (parameter['endTime'] > end):
                        parameter['endTime'] = end
                    connect=get(exchangeendpoint,querystring['GetCandleStickData'],parameter,header=None)
                    for j in connect:
                        data.append(j)
                    parameter['startTime'] = parameter['endTime']
                    time.sleep(0.08)
            else:
                data = get(exchangeendpoint,querystring['GetCandleStickData'],parameter,header=None)
                time.sleep(0.08)
            info.update({f'{everycoin}_{everyintervals}':data})


    return info

def GetAccountSnapshot(AccountType,ApiKey,SecretKey,timestamp=None):
    if isinstance(ApiKey,list):
        ApiKey = ApiKey[0]
    if isinstance(AccountType,list):
        AccountType=AccountType[0]
    if isinstance(SecretKey,list):
        SecretKey=SecretKey[0]
    if timestamp==None:
        timestamp=time.time()*1000
    timestamp=int(timestamp)
    parameter={
        'type':AccountType,
        'timestamp':timestamp
    }
    keys={
        'apikey':ApiKey,
        'secretkey':SecretKey
    }
    signature=sign(parameter,keys)
    parameter.update({'signature':signature})
    info=get(exchangeendpoint,querystring['GetAccountSnapshot'],parameter,header={"X-MBX-APIKEY": keys['apikey']})
    return info

def PlaceNewMarketOrder(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,BUY_or_SELL,quantity_Of_BTC_or_BNB_or_ETH_etc,
                        Set_Any_Unique_Order_ID_in_string_format,ApiKey,SecretKey):
    if isinstance(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,list):
        BTCUSDT_or_BNBUSDT_or_BTCBNB_etc=BTCUSDT_or_BNBUSDT_or_BTCBNB_etc[0]
    if isinstance(BUY_or_SELL,list):
        BUY_or_SELL=BUY_or_SELL[0]
    if isinstance(quantity_Of_BTC_or_BNB_or_ETH_etc,list):
        quantity_Of_BTC_or_BNB_or_ETH_etc=quantity_Of_BTC_or_BNB_or_ETH_etc[0]
    if isinstance(Set_Any_Unique_Order_ID_in_string_format,list):
        Set_Any_Unique_Order_ID_in_string_format=Set_Any_Unique_Order_ID_in_string_format[0]
    if isinstance(ApiKey,list):
        ApiKey=ApiKey[0]
    if isinstance(SecretKey,list):
        SecretKey=SecretKey[0]
    timestamp=date_to_milliseconds('now UTC')
    parameter={
        'symbol':BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,
        'side':BUY_or_SELL,
        'type':'MARKET',
        'quantity':quantity_Of_BTC_or_BNB_or_ETH_etc,
        'newClientOrderId':Set_Any_Unique_Order_ID_in_string_format,
        'timestamp':timestamp
    }
    keys = {
        'apikey': ApiKey,
        'secretkey': SecretKey
    }
    signature=sign(parameter,keys)
    parameter.update({'signature':signature})
    info=post(exchangeendpoint,querystring['PlaceNewMarketOrder'],parameter,header={"X-MBX-APIKEY": keys['apikey']})

    if info['status']=='FILLED':
        info_={
            'order_id':info['clientOrderId'],
            'status':info['status'],
            'time':info['transactTime'],
            'price':info['fills'][0]['price'],
            'quantity':info['fills'][0]['qty'],
            'commission':info['fills'][0]['commission'],
            'commission_asset':info['fills'][0]['commissionAsset'],
            'order_id_':info['orderId'],
            'trade_id':info['fills'][0]['tradeId']
        }

    elif info['status']=='NEW':
        info_ = {
            'order_id': info['clientOrderId'],
            'order_id_': info['orderId'],
            'status': info['status'],
            'time': info['updateTime'],
            'buy_or_sell': info['side'],
            'price': info['price'],
            'quantity': info['origQty']
        }

    else:
        info_=info

    return info_

def PlaceNewLimitOrder(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,BUY_or_SELL,quantity_Of_BTC_or_BNB_or_ETH_etc,Price,
                      Set_Any_Unique_Order_ID_in_string_format,ApiKey,SecretKey, timeinforce_GTC_or_IOK_or_FOK='GTC'):
    if isinstance(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,list):
        BTCUSDT_or_BNBUSDT_or_BTCBNB_etc=BTCUSDT_or_BNBUSDT_or_BTCBNB_etc[0]
    if isinstance(BUY_or_SELL,list):
        BUY_or_SELL=BUY_or_SELL[0]
    if isinstance(quantity_Of_BTC_or_BNB_or_ETH_etc,list):
        quantity_Of_BTC_or_BNB_or_ETH_etc=quantity_Of_BTC_or_BNB_or_ETH_etc[0]
    if isinstance(Set_Any_Unique_Order_ID_in_string_format,list):
        Set_Any_Unique_Order_ID_in_string_format=Set_Any_Unique_Order_ID_in_string_format[0]
    if isinstance(ApiKey,list):
        ApiKey=ApiKey[0]
    if isinstance(SecretKey,list):
        SecretKey=SecretKey[0]
    if isinstance(Price,list):
        Price=Price[0]
    timestamp = date_to_milliseconds('now UTC')
    parameter = {
        'symbol': BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,
        'side': BUY_or_SELL,
        'type': 'LIMIT',
        'timeInForce':timeinforce_GTC_or_IOK_or_FOK,
        'price':Price,
        'quantity': quantity_Of_BTC_or_BNB_or_ETH_etc,
        'newClientOrderId': Set_Any_Unique_Order_ID_in_string_format,
        'timestamp': timestamp
    }
    keys = {
        'apikey': ApiKey,
        'secretkey': SecretKey
    }
    signature = sign(parameter, keys)
    parameter.update({'signature': signature})
    info = post(exchangeendpoint, querystring['PlaceNewLimitOrder'], parameter,
                header={"X-MBX-APIKEY": keys['apikey']})

    if info['status']=='FILLED':
        info_={
            'order_id':info['clientOrderId'],
            'order_id_': info['orderId'],
            'status':info['status'],
            'time':info['transactTime'],
            'buy_or_sell':info['side'],
            'price':info['fills'][0]['price'],
            'quantity':info['fills'][0]['qty'],
            'commission':info['fills'][0]['commission'],
            'commission_asset':info['fills'][0]['commissionAsset'],
            'trade_id':info['fills'][0]['tradeId']
        }

    elif info['status']=='NEW':
        info_={
            'order_id': info['clientOrderId'],
            'order_id_': info['orderId'],
            'status': info['status'],
            'time': info['updateTime'],
            'buy_or_sell': info['side'],
            'price': info['price'],
            'quantity': info['origQty']
        }

    elif info['status']=='CANCELED':
        info_ = {
            'order_id': info['clientOrderId'],
            'order_id_': info['orderId'],
            'status': info['status'],
            'time': info['updateTime'],
            'buy_or_sell': info['side'],
            'price': info['price'],
            'quantity': info['origQty']
        }
    else:
        info_=info

    return info_

def CancelaOrder(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,Your_Unique_Order_ID,ApiKey,SecretKey):
    if isinstance(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc, list):
        BTCUSDT_or_BNBUSDT_or_BTCBNB_etc = BTCUSDT_or_BNBUSDT_or_BTCBNB_etc[0]
    if isinstance(Your_Unique_Order_ID, list):
        Your_Unique_Order_ID = Your_Unique_Order_ID[0]
    if isinstance(ApiKey, list):
        ApiKey = ApiKey[0]
    if isinstance(SecretKey, list):
        SecretKey = SecretKey[0]
    timestamp=date_to_milliseconds('now utc')
    parameter={
        'symbol':BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,
        'origClientOrderId':Your_Unique_Order_ID,
        'timestamp':timestamp
    }
    keys = {
        'apikey': ApiKey,
        'secretkey': SecretKey
    }
    signature = sign(parameter, keys)
    parameter.update({'signature': signature})
    info = delete(exchangeendpoint, querystring['CancelaOrder'], parameter,
                header={"X-MBX-APIKEY": keys['apikey']})

    return info

def CancelAllOrders(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,ApiKey,SecretKey):
    timestamp = date_to_milliseconds('now utc')
    parameter = {
        'symbol': BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,
        'timestamp': timestamp
    }
    keys = {
        'apikey': ApiKey,
        'secretkey': SecretKey
    }
    signature = sign(parameter, keys)
    parameter.update({'signature': signature})
    info = delete(exchangeendpoint, querystring['CancelAllOrders'], parameter,
                  header={"X-MBX-APIKEY": keys['apikey']})
    return info

def CheckOrderStatus(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,Your_Unique_Order_ID,ApiKey,SecretKey):

    if isinstance(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,list):
        BTCUSDT_or_BNBUSDT_or_BTCBNB_etc=BTCUSDT_or_BNBUSDT_or_BTCBNB_etc[0]
    if isinstance(Your_Unique_Order_ID,list):
        Your_Unique_Order_ID=Your_Unique_Order_ID[0]
    if isinstance(ApiKey,list):
        ApiKey=ApiKey[0]
    if isinstance(SecretKey,list):
        SecretKey=SecretKey[0]

    timestamp = date_to_milliseconds('now utc')
    parameter = {
        'symbol': BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,
        'origClientOrderId': Your_Unique_Order_ID,
        'timestamp': timestamp
    }
    keys = {
        'apikey': ApiKey,
        'secretkey': SecretKey
    }
    signature = sign(parameter, keys)
    parameter.update({'signature': signature})
    info = get(exchangeendpoint, querystring['CheckOrderStatus'], parameter,
                  header={"X-MBX-APIKEY": keys['apikey']})

    try:
        if info['status'] == 'FILLED':
            info_ = {
                'order_id': info['clientOrderId'],
                'order_id_': info['orderId'],
                'status': info['status'],
                'time': info['time'],
                'buy_or_sell': info['side'],
                'price': info['price'],
                'quantity': info['origQty'],
            }

        elif info['status'] == 'NEW':
            info_ = {
                'order_id': info['clientOrderId'],
                'order_id_': info['orderId'],
                'status': info['status'],
                'time': info['updateTime'],
                'buy_or_sell': info['side'],
                'price': info['price'],
                'quantity': info['origQty']
            }
        elif info['status'] == 'CANCELED':
            info_ = {
                'order_id': info['clientOrderId'],
                'order_id_': info['orderId'],
                'status': info['status'],
                'time': info['updateTime'],
                'buy_or_sell': info['side'],
                'price': info['price'],
                'quantity': info['origQty']
            }
        else:
            info_ = info
    except:
        info_=info
    return info_

def CheckForCurrentOpenOrders(ALL_BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,ApiKey,SecretKey):
    timestamp = date_to_milliseconds('now utc')
    if ALL_BTCUSDT_or_BNBUSDT_or_BTCBNB_etc == 'ALL':
        parameter={
            'timestamp': timestamp
        }
    else:
        parameter={
            'symbol':ALL_BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,
            'timestamp':timestamp
        }
    keys = {
        'apikey': ApiKey,
        'secretkey': SecretKey
    }
    signature = sign(parameter, keys)
    parameter.update({'signature': signature})
    info = get(exchangeendpoint, querystring['CheckForCurrentOpenOrders'], parameter,
               header={"X-MBX-APIKEY": keys['apikey']})
    return info

def GetAccountInfo(ApiKey,SecretKey,assets_to_get):
    if isinstance(ApiKey,list):
        ApiKey=ApiKey[0]
    if isinstance(SecretKey,list):
        SecretKey=SecretKey[0]
    timestamp = date_to_milliseconds('now utc')
    parameter={
        'timestamp':timestamp
    }
    keys = {
        'apikey': ApiKey,
        'secretkey': SecretKey
    }
    signature = sign(parameter, keys)
    parameter.update({'signature': signature})
    info = get(exchangeendpoint, querystring['GetAccountInfo'], parameter,
               header={"X-MBX-APIKEY": keys['apikey']})

    info = info['balances']
    assets_={}
    for i in info:
        if i['asset'] in assets_to_get:
            assets_.update({i[f'asset']: i['free']})
    info=assets_
    return info

def GetCandleStickDataOHLCV(ListOfCoins,ListOfIntervals,fromwhen_date_string=None,tillwhen_date_string=None):

    rawdata=GetCandleStickData(ListOfCoins,ListOfIntervals,fromwhen_date_string,tillwhen_date_string)
    info={}
    for eachcoin in ListOfCoins:
        for eachinterval in ListOfIntervals:
            open = []
            high = []
            low = []
            close = []
            volume = []
            datetimes = []
            for eachdata in rawdata.get(f'{eachcoin}_{eachinterval}'):
                datetimes.append(datetime.datetime.fromtimestamp(eachdata[0] / 1000.0))
                open.append(eachdata[1])
                high.append(eachdata[2])
                low.append(eachdata[3])
                close.append(eachdata[4])
                volume.append(eachdata[5])
            df = pd.DataFrame(list(zip(datetimes, open, high, low, close, volume)),
                                  columns=['time', 'open', 'high', 'low', 'close', 'volume'])
            open.clear()
            close.clear()
            high.clear()
            low.clear()
            high.clear()
            datetimes.clear()
            volume.clear()
            info.update({f'{eachcoin}_{eachinterval}':df})

    return info




