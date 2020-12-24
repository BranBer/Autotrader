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

from symbol import TradingPosition

class MyAccount:   

    def __init__(self, key_file, symbols, useBollinger):    
        self.symbols = []
        self.useBollinger = useBollinger
        self.funcs = []
        self.processes = []
        plt.style.use("ggplot")
        self.logFileName = "algoautotrading.log"

        with open(key_file, "r") as file:
            alpaca_info = file.read()
            alpaca_json = json.loads(alpaca_info)

            self.key_id = alpaca_json["KEY_ID"]
            self.secret_key = alpaca_json["SECRET_KEY"]        
            
        self.api = tradeapi.REST(self.key_id, self.secret_key, base_url='https://paper-api.alpaca.markets') 
        account = self.api.get_account()

        self.cash = float(account.cash)

        print("Now working with $" + str(self.cash) + ", with symbols: " )

        for s in symbols:
            perc = math.floor(float(s[1]) * float(self.cash))
            print (s[0] + " using $" + str(perc) + ".")

            sym = TradingPosition(api = self.api, symbol = s[0], cash_percentage = s[1])

            self.symbols.append(sym)
                
    def run_algo_pool(self):
        for s in self.symbols:
            f = s.run_algorithmic_trader()
            self.funcs.append(f)

        plt.show()





