import json, time
import pandas as pd
import ccxt


with open('config.json', 'r') as f: 
    config = json.load(f)

api_key = config['exchange']['apiKey']
api_secret = config['exchange']['secret']

exchange = ccxt.ftx()
exchange_class = getattr(ccxt, 'ftx')
exchange = exchange_class({
    'apiKey': "",
    'secret': "",
    # 'asyncio_loop': self.loop,
    'enableRateLimit': True,
    'test': False,
})

bitmex_symbols = ['BTC/USDT:USDT', 'ETH/USDT:USDT', 'SOL/USDT:USDT']
bitmex_futures = ['BTC/USDT:USDT-220624']

## To get historical data for expired contracts, use exchange specific symbols
params_bitmex = {'market_name': 'ETHJ17'} # TODO: bitMEX does not return any expired markets

# Perpetuals
ftx_symbols = ['BTC/USD:USD', 'ETH/USD:USD', 'SOL/USD:USD', 'CRO/USD:USD', 'GLMR/USD:USD', 'BNB/USD:USD', 'LTC/USD:USD']
ftx_futures = ['BTC/USD:USD-220624']

## To get historical data for expired contracts, use exchange specific symbols
params_ftx = {'market_name': 'BTC-0325'}

msec = 1000
minute = 60 * msec

def get_historical_data():
    from_timestamp = exchange.parse8601('2021-12-19 00:00:00')
    now = exchange.milliseconds()
    while from_timestamp < now:

        bars = exchange.fetch_ohlcv(ftx_symbols[0], '1m', from_timestamp)
        funding = exchange.fetch_funding_rate_history("BTC-PERP", from_timestamp, now) ## This function must pass in the exchange specific ID

        # print(exchange.last_response_headers)
        time.sleep(exchange.rateLimit / msec)  
        from_timestamp += len(bars) * minute

        df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df2 = pd.DataFrame(funding)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['funding_rate_time'] = pd.to_datetime(df2['datetime'])
        df['funding_rate'] = df2['fundingRate']
        # df = df.drop_duplicates
        # df['previous_close'] = df['close'].shift(1)
        df.to_csv('working.csv', mode='a', index=False, header=False)

def get_expired_historical_data():
    from_timestamp = exchange.parse8601('2022-03-22 00:00:00') 
    end = exchange.parse8601('2022-03-25 00:00:00') # End date of the contract
    while from_timestamp < end:

        ## Params overrides the first paramter, so that can be left blank
        bars = exchange.fetch_ohlcv('','1m', from_timestamp, end, params_ftx)

        time.sleep(exchange.rateLimit / msec)  
        from_timestamp += len(bars) * minute

        df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        # df = df.drop_duplicates
        # df['previous_close'] = df['close'].shift(1)
        df.to_csv('expired.csv',  mode='a', index=False, header=False)

get_expired_historical_data()
# get_historical_data()

## resample lower timeframe data into higher timeframes
# data = df.resample('15T', on='timestamp').agg({'open': 'first',
#                                               'high': 'max',
#                                               'low': 'min',
#                                               'close': 'last',
#                                               'volume': 'sum',})

#print(data)
