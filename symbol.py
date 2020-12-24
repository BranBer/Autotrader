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

class TradingPosition:
    def __init__(self, api, symbol, cash_percentage):
        self.symbol = symbol.upper()
        self.api = api
        self.anim = None
        account = self.api.get_account()
        self.cash = float(account.cash)
        self.percent_cash = math.floor(float(account.cash) * float(cash_percentage))

        self.fig, self.ax = plt.subplots()
        self.fig.suptitle(self.symbol, fontsize=16)
        self.logFileName = "algoautotrading.log"

    def run_algorithmic_trader(self):
        symbol = self.symbol
        percent_cash = self.percent_cash

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

        def animate(i):
            now = datetime.datetime.now()
            weekday = now.weekday()
            is_weekday = True if weekday < 5 else False
            is_market_open = True if now.time() > datetime.time(9, 30, 00) and now.time() < datetime.time(16, 00, 00) else False
            is_tradeable_time = is_weekday and is_market_open

            if(is_tradeable_time):
                price = float(self.api.get_last_trade(symbol).price)
                timestamp = self.api.get_last_trade(symbol).timestamp
                closing_prices.append(price)
                timestamps.append(timestamp)

                position = pd.Series(closing_prices)

                pos = position.tolist()
                
                std = position.rolling(window).std()
                avg = position.rolling(window).mean()

                moving_std = list(filter(lambda i: not pd.isna(i), std.tolist()))
                moving_avg = avg.tolist()
                upper = avg + (std * 2)
                lower = avg - (std * 2)  

                upper_band = upper.tolist()
                lower_band = lower.tolist()

                self.ax.cla()
                self.ax.plot(timestamps[-100:], closing_prices[-100:], color="green")                      
                self.ax.plot(timestamps[-100:], upper_band[-100:], color="red") 
                self.ax.plot(timestamps[-100:], moving_avg[-100:], color="red")   
                self.ax.plot(timestamps[-100:], lower_band[-100:], color="red")       

                buy_qty = math.floor(percent_cash/price)
                sell_qty = 0

                owned_positions = list(map(lambda position: position.symbol, self.api.list_positions()))

                has_symbol = True if symbol in owned_positions else False

                if(has_symbol):
                    sell_qty = int(self.api.get_position(symbol).qty)
                
                
                #sell
                if(price >= upper_band[len(upper_band) - 1] and has_symbol and sell_qty > 0 ):
                    self.api.submit_order(symbol=symbol, qty=sell_qty, side='sell', time_in_force='day', type='market')

                    with open(self.logFileName, "a+") as log:
                        log.write('Sold ' + str(sell_qty) + ' of ' + symbol + ' for a total of $' + str(price * sell_qty) + '\n')

                #Buy
                if(price <= lower_band[len(lower_band) - 1] and not has_symbol and buy_qty >= 1 and float(buy_qty * price) <=self.cash):
                    self.api.submit_order(symbol=symbol, qty=buy_qty, side='buy', time_in_force='day', type='market')
                    
                    with open(self.logFileName, "a+") as log:
                        log.write('Bought ' + str(buy_qty) + ' of ' + symbol + ' for a total of $' + str(price * buy_qty) + '\n')

            
        self.anim = FuncAnimation(self.fig, animate, interval=60000)
        return self.anim



