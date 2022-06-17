from secret import API_KEY, API_SECRET
from binance.client import Client
import pandas as pd
from ta.volatility import BollingerBands
from ta.utils import dropna
import plotly.graph_objects as go
from datetime import datetime


# Initialize Client
client = Client(API_KEY, API_SECRET, testnet=True)

# Vraag de candlesticks op van binance
klines = client.get_historical_klines("BTCBUSD", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

#Maak een pandas dataframe van de candlestick data van binance om te data makkelijker te bekijken en te gebruiken.
df = pd.DataFrame(klines)

## Geheugensteuntje
  # date    df[0]
  # open    df[1]
  # high    df[2]
  # low     df[3]
  # close   df[4]
  # volume  df[5]
                
                
df.drop(df.columns[5:12], axis=1, inplace=True) # Verwijder ongebruikte kollommen 5 tot en met 11 (Twaalf omdat de laatste niet meegeteld wordt)


for i in range(len(df[0])):             
    df[0][i] = datetime.utcfromtimestamp(df[0][i]//1000) # Delen door duizend omdat binance de unix-timestamps met drie extra integers stuurt, waarom binance... 😕 ?
    

indicator_bb = BollingerBands(close=df[4], window=20, window_dev=2)


df['bb_bbm'] = indicator_bb.bollinger_mavg()    # voeg middelste bb lijn toe aan dataframe
df['bb_bbh'] = indicator_bb.bollinger_hband()   # voeg bovenste bb lijn toe aan dataframe
df['bb_bbl'] = indicator_bb.bollinger_lband()   # voeg onderste bb lijn toe aan dataframe



# Plot Chart
fig = go.Figure(data=[
    go.Candlestick(x=df[0],
                open=df[1],
                high=df[2],
                low=df[3],
                close=df[4],
                line=dict(width=1)),
    
    ##CODE NOT OPTIMISED!
    
    
      go.Line(              #
            x=df[0],        # zet de x as van die lijn gelijk met de date
            y=df['bb_bbm'], # plot middelste bb lijn

       ), 
      go.Line(              #
            x=df[0],        # zet de x as van die lijn gelijk met de date
            y=df['bb_bbh'], # plot bovenste bb lijn
       ), 
            go.Line(        # 
            x=df[0],        # zet de x as van die lijn gelijk met de date
            y=df['bb_bbl'], # plot onderste bb lijn
       )            
])

fig.show()
