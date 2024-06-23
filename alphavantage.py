
# import
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

ts = TimeSeries(API_KEY, output_format='pandas', indexing_type='integer') 
ti = TechIndicators(key=API_KEY, output_format='pandas')

# TimeSeries(key='YOUR_API_KEY',output_format='pandas', indexing_type='date')

class stock:
    def __init__(self, ticker, interval= '15min') -> None:
        self.ticker = ticker
        self.interval = interval # Allowed:  1min, 5min, 15min, 30min, 60min 

    def getIntraDayData(self, interval='1min', last100=True, plot=False):
        self.interval = interval
        output = 'full'
        if last100: 
            output ='compact'
        
        self.data, self.metaData = ts.get_intraday(self.ticker, self.interval, output)
        self.data['typical_price'] = (self.data['2. high'] + self.data['3. low'] + 
                                      self.data['4. close'] + self.data['1. open'])/4
        if plot:
            self.data['typical_price'].plot()
            plt.title(f'{self.ticker} stock ({self.interval})')
            plt.show()
        
    def getBbands(self, interval='1min'):
        # Bolinger Band
        self.band, meta_data = ti.get_bbands(symbol=self.ticker, 
                                        interval=self.interval, time_period=60)
        
    
    def calculate_ema(self, days):
        return self.data['typical_price'].ewm(span=days, adjust=False).mean()

    def calculate_macd(self):
        ema_12 = self.calculate_ema(12)
        ema_26 = self.calculate_ema(26)
        macd_line = ema_12 - ema_26
        signal_line = self.calculate_ema(9)
        return macd_line, signal_line


   
    def getSignal(self, indicator):
        self.getIntraDayData()
        # https://www.alphavantage.co/simple_moving_average_sma/
        if (indicator == 'MACD'):
            # Calculate MACD and Signal Line
            macd_line, signal_line = self.calculate_macd()

            # calculate macd

            # using SMA cross-over of SMA-5 day (short term) and SMA-20 days
            self.data['SMA5'] = self.data['typical_price'].rolling(5).mean()
            self.data['SMA20'] = self.data['typical_price'].rolling(20).mean()
            
            signals = pd.DataFrame(index=macd_line.index)
            signals['MACD'] = macd_line
            signals['Signal'] = signal_line
            signals['Signal Line'] = 0.0

            # Generate Buy/Sell signals
            signals['Signal'] = np.where(signals['MACD'] > signals['Signal'], 1.0, 0.0)
            signals['Position'] = signals['Signal'].diff()
            
            # Print the signals
            print(signals.tail(10))

            # check for CROSSOVER
            # Golden Cross:(Buy Signal) SMA5 crosses above SMA20.
            #    Early stages of a reversal to an uptrend
            # Death Cross = (Sell Signal) SMA5 crosses below SMA20
            #    Early stages of a reversal to a downtrend.
            # delta_percent = (self.data['SMA5'].iloc[-1] - self.data['SMA20'].iloc[-1])/self.data['SMA5'].iloc[-1]
            # if abs(delta_percent) < 0.005:
            #     if delta_percent > 0:
            #         # SELL
            #         print("SELL")
            #         return -1
            #     else:
            #         # BUY
            #         print("BUY")
            #         return 1 
            
            # if delta_percent > 0:
            #     # SELL
            #     print("Upcoming SELL event")
            #     return -0.5
            # else:
            #     # BUY
            #     print("Upcoming BUY event")
            #     return 0.5 
