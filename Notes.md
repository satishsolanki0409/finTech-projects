
# 1. SMA (Simple Moving Average)
- Simple Arithmetic mean of given period of data. 
- All the data points have equal weights (both recent and old). It make sense for Intra-Day, but may not be good large period data
- Less sensitive to recent price movement

# 2. EMA (Exponential Moving Avg)
-  more weightage to recent data
EMA(t) = (2 / (N+1)) * P  + ((N-1)/(N+1))*EMA(t-1) 

- More responsive to current price movement

# 3. MACD (Moving Average Convergence Divergence)
- Its one of the momentum indicator based on 2 exponential moving averages​
MACD = EMA_12 - EMA_26

- Assumption: Stock is trending and have high Momentum

- Key definitions : 
    - Trending = if current price is higher than last 200 MA price
    - Momentum =  (current price - (10 days before closing price)) / 10 

