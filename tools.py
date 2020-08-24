import time
import os
import pandas as pd
####################################################################################################################
###  CLEAN CODE ### MINIMUM ERRORS ###

def __id__():
    time.sleep(0.08)
    return int(time.time() * 1000)

# options={
#         'HeyBinance':{'BTCUSDT','ETHUSDT'}
# }

class Price_Ticker:

    def __init__(self,unique_name='none'):
        self.id=f'price_ticker_{__id__()}'
        self.name=unique_name

    def set(self,options,tick_rate=1.0,_yield_=True):
        self.options=options
        self.tick_rate=tick_rate
        self._yield_=_yield_

    def info(self):
        return {
            'name':self.name,
            'id':self.id,
            'options':self.options,
            'tick_rate':self.tick_rate,
            'yield':self._yield_
        }

    def restore(self,info):
        self.name=info['name']
        self.id=info['id']
        self.options=info['options']
        self.tick_rate=info['tick_rate']
        self._yield_=info['yield']

    def save(self,save_obj):
        save_obj.save(self.info(),self.name)

    def load(self,save_obj,name):
        info=save_obj.load(name,self.id)
        self.restore(info)

    def run(self):
        if self.tick_rate < 0.1:
            self.tick_rate=0.1
            print('MIN TICK RATE IS 0.1 TO PREVENT SERVER BAN \n')

        for option in self.options:
            exec(f'import {option}')

        try :

            while(True):
                last_time=time.time()
                self.feedback={}
                self.feedback.update({'id':self.id})
                self.feedback.update({'tick_rate':self.tick_rate})

                return_price={}

                for option in self.options:

                    self.symbols=self.options[f'{option}']
                    self.symbol_price={}

                    symbol_list=[]
                    for self.symbol in self.symbols:
                        symbol_list.append(self.symbol)

                    self.price_list=eval(f'{option}.GetPriceTicker({symbol_list})')

                    for price in self.price_list:
                        self.symbol_price.update({price['symbol']: price['price']})

                    return_price.update({f'{option}':self.symbol_price})

                time.sleep(self.tick_rate)
                loop_took = time.time() - last_time
                self.feedback.update({'time':time.time()})
                self.feedback.update({'loop_took':loop_took})
                if self._yield_==False:
                    break

                yield return_price,self.feedback

            return return_price, self.feedback

        except:
            pass

# options={
#     'HeyBinance':{'BTC','USDT','BNB'}
# }
#
# Keys={
#     'HeyBinance':{'api_key':'12345','secret_key':'1234566'}
# }

class Account_info:
    def __init__(self,unique_name='none'):
        self.name=unique_name
        self.type=['SPOT']
        self.id= f'account_info_{__id__()}'

    def set(self,options,keys):
        self.options=options
        self.keys=keys

    def info(self):
        return {
            'name':self.name,
            'id':self.id,
            'options': self.options,
            'keys': self.keys,
            'account_type': self.type
        }

    def restore(self,info):
        self.name=info['name']
        self.id=info['id']
        self.options=info['options']
        self.keys=info['keys']
        self.type=info['account_type']

    def save(self,save_obj):
        save_obj.save(self.info(),self.name)

    def load(self,save_obj,name):
        info=save_obj.load(name,self.id)
        self.restore(info)

    def run(self):
        last_time = time.time()
        self.feedback = {}
        self.feedback.update({'id':self.id})
        self.feedback.update({'options':self.options})

        self.assets={}
        for self.option in self.options:

            exec(f'import {self.option}')
            self.api_key=[self.keys[f'{self.option}'][f'api_key']]
            self.secret_key=[self.keys[f'{self.option}'][f'secret_key']]
            assets_to_get=self.options[f'{self.option}']
            info=eval(f"{self.option}.GetAccountInfo({self.api_key},{self.secret_key},{assets_to_get})")

            self.assets.update( {f'{self.option}':info})

        loop_took=time.time()-last_time
        self.feedback.update({'loop_took':loop_took})

        return self.assets,self.feedback

####################################################################################################################

