import ccxt
import pandas as pd

exchange = ccxt.ftx()
exchange_class = getattr(ccxt, 'ftx') #change exchange name here 
exchange = exchange_class({
    'apiKey': "",
    'secret': "",
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

def find_active_BTC_ETH_futures(exchange):
    exchange.loadMarkets()
    symbols = exchange.symbols
    tickers=[]
    for symbol in symbols:
        if not '.' in symbol:
            if 'BTC/USD'in symbol or 'ETH/USD' in symbol:
                tickers.append(symbol)
            if 'XBT' in symbol and '_' not in symbol:
                tickers.append(symbol)
    # df = pd.DataFrame(tickers)
    # df.to_csv('ActiveFutures.csv', mode='a', index=False, header=False)
    return tickers

# def find_inactive_BTC_ETH_futures(exchange):
#     exchange.loadMarkets()
#     symbols = exchange.symbols
#     tickers=[]
#     for symbol in symbols:
#         if '.' in symbol:
#             if 'BTC/USD'in symbol or 'ETH/USD' in symbol:
#                 tickers.append(symbol)
#             if 'XBT' in symbol and '_' not in symbol:
#                 tickers.append(symbol)
#     # df = pd.DataFrame(tickers)
#     # df.to_csv('InactiveFutures.csv', mode='a', index=False, header=False)
#     return tickers

def main():
    # for i in find_active_BTC_ETH_futures(exchange):
    #     print(i)
    for i in find_all_exchange_tickers(exchange):
        print(i)


if __name__ == '__main__':
    main()
