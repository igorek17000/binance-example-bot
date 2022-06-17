from secret import API_KEY, API_SECRET
from binance.client import Client
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
import plotly.graph_objects as go
from datetime import datetime



client = Client(API_KEY, API_SECRET, testnet=True)

klines = client.get_historical_klines("BTCBUSD", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

df = pd.DataFrame(klines)


for i in range(len(df[0])):             
    df[0][i] = datetime.utcfromtimestamp(df[0][i]//1000) # Divide by thousand because binance delivers unix timestamps with three extra integers
    
    
fig = go.Figure(data=[go.Candlestick(x=df[0],
                open=df[1],
                high=df[2],
                low=df[3],
                close=df[4])])

fig.show()