# option={
#     'HeyBinance': {'BTCUSDT'}
# }
#
# Keys={
#     'HeyBinance':{'api_key':'12345','secret_key':'1234566'}
# }
# trade_type='market_order'

class Place_Order():
    def __init__(self,unique_name='none'):
        self.id=f'place_order_{__id__()}'
        self.name=unique_name
        self.trade_type = None
        self.option = None
        self.keys=None

    def set(self,trade_type,option,keys):
        self.option=option
        self.trade_type=trade_type
        self.keys=keys

    def info(self):
        return {
            'name':self.name,
            'id':self.id,
            'options':self.option,
            'trade_type':self.trade_type,
            'keys':self.keys
        }

    def restore(self,info):
        self.name=info['name']
        self.id=info['id']
        self.option=info['options']
        self.trade_type=info['trade_type']
        self.keys=info['keys']

    def save(self,save_obj):
        save_obj.save(self.info(),self.name)

    def load(self,save_obj,name):
        info=save_obj.load(name,self.id)
        self.restore(info)

    def run(self,BUY_or_SELL=None,quantity=0.001,price=None):
        last_time=time.time()
        self.price=price
        self.feedback={}
        self.info_={}

        for option in self.option:
            exec(f'import {option}')

        if self.price==None:
            self.trade_type='market_order'

        if self.trade_type == 'market_order':
            self.price=None
            for option in self.option:
                for symbol in self.option[option]:
                    self.order_id=[f'market_order_id_{__id__()}']
                    symbol=[symbol]
                    self.quantity=[quantity]
                    self.BUY_or_SELL=[BUY_or_SELL]
                    self.api_key = [self.keys[f'{option}'][f'api_key']]
                    self.secret_key = [self.keys[f'{option}'][f'secret_key']]
                    info=eval(f'{option}.PlaceNewMarketOrder({symbol},{self.BUY_or_SELL},{self.quantity},{self.order_id},{self.api_key},{self.secret_key})')
                    self.info_.update({f'{option}': {symbol[0]:info}})

        elif self.trade_type == 'limit_order':
            for option in self.option:
                for symbol in self.option[option]:
                    self.order_id=[f'limit_order_id_{__id__()}']
                    symbol = [symbol]
                    self.quantity = [quantity]
                    self.BUY_or_SELL = [BUY_or_SELL]
                    self.api_key = [self.keys[f'{option}'][f'api_key']]
                    self.secret_key = [self.keys[f'{option}'][f'secret_key']]
                    info=eval(f'{option}.PlaceNewLimitOrder({symbol},{self.BUY_or_SELL},{self.quantity},{self.price},{self.order_id},{self.api_key},{self.secret_key})')
                    self.info_.update({f'{option}': {symbol[0]: info}})

        self.feedback.update({'id':self.id})
        self.feedback.update({'options':self.option})
        self.feedback.update({'trade_type':self.trade_type})
        loop_took=time.time()-last_time
        self.feedback.update({'loop_took':loop_took})

        return self.info_ , self.feedback

# option={
#     'HeyBinance':{'BTCUSDT'}
# }
#
# keys={
#     'HeyBinance':{ 'api_key': '12345','secret_key': '12345556'}
# }

class Check_Order:
    def __init__(self,unique_name='name'):
        self.name=unique_name
        self.id = f'check_order_{__id__()}'

    def set(self,option,keys):
        self.option=option
        self.keys=keys

    def info(self):
        return {
            'name':self.name,
            'id':self.id,
            'options':self.option,
            'keys':self.keys
        }

    def restore(self, info):
        self.name = info['name']
        self.id = info['id']
        self.option = info['options']
        self.keys = info['keys']

    def save(self, save_obj):
        save_obj.save(self.info(), self.name)

    def load(self, save_obj, name):
        info = save_obj.load(name, self.id)
        self.restore(info)

    def run(self,place_order_output):
        last_time=time.time()
        self.feedback={}
        for option in self.option:
            exec(f'import {option}')

        self.info_={}

        for option in self.option:
            asset_to_get=place_order_output[option]
            for symbol in self.option[option]:
                _info=asset_to_get[symbol]
                self.order_id=[_info['order_id']]
                self.symbol=[symbol]
                self.api_key = [self.keys[f'{option}'][f'api_key']]
                self.secret_key = [self.keys[f'{option}'][f'secret_key']]
                info=eval(f'{option}.CheckOrderStatus({self.symbol},{self.order_id},{self.api_key},{self.secret_key})')
                self.info_.update({f'{option}': {symbol: info}})

            self.feedback.update({'id':self.id})
            self.feedback.update({'options':self.option})
            loop_took=time.time()-last_time
            self.feedback.update({'loop_took':loop_took})
            return self.info_,self.feedback

