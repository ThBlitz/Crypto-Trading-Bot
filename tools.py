import time
import os

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
        self.save_feedback = False

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

    def record_feedback(self,feedback_obj=None):
        if feedback_obj==None:
            self.save_feedback=False
        else:
            self.save_feedback=True
            self.feed=feedback_obj

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

                if self.save_feedback==True:
                    self.feed.push(self.feedback)

                if self._yield_==False:
                    break

                yield return_price

            return return_price

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
        self.save_feedback = False

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

    def record_feedback(self,feedback_obj=None):
        if feedback_obj==None:
            self.save_feedback=False
        else:
            self.save_feedback=True
            self.feed=feedback_obj

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

        if self.save_feedback==True:
            self.feed.push(self.feedback)

        return self.assets

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
        self.save_feedback = False

    def set(self,trade_type,options,keys):
        self.options=options
        self.trade_type=trade_type
        self.keys=keys

    def info(self):
        return {
            'name':self.name,
            'id':self.id,
            'options':self.options,
            'trade_type':self.trade_type,
            'keys':self.keys
        }

    def restore(self,info):
        self.name=info['name']
        self.id=info['id']
        self.options=info['options']
        self.trade_type=info['trade_type']
        self.keys=info['keys']

    def save(self,save_obj):
        save_obj.save(self.info(),self.name)

    def load(self,save_obj,name):
        info=save_obj.load(name,self.id)
        self.restore(info)

    def record_feedback(self,feedback_obj=None):
        if feedback_obj==None:
            self.save_feedback=False
        else:
            self.save_feedback=True
            self.feed=feedback_obj

    def run(self,assetA_assetB,quantity,BUY_or_SELL,precision,price=None):
        last_time=time.time()
        assetA_assetB=assetA_assetB.split('_')
        self.assetA_and_assetB=assetA_assetB[0]+assetA_assetB[1]
        self.price=price
        self.feedback={}
        self.info_={}

        for option in self.options:
            exec(f'import {option}')

        if self.price==None:
            self.trade_type='market_order'

        if self.trade_type == 'market_order':
            self.price=None
            for option in self.options:
                symbol=self.assetA_and_assetB
                self.order_id=[f'market_order_id_{__id__()}']
                symbol=[symbol]
                if isinstance(quantity,float):
                    self.quantity=[round(quantity,precision)]
                elif isinstance(quantity[option],float):
                    self.quantity=[round(quantity[option],precision)]
                else:
                    print('ERROR_AT_PLACE_ORDER')
                self.BUY_or_SELL=[BUY_or_SELL]
                self.api_key = [self.keys[f'{option}'][f'api_key']]
                self.secret_key = [self.keys[f'{option}'][f'secret_key']]
                info=eval(f'{option}.PlaceNewMarketOrder({symbol},{self.BUY_or_SELL},{self.quantity},{self.order_id},{self.api_key},{self.secret_key})')
                self.info_.update({f'{option}': {symbol[0]:info}})

        elif self.trade_type == 'limit_order':
            for option in self.options:
                symbol=self.assetA_and_assetB
                self.order_id=[f'limit_order_id_{__id__()}']
                symbol = [symbol]
                self.quantity = [quantity]
                self.BUY_or_SELL = [BUY_or_SELL]
                self.api_key = [self.keys[f'{option}'][f'api_key']]
                self.secret_key = [self.keys[f'{option}'][f'secret_key']]
                info=eval(f'{option}.PlaceNewLimitOrder({symbol},{self.BUY_or_SELL},{self.quantity},{self.price},{self.order_id},{self.api_key},{self.secret_key})')
                self.info_.update({f'{option}': {symbol[0]: info}})

        self.feedback.update({'id':self.id})
        self.feedback.update({'options':self.options})
        self.feedback.update({'trade_type':self.trade_type})
        loop_took=time.time()-last_time
        self.feedback.update({'loop_took':loop_took})

        if self.save_feedback==True:
            self.feed.push(self.feedback)

        return self.info_

