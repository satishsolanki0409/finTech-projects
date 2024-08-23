#%%
import alphavantage as app
import matplotlib.pyplot as plt
ticker = 'NVDA'

# Allowed:  1min, 5min, 15min, 30min, 60min 
msft = app.stock(ticker, interval='1day')
msft.getSignal('MACD')
# %%
