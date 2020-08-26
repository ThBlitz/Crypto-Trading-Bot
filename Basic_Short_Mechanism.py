import blitz_trade_tools

options={
    'HeyBinance':{
        'BTCUSDT':'1h'
    }
}

keys={
    'HeyBinance':{
        'api_key': 'SDHGKA---------->>> YOUR API KEY <<<----------AJGHLAKK' ,
        'secret_key': 'DAHSGLAKHD----------->>> YOUR SECRET KEY <<<-------------AJKHGASKJD'
    }
}

candles=blitz_trade_tools.Candle_Sticks_Ticker()
candles.set(options=options,tick_rate=4,_yield_=True)

options = {
    'HeyBinance':{
        'BTC','USDT','BNB'
    }
}

account_info=blitz_trade_tools.Account_info()
account_info.set(options=options,keys=keys)

options={
    'HeyBinance':{
        'BTCUSDT'
    }
}

place_order=blitz_trade_tools.Place_Order()
place_order.set(trade_type='market_order',options=options,keys=keys)

checker=blitz_trade_tools.Manage_Order()
checker.set(keys=keys)

price_level=blitz_trade_tools.Price_Levels()
price_level.set('HeyBinance','BTCUSDT',11391.98)

feed=blitz_trade_tools.Feedback()

candles.record_feedback(feed)
account_info.record_feedback(feed)
place_order.record_feedback(feed)
checker.record_feedback(feed)

trade = blitz_trade_tools.BUY_or_SELL()
trade.set(account_info,place_order,checker)

_c_=blitz_trade_tools.Candle_Sticks_Manager()
saver=blitz_trade_tools.Save_Load_Data('D:\\', 'test')

a = account_info.run()
a=a['HeyBinance']['BTC']
print(a)

shorted=False

for x in candles.run():

    price=x['HeyBinance']['BTCUSDT'].close

    _c_.record_ticks(x,saver)

    print(price)
    print(price_level.compare(price))

    if price_level.compare(price) == 'none':
        if shorted == False:
            a,b,c=trade.run(price_ticks=x,BUY_or_SELL='SELL',assetA_assetB='BTC_USDT',precision=5,quantity_in_percentage=.98)
            print(a)
            print(b)
            print(c)
            shorted=True

    print(feed.feedback)
    feed.reset()