# option={
#     'HeyBinance':{'BTCUSDT'}
# }
#
# keys={
#     'HeyBinance':{ 'api_key': '12345','secret_key': '12345556'}
# }

class Manage_Order:
    def __init__(self,unique_name='name'):
        self.name=unique_name
        self.id = f'check_order_{__id__()}'
        self.save_feedback = False

    def set(self,keys):
        self.keys=keys

    def info(self):
        return {
            'name':self.name,
            'id':self.id,
            'keys':self.keys
        }

    def restore(self, info):
        self.name = info['name']
        self.id = info['id']
        self.keys = info['keys']

    def save(self, save_obj):
        save_obj.save(self.info(), self.name)

    def load(self, save_obj, name):
        info = save_obj.load(name, self.id)
        self.restore(info)

    def record_feedback(self,feedback_obj=None):
        if feedback_obj==None:
            self.save_feedback=False
        else:
            self.save_feedback=True
            self.feed=feedback_obj

    def run_check_order(self,place_order_output):
        last_time=time.time()
        self.feedback={}
        for option in place_order_output:
            exec(f'import {option}')

        self.info_={}

        for option in place_order_output:
            self.info_.update({option:{}})
            for symbol in place_order_output[option]:
                _info=place_order_output[option][symbol]
                self.order_id=[_info['order_id']]
                self.symbol=[symbol]
                self.api_key = [self.keys[f'{option}'][f'api_key']]
                self.secret_key = [self.keys[f'{option}'][f'secret_key']]
                info=eval(f'{option}.CheckOrderStatus({self.symbol},{self.order_id},{self.api_key},{self.secret_key})')
                self.info_[option].update({symbol: info})

        self.feedback.update({'id':self.id})
        loop_took=time.time()-last_time
        self.feedback.update({'loop_took':loop_took})

        if self.save_feedback==True:
            self.feed.push(self.feedback)

        return self.info_

    def run_cancel_order(self, place_order_output):
        last_time = time.time()
        self.feedback = {}
        for option in place_order_output:
            exec(f'import {option}')

        self.info_ = {}

        for option in place_order_output:
            self.info_.update({option:{}})
            for symbol in place_order_output[option]:
                _info = place_order_output[option][symbol]
                self.order_id = [_info['order_id']]
                self.symbol = [symbol]
                self.api_key = [self.keys[f'{option}'][f'api_key']]
                self.secret_key = [self.keys[f'{option}'][f'secret_key']]
                info=eval(f'{option}.CancelaOrder({self.symbol},{self.order_id},{self.api_key},{self.secret_key})')
                self.info_[option].update({symbol: info})

        self.feedback.update({'id': self.id})
        loop_took = time.time() - last_time
        self.feedback.update({'loop_took': loop_took})

        if self.save_feedback==True:
            self.feed.push(self.feedback)

        return self.info_

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
        self.save_feedback = False
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

    def record_feedback(self,feedback_obj=None):
        if feedback_obj==None:
            self.save_feedback=False
        else:
            self.save_feedback=True
            self.feed=feedback_obj

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

                        try:

                            info=eval(f'{option}.GetCandleStickDataOHLCV({symbol},{interval},{int(from_when)},{int(till_when)})')


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

            if self.save_feedback==True:
                self.feed.push(self.feedback)

            if self._yield_ == False:
                break
            yield self.info_

        return self.info_

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
        self.folder_path=folder_path
        self.file_info=None
        self.file_path=os.path.join(self.folder_path,self.file_name)
        if os.path.exists(self.file_path)==False:
            os.makedirs(self.file_path)
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
            if os.path.exists(folder)==False:
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

    def record_ticks(self,candle_stick_ticks,save_load_obj):
        isinstance(save_load_obj,Save_Load_Data)
        for option in candle_stick_ticks:
            for symbol in candle_stick_ticks[option]:
                candle_stick=candle_stick_ticks[option][symbol]
                isinstance(candle_stick,Candle_Sticks)
                status=candle_stick.status
                interval=candle_stick.interval
                if status=='complete':
                    folder = os.path.join(save_load_obj.file_path, option)
                    if os.path.exists(folder) == False:
                        os.mkdir(folder)

                    symbol_file = os.path.join(folder, f'{symbol}_{interval}.txt')
                    with open(symbol_file, 'a') as file:
                        file.write(f'{candle_stick.info()}\n')

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