class Cancel_Order:
    def __init__(self,unique_name='none'):
        self.name=unique_name
        self.id = f'cancel_order_{__id__()}'

    def set(self, option, keys):
        self.option = option
        self.keys = keys

    def info(self):
        return {
            'id': self.id,
            'options': self.option,
            'keys': self.keys
        }

    def restore(self, info):
        self.name = info['name']
        self.id = info['id']
        self.option = info['options']
        self.keys = info['keys']

    def save(self, save_obj):
        save_obj.save(self.info(), self.name)

    def load(self, save_obj, name):
        info = save_obj.load(name, self.id)
        self.restore(info)

    def run(self, place_order_output):
        last_time = time.time()
        self.feedback = {}
        for option in self.option:
            exec(f'import {option}')

        self.info_ = {}

        for option in self.option:
            asset_to_get = place_order_output[option]
            for symbol in self.option[option]:
                _info = asset_to_get[symbol]
                self.order_id = [_info['order_id']]
                self.symbol = [symbol]
                self.api_key = [self.keys[f'{option}'][f'api_key']]
                self.secret_key = [self.keys[f'{option}'][f'secret_key']]
                info=eval(f'{option}.CancelaOrder({self.symbol},{self.order_id},{self.api_key},{self.secret_key})')
                self.info_.update({f'{option}': {symbol: info}})

        self.feedback.update({'id': self.id})
        self.feedback.update({'options': self.option})
        loop_took = time.time() - last_time
        self.feedback.update({'loop_took': loop_took})
        return self.info_, self.feedback

# options={
#     'HeyBinance':{
#         'BTCUSDT':'1h','ETHUSDT':'1m'
#     }
# }

####################################################################################################################
###  CLEAN CODE ### MINIMUM ERRORS ###

class Candle_Sticks:
    def __init__(self):
        self.id=f'candle_stick_{__id__()}'

    def set(self,option,symbol,interval,_time_,open,high,low,close,volume,status):
        open=float(open)
        close=float(close)
        high=float(high)
        low=float(low)
        volume=float(volume)
        self.option=option
        self.symbol=symbol
        self.interval=interval
        self.time=_time_
        self.open=open
        self.high=high
        self.low=low
        self.close=close
        self.volume=volume
        self.status=status
        if open-close < 0:
            self.colour='green'
        elif open-close > 0:
            self.colour='red'
        else:
            self.colour='red'

    def info(self):
        return {
            'id':self.id,
            'option':self.option,
            'symbol':self.symbol,
            'interval':self.interval,
            'time':self.time,
            'open':self.open,
            'high':self.high,
            'low':self.low,
            'close':self.close,
            'volume':self.volume,
            'colour':self.colour,
            'status':self.status
        }

    def restore(self,info):
        self.id=info['id']
        self.option=info['option']
        self.symbol=info['symbol']
        self.interval=info['interval']
        self.time=info['time']
        self.open=info['open']
        self.high=info['high']
        self.low=info['low']
        self.close=info['close']
        self.volume=info['volume']
        self.colour=info['colour']
        self.status=info['status']

