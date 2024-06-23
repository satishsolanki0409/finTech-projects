#%%
import alphavantage as app
import matplotlib.pyplot as plt
ticker = 'NVDA'

msft = app.stock(ticker, interval='60min')
msft.getSignal('MACD')
# %%
