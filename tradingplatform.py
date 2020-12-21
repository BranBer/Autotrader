import matplotlib.pyplot as plt
import json
import alpaca_trade_api as tradeapi
import statistics
import datetime
import time
import math
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation
from multiprocessing import Process

class MyAccount:
    logFileName = "algoautotrading.log"

    def __init__(self, key_file, symbols, useBollinger):    
        self.symbols = []
        self.useBollinger = useBollinger
        self.anims = []
        self.funcs = []
        self.figs = []

        with open(key_file, "r") as file:
            alpaca_info = file.read()
            alpaca_json = json.loads(alpaca_info)

            self.key_id = alpaca_json["KEY_ID"]
            self.secret_key = alpaca_json["SECRET_KEY"]        
            
        self.api = tradeapi.REST(self.key_id, self.secret_key, base_url='https://paper-api.alpaca.markets') 
        account = self.api.get_account()

        self.cash = account.cash

        print("Now working with $" + str(self.cash) + ", with symbols: " )

        for s in symbols:
            perc = math.floor(float(s[1]) * float(self.cash))
            print (s[0] + " using $" + str(perc) + ".")
            self.symbols.append([s[0], perc])

    def get_cash(self):
        return self.cash

    def run_algorithmic_trader(self, symbol):
        indexed_sym = None
        is_last_symbol = False

        count = 0
        for sym in self.symbols:
            if(sym[0].upper() == symbol.upper()):
                indexed_sym = sym
                if(count == len(self.symbols) - 1):
                    is_last_symbol = True
                break
            
            count+=1

        if(indexed_sym == None):
            raise ValueError("Symbol Not Found")

        symbol = indexed_sym[0].upper()
        percent_cash = indexed_sym[1]

        print("Running Algo Trader for " + symbol)

        window = 21

        barset = self.api.get_barset(symbol, "1Min", limit=window)[symbol]

        closing_prices = list(map(lambda bar: bar.c, barset))
        timestamps = list(map(lambda bar: bar.t, barset))
        position = pd.Series(closing_prices)

        pos = position.tolist()
        
        std = position.rolling(window).std()
        avg = position.rolling(window).mean()

        moving_std = list(filter(lambda i: not pd.isna(i), std.tolist()))
        moving_avg = list(filter(lambda i: not pd.isna(i), avg.tolist()))

        upper = position + (std * 2)
        lower = position - (std * 2)

        upper_band = list(filter(lambda i: not pd.isna(i), upper.tolist()))
        lower_band = list(filter(lambda i: not pd.isna(i), lower.tolist()))        


        fig = plt.figure()
        plt.style.use('ggplot')
        plt.title(symbol)


        def animate(i):
            now = datetime.datetime.now()
            weekday = now.weekday()

            is_weekday = True if weekday < 5 else False
            is_market_open = True if now.time() > datetime.time(9, 00, 00) and now.time() < datetime.time(16, 00, 00) else False
            is_tradeable_time = is_weekday and is_market_open

            if(is_tradeable_time):
                price = self.api.get_last_trade(symbol).price
                timestamp = self.api.get_last_trade(symbol).timestamp
                closing_prices.append(price)
                timestamps.append(timestamp)

                position = pd.Series(closing_prices)

                pos = position.tolist()
                
                std = position.rolling(window).std()
                avg = position.rolling(window).mean()

                moving_std = list(filter(lambda i: not pd.isna(i), std.tolist()))
                moving_avg = avg.tolist()
                upper = position + (std * 2)
                lower = position - (std * 2)  

                upper_band = upper.tolist()
                lower_band = lower.tolist()

                plt.cla()
                plt.plot(timestamps[-100:], closing_prices[-100:], color="green")                      
                plt.plot(timestamps[-100:], upper_band[-100:], color="red") 
                plt.plot(timestamps[-100:], moving_avg[-100:], color="red")   
                plt.plot(timestamps[-100:], lower_band[-100:], color="red")       

                plt.tight_layout()
                buy_qty = math.floor(percent_cash/price)
                sell_qty = 0

                has_symbol = True if symbol in self.api.list_positions() else False

                if(has_symbol):
                    sell_qty = self.api.get_position(symbol).qty   

                #sell
                if(price >= upper and has_symbol and sell_qty > 0 ):
                    self.api.submit_order(symbol=symbol, qty=sell_qty, side='sell', time_in_force='day', type='market')

                    with open(logFileName, "a+") as log:
                         log.write('Sold ' + str(sell_qty) + ' of ' + symbol + ' for a total of $' + str(price * sell_qty) + '\n')

                #Buy
                if(price <= lower and not has_symbol and buy_qty >= 1 and (buy_qty * price) <= self.cash):
                    self.api.submit_order(symbol=symbol, qty=buy_qty, side='buy', time_in_force='day', type='market')
                    
                    with open(logFileName, "a+") as log:
                         log.write('Bought ' + str(buy_qty) + ' of ' + symbol + ' for a total of $' + str(price * buy_qty) + '\n')


        ani = FuncAnimation(fig, animate, interval=1000)
        self.anims.append(ani)

        
        plt.show()

                
    def run_algo_pool(self):
        for s in self.symbols:
            p = Process(target = self.run_algorithmic_trader, args=(s[0].upper(),))
            p.start()
            p.join()
        