class Candle_Sticks_Ticker:
    def __init__(self,unique_name='none'):
        self.name=unique_name
        self.id=f'candle_stick_ticker_{__id__()}'
        self.intervalsinmilli = {'1m': 1 * 60 * 1000, '3m': 3 * 60 * 1000, '5m': 5 * 60 * 1000, '15m': 15 * 60 * 1000,
                        '30m': 30 * 60 * 1000, '1h': 1 * 60 * 60 * 1000, '2h': 2 * 60 * 60 * 1000,
                        '4h': 4 * 60 * 60 * 1000,
                        '6h': 6 * 60 * 60 * 1000, '8h': 8 * 60 * 60 * 1000, '12h': 12 * 60 * 60 * 1000,
                        '1d': 1 * 24 * 60 * 60 * 1000,
                        '3d': 3 * 24 * 60 * 60 * 1000, '1w': 1 * 7 * 24 * 60 * 60 * 1000
                        }

    def set(self,options,tick_rate=4,_yield_=True):
        self._yield_=_yield_
        self.options=options
        self.tick_rate=tick_rate
        self.prev_time={}
        self.now_time={}
        for option in options:
            self.prev_time.update({option:{}})
            self.now_time.update({option:{}})
            for symbol in self.options[option]:

                self.prev_time[option].update({symbol:None})
                self.now_time[option].update({symbol:None})

    def info(self):
        return {
            'name':self.name,
            'id':self.id,
            'options':self.options,
            'tick_rate':self.tick_rate,
            'yield':self._yield_
        }

    def restore(self,info):
        self.name=info['name']
        self.id=info['id']
        self.options=info['options']
        self.tick_rate=info['tick_rate']
        self._yield_=info['yield']

    def save(self, save_obj):
        save_obj.save(self.info(), self.name)

    def load(self, save_obj, name):
        info = save_obj.load(name, self.id)
        self.restore(info)

    def run(self):

        self.feedback = {}
        for option in self.options:
            exec(f'import {option}')

        prev_time={}
        now_time={}
        candle_sticks={}
        for option in self.options:
            prev_time.update({option: {}})
            now_time.update({option: {}})
            candle_sticks.update({option:{}})
            for symbol in self.options[option]:
                prev_time[option].update({symbol: None})
                now_time[option].update({symbol: None})
                candle_sticks[option].update({symbol:None})

        while(True):

            last_time = time.time()
            self.info_ = {}

            for option in self.options:
                self.info_.update({option:{}})
                for symbol in self.options[option]:
                    interval=self.options[option][symbol]
                    symbol=[symbol]
                    till_when=time.time()*1000
                    from_when=till_when-(2*self.intervalsinmilli[interval])
                    interval=[interval]

                    while(True):

                        info=eval(f'{option}.GetCandleStickDataOHLCV({symbol},{interval},{int(from_when)},{int(till_when)})')

                        try:
                            df = info[f'{symbol[0]}_{interval[0]}']
                            prev_time[option][symbol[0]]=df['time'][0]
                            now_time[option][symbol[0]]=df['time'][1]
                            try_again=False
                        except:
                            try_again=True
                            print('___S_E_R_V_O_R___U_N - R_E_S_P_O_N_S_I_V_S___')
                            time.sleep(1)
                        if try_again==False:
                            break

                    symbol=symbol[0]

                    if self.now_time[option][symbol]==None and self.prev_time[option][symbol]==None:

                        self.now_time[option][symbol]=now_time[option][symbol]
                        self.prev_time[option][symbol]=prev_time[option][symbol]
                        candle_sticks[option][symbol]= Candle_Sticks()
                        candle_sticks[option][symbol].set(option,symbol, interval[0], df['time'][1], df['open'][1], df['high'][1],
                                             df['low'][1], df['close'][1], df['volume'][1],'in_complete')
                        self.info_[option].update({symbol:candle_sticks[option][symbol]})

                    elif prev_time[option][symbol]==self.now_time[option][symbol]:

                        candle_sticks[option][symbol].set(option,symbol, interval[0], df['time'][1], df['open'][1],
                                                          df['high'][1],
                                                          df['low'][1], df['close'][1], df['volume'][1], 'complete')

                        self.info_[option].update({symbol:candle_sticks[option][symbol]})
                        self.now_time[option][symbol]=now_time[option][symbol]
                        self.prev_time[option][symbol]=prev_time[option][symbol]
                        candle_sticks[option][symbol] = Candle_Sticks()
                        candle_sticks[option][symbol].set(option,symbol,interval[0],df['time'][1],df['open'][1],df['high'][1],
                                             df['low'][1],df['close'][1],df['volume'][1],'in_complete')

                    elif prev_time[option][symbol]==self.prev_time[option][symbol] and now_time[option][symbol]==self.now_time[option][symbol]:
                        candle_sticks[option][symbol].set(option,symbol, interval[0], df['time'][1], df['open'][1],
                                                          df['high'][1],
                                                          df['low'][1], df['close'][1], df['volume'][1],'in_complete')
                        self.info_[option].update({symbol:candle_sticks[option][symbol]})

            self.feedback.update({'id': self.id})
            self.feedback.update({'options': self.options})
            self.feedback.update({'tick_rate':self.tick_rate})
            self.feedback.update({'time': time.time()})
            time.sleep(self.tick_rate)
            loop_took = time.time() - last_time
            self.feedback.update({'loop_took': loop_took})
            if self._yield_ == False:
                break
            yield self.info_,self.feedback

        return self.info_,self.feedback

