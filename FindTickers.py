import ccxt, json
import pandas as pd


with open('config.json', 'r') as f: 
    config = json.load(f)

api_key = config['exchange']['apiKey'] # enter keys in config.json 
api_secret = config['exchange']['secret']

exchange = ccxt.ftx()
exchange_class = getattr(ccxt, 'ftx') #change exchange name here 
exchange = exchange_class({
    'apiKey': api_key,
    'secret': api_secret,
    'test': False,
})

def find_all_exchange_tickers(exchange):
    '''
        Returns a list of all active symbols. 
        Inactive symbols have '.' at the front
        Indexes have '_' at the front 
    '''
    exchange.loadMarkets()
    symbols = exchange.symbols
    tickers=[]
    for symbol in symbols:
        tickers.append(symbol)
    df = pd.DataFrame(tickers)
    df.to_csv('Tickers.csv', mode='w+', index=False, header=False) ## Change the name of the cvs to suit your exchange
    return tickers

def find_futures_symbols(exchange):
    exchange.loadMarkets()
    symbols = exchange.symbols
    tickers=[]
    for symbol in symbols:
        if not '.' in symbol: # '.' denotes inactive symbols, remove the not to find inactive futures
            if 'BTC/USD'in symbol or 'ETH/USD' in symbol: # change paramaters as needed
                tickers.append(symbol)
            if 'XBT' in symbol and '_' not in symbol:
                tickers.append(symbol)
    return tickers

def main():
    for i in find_all_exchange_tickers(exchange):
        print(i)

if __name__ == '__main__':
    main()