class BUY_or_SELL:

    def __init__(self,unique_name='none'):
        self.id=__id__()
        self.name=unique_name

    def set(self,account_info_obj,place_order_obj,
                manage_order_obj):

        if isinstance(account_info_obj,Account_info) and isinstance(place_order_obj,Place_Order) and isinstance(manage_order_obj,Manage_Order):

            self._acc_=account_info_obj
            self._place_order_=place_order_obj
            self._manage_order_=manage_order_obj

        else:
            print('ERROR AT BUY or SELL SET()')

    def run(self,price_ticks,BUY_or_SELL,assetA_assetB,precision,quantity_in_percentage=0.5,price=None):

        assetA_assetB_=assetA_assetB.split('_')

        self.assetA_and_assetB=assetA_assetB_[0]+assetA_assetB_[1]
        self.fraction=quantity_in_percentage

        self.price={}

        for option in self._place_order_.options:

            i=price_ticks[option][self.assetA_and_assetB]
            if isinstance(i,Candle_Sticks):
                self.price.update({option:i.close})
            elif isinstance(i,float):
                self.price.update({option:i})
            else:
                print('ERROR_AT_BUY_or_SELL_CLASS')

        quantity_A={}
        quantity_B={}
        quantity_A_to_buy={}
        quantity_A_to_sell={}

        acc_info=self._acc_.run()
        for option in acc_info:

            quantity_A.update({option:acc_info[option][assetA_assetB_[0]]})
            quantity_B.update({option:acc_info[option][assetA_assetB_[1]]})
            b=float(quantity_B[option])
            a=float(quantity_A[option])
            quantity_A_to_buy.update({option:(b * self.fraction)/self.price[option]})
            quantity_A_to_sell.update({option:(a * self.fraction)})


        if self._place_order_.trade_type=='market_order':

            if BUY_or_SELL=='BUY':

                order_info=self._place_order_.run(assetA_assetB,quantity_A_to_buy,'BUY',precision)

            elif BUY_or_SELL=='SELL':

                order_info=self._place_order_.run(assetA_assetB,quantity_A_to_sell,'SELL',precision)

            else:
                print('ERROR AT BUY or SELL')
                order_info=None


            time.sleep(2)
            _order_= self._manage_order_.run_check_order(order_info)

            _acc_info_ = self._acc_.run()
        elif self._place_order_.trade_type=='limit_order':
            order_info=None
            _order_=None
            _acc_info_ = self._acc_.run()
        else:
            order_info = None
            _order_ = None
            _acc_info_ = self._acc_.run()

        return order_info,_order_,_acc_info_

class Manage_Time_Ticker:

    def __init__(self,unique_name='none'):
        self.name=unique_name
        self.id=f'manage_time_{__id__()}'
        self.prev_loop_took=0

    def set(self,feed_back_obj):
        if isinstance(feed_back_obj,Feedback):
            self.feed=feed_back_obj
        else:
            print('Error at manage_time_ticker.set()')

    def run(self):
        total_time=0
        expected_time=0
        for i in self.feed.spit():
            total_time=total_time+i['loop_took']
            try:
                expected_time=expected_time+i['tick_rate']
            except:
                pass

        loss=total_time-expected_time
        time_diff=self.prev_loop_took-total_time
        self.prev_loop_took=total_time

        return time_diff,loss