#####################################################################################################################

class Trend_Lines:
    def __init__(self):
        self.id=f'line_{__id__()}'
        self.m=0
        self.c=0

    def draw(self,p0,p1):
        x_1,y_1=p0
        x_2,y_2=p1
        m=(y_2-y_1)/(x_2-x_1)
        self.m=m
        c=y_1-(m*x_1)
        self.c=c
        return

    def set(self,symbol,points_0=(None,None),points_1=(None,None)):
        self.p0=points_0
        self.p1=points_1
        self.symbol=symbol
        self.draw(self.p0,self.p1)
        self.equation = f'Y = {self.m} X + {self.c}'

    def info(self):
        return {
            'id':self.id,
            'symbol':self.symbol,
            'equation': self.equation,
            'm':self.m,
            'c':self.c,
            'points_1':self.p0,
            'points_2':self.p1
        }

class Price_Levels:
    def __init__(self):
        self.id=f'price_level_{__id__()}'
        self.Y_price=0
        self.X_time=0
        self.support=False
        self.resistance=False
        self.number_of_retest=0

    def set(self,option,symbol,price,_time_=None,type=None,error=0.5):
        self.option=option
        self.symbol=symbol
        self.Y_price=price
        self.error=error
        if _time_==None:
            self.level_creator='user_created'
            self.X_time=time.time()
            self.type=type

        else:
            self.level_creator='market_created'
            self.X_time=_time_
            self.type=type

    def info(self):
        return {
            'id':self.id,
            'option':self.option,
            'symbol':self.symbol,
            'price_level':self.Y_price,
            'time':self.X_time,
            'level_creator':self.level_creator,
            'type':self.type,
            'support':self.support,
            'resistance':self.resistance,
            'error':self.error
        }

    def restore(self,info):
        self.id=info['id']
        self.option=info['option']
        self.symbol=info['symbol']
        self.Y_price=info['price_level']
        self.X_time=info['time']
        self.level_creator=info['level_creator']
        self.type=info['type']
        self.support=info['support']
        self.resistance=info['resistance']
        self.error=info['error']

    def compare(self,price):

        range = (self.Y_price * self.error) / 100

        if self.Y_price > price and self.Y_price-range > price:
            return 'less_than_and_not_in_range'

        elif self.Y_price < price and self.Y_price+range < price:
            return 'greater_than_and_not_in_range'

        elif self.Y_price > price and self.Y_price-range < price:
            return 'less_than_and_in_range'

        elif self.Y_price < price and self.Y_price+range > price:
            return 'greater_than_and_in_range'

        elif self.Y_price == price:
            return 'equal'

