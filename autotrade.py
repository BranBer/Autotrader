import matplotlib.pyplot as plt
import json
import alpaca_trade_api as tradeapi
import statistics
from tradingplatform import MyAccount

def trader():
    # alpaca_info = open("alpacakeys.json", "r").read()
    # alpaca_json = json.loads(alpaca_info)
    # key_id = alpaca_json["KEY_ID"]
    # secret_key = alpaca_json["SECRET_KEY"]

    # api = tradeapi.REST(key_id, secret_key, base_url='https://paper-api.alpaca.markets') 
    # account = api.get_account()
    # api.list_positions()

    #account = MyAccount(key_file = "alpacakeys.json", symbols=[("aapl", .50), ("f", .30), ("x", .20)], useBollinger = True)
    account = MyAccount(key_file = "alpacakeys.json", symbols=[("aapl", .90)], useBollinger = True)
    account.run_algo_pool()

def main():
    trader()
    #plt.plot([1,2,3,4], [1, 10, 20, 40])
    #plt.ylabel('Some Numbers')
    plt.show()

if __name__ == "__main__":
    main()
    
