#  Tr_Blitz_ 
### Crypto-Trading-Bot
_________________________________________________________________________________________________________________

1.blitz_trade_tools.py 

* This library consist of all kinds of tools which you can use to build any type of trading bot you can imagine 

* It has tools like 24x7 price ticker , 24x7 candle sticks ticker , tools to manage candle sticks , 
tools to manage price levels , tools to place orders , concel orders , check orders , view account info ,
manage time etc with multiple exchanges and multiple assets.
                                          
* The data type used is nested structures , for example :

       import blitz_trade_tools
       
       ## Input for 24x7 candle stick ticker tool.
       
       options = {
                    'HeyBinance' : {
                         'BTCUSDT' : '1h',
                         'ETHBNB' : '1m'
                    },
                    
                    'RobinHood' : {
                         'LTCUSDT' : '1h'
                    }
                 }
       
       ## Create the ticker obj. This way you can create any number of tickers you want.
       
       candle_stick_ticker_1 = blitz_trade_tools.Candle_Stick_Ticker()
       
       ## .set() is used to give required settings for this tool. .set() is used for all the tools.
       
       candle_stick_ticker_1.set(options = options , tick_rate = 4)
       
       ## tick_rate = 4 , ticks every 4 seconds.
      
* Here HeyBinance is to call binance API and RobinHood for Robinhood API
* This is the input for 24x7 candle stick ticker tool to get candle stick data of BTCUSDT 1 hour , ETHBNB 1 minute , LTCUSDT 1 hour candle sticks from binance and robinhood.
* The output will be candle stick objects which consists all the details of a single candle stick :

      ## Output for 24x7 candle stick ticker tool.
      
      for output in candle_stick_ticker_1.run():
           print(output)
           ## Iterate 24x7 for 4 seconds per iter. OR you can call it as ticks per second OR as tick_rate.
      
OUTPUT:

      _______________________________________________________
      {
         'HeyBinance' : {
              'BTCUSDT' : BTCUSDT candlestick obj ,
              'ETHBNB' : ETHBNB candlestick obj
         },
         'RobinHood' : {
              'LTCUSDT' : LTCUSDT candlestick obj
         }
      }
      ________________________________________________________

* you can also set the above tool if you want to avoid for loop
      
      candle_stick_ticker_1.set(options = options , tick_rate = 4 ,yield = False)
      
      while(True):
          ## can be called inside any kind of loop. 
                                 
                        |
                        
          output = candle_stick_ticker_1.run()
          print(output)
                        |
                        
 OUTPUT:
 
       _______________________________________________________
      {
         'HeyBinance' : {
              'BTCUSDT' : BTCUSDT candlestick obj ,
              'ETHBNB' : ETHBNB candlestick obj
         },
         'RobinHood' : {
              'LTCUSDT' : LTCUSDT candlestick obj
         }
      }
      ________________________________________________________                  
                        
                        