class Save_Load_Data:

    def __init__(self,folder_path,name):

        self.file_name=name
        self.file_info=None
        self.file_path=os.path.join(folder_path,self.file_name)
        self.dir_info=os.path.join(self.file_path,r'dir_info.txt')

    def id_parser(self,id):
        id = id.split('_')
        id.pop(-1)
        id_ = ''
        for i in id:
            id_ = id_ + i
            id_ = id_ + '_'
        id = id_
        return id

    def save(self,object_info,name):

        id=object_info['id']
        id=self.id_parser(id)

        with open(self.dir_info, "a") as a_file:
            a_file.write(name+'&'+f'{id}'+'\n')
        with open(self.file_path+f'\\{name}&{id}.txt','a') as a_file:
            a_file.write(f'{object_info}'+'\n')

    def load(self,name,id):

        id=self.id_parser(id)

        with open(self.file_path+f'\\{name}&{id}.txt','r') as a_file:
            for line in a_file:
                info=line.strip()

        info=eval(info)

        return info

class Feedback:
    def __init__(self,unique_name='none'):
        self.name=unique_name
        self.id=f'feedback_{__id__()}'
        self.feedback=[]

    def push(self,feedback):
        self.feedback.append(feedback)

    def reset(self):
        self.feedback=[]

    def spit(self):

        for feedback in self.feedback:
            yield feedback

class Candle_Sticks_Manager:

    def __init__(self,unique_name='none'):
        self.name=unique_name
        self.id=f'manage_candle_sticks_{__id__()}'
        self.intervalsinmilli = {'1m': 1 * 60 * 1000, '3m': 3 * 60 * 1000, '5m': 5 * 60 * 1000, '15m': 15 * 60 * 1000,
                                 '30m': 30 * 60 * 1000, '1h': 1 * 60 * 60 * 1000, '2h': 2 * 60 * 60 * 1000,
                                 '4h': 4 * 60 * 60 * 1000,
                                 '6h': 6 * 60 * 60 * 1000, '8h': 8 * 60 * 60 * 1000, '12h': 12 * 60 * 60 * 1000,
                                 '1d': 1 * 24 * 60 * 60 * 1000,
                                 '3d': 3 * 24 * 60 * 60 * 1000, '1w': 1 * 7 * 24 * 60 * 60 * 1000
                                 }

    def set(self,options):
        self.options=options

    def info(self):
        return {
            'options':self.options
        }

    def __save__(self,candle_sticks,save_load_obj):

        for option in candle_sticks:
            folder=os.path.join(save_load_obj.file_path,option)
            if os.path.exists(folder)!=True:
                os.mkdir(folder)
            for symbol in candle_sticks[option]:
                symbol_file=os.path.join(folder,f'{symbol}_{self.options[option][symbol]}.txt')
                with open(symbol_file,'a') as file:
                    if os.path.exists(symbol_file) == True:
                        candle_sticks[option][symbol].to_string(file,header=False,index=False)
                    else:
                        candle_sticks[option][symbol].to_string(file,index=False)

        return

    def __load__(self,save_load_obj):

        pass

    def download_and_save_candle_sticks(self,from_when,till_when,save_load_object):

        for option in self.options:
            exec(f'import {option}')

        monitor={}
        candle_sticks={}

        for option in self.options:
            candle_sticks.update({option:{}})
            monitor.update({option:{}})
            for symbol in self.options[option]:
                candle_sticks[option].update({symbol:None})
                monitor[option].update({symbol:None})

        self.feedback = {}
        last_time = time.time()

        for option in self.options:

            for symbol in self.options[option]:
                interval = self.options[option][symbol]
                symbol = [symbol]
                from_when_ = [from_when]
                till_when_ = [till_when]
                interval = [interval]

                while (True):

                    info = eval(
                        f'{option}.GetCandleStickDataOHLCV({symbol},{interval},{from_when_},{till_when_})')

                    df = info[f'{symbol[0]}_{interval[0]}']
                    try:

                        try_again = False
                    except:
                        try_again = True
                        print('___S_E_R_V_O_R___U_N - R_E_S_P_O_N_S_I_V_S___')
                        time.sleep(1)
                    if try_again == False:
                        break

                symbol=symbol[0]
                candle_sticks[option][symbol]=df

        self.__save__(candle_sticks,save_load_object)

        self.feedback.update({'id': self.id})
        self.feedback.update({'options': self.options})
        loop_took = time.time() - last_time
        self.feedback.update({'time': time.time()})
        self.feedback.update({'loop_took': loop_took})

        return self.feedback




