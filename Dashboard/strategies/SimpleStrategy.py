import math
import backtrader as bt

#MACD line is the FastEMA - SlowEMA
#Signal line is the mean of the 9 day MA of the MACD line

class SimpleStrategy(bt.Strategy):
    params = (('fast',12), ('slow', 26), ('order_percentage', 0.95), ('ticker', 'DOT'))
    #fast-12, slow-26

    def __init__(self):
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close,
            period=self.params.fast,
            plotname='12 day moving average'
        )

        self.slow_moving_average = bt.indicators.SMA(
            self.data.close,
            period=self.params.slow,
            plotname='26 day moving average'
        )

        self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)
        self.stoc = bt.talib.STOCH(self.data.high, self.data.low, self.data.close, fastk_period=14, slowk_period=3)

    def next(self):
        #We own 0 tokens
        if self.position.size == 0:
            #If MA cross has happened execute a buy order
            if (self.crossover > 0) and (90 > self.stoc > 40):
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)
                
                print(f"Buying {self.size} shares of {self.params.ticker} at {self.data.close[0]}")

                self.buy(size=self.size)
            
        #If we own the token
        if (self.position.size > 0) and (10 < self.stoc < 60):
            #if the MA cross happens sell
            if self.crossover < 0:
                print(f"Selling {self.size} shares of {self.params.ticker} at {self.data.close[0]}")

                self.close()