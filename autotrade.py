import matplotlib.pyplot as plt
import json
import alpaca_trade_api as tradeapi
import statistics
from tradingplatform import MyAccount

def trader():
    account = MyAccount(key_file = "alpacakeys.json", symbols=[("aapl", .50), ("f", .20), ("x", .20), ("ge", .10)], useBollinger = True)
    account.run_algo_pool()

def main():
    trader()


if __name__ == "__main__":
    main()
    
