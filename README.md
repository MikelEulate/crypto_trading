# Crypto Trading Strategies
In this repository we will try several cryptocurrencies algorithmic trading strategies. All this strategies are real time ones but without sending the trades to an exchange*. There is an option to set a Telgram bot to send you messages to your Telegram account for trades executed and equity balance information. 

The different strategies tried are:

* Momentum
* Statistical Arbitrage

## Momentum algo:
The scritp that makes this strategy is: trend_follow_algo.py.

The basics of this strategy is that if one asset (crypto) is going up (or down) it will keep going up (down) for the next periods. We don't know how many periods the asset will keep going up (or down), but as a rule of thumb if a tendency is bigger then it will last more time that one that is more flat. 

So with that on mind, we code a trend following algorithm that computes a regression of the previous 12 data closing prices of the asset and if:

* Bullish asset: the slope of this regression line is greather than a value, and the last close price is below  the line (but not more than the maximum drowdawn expected) we will buy that asset expecting it to maintain the tendency and its momentum. If later the slope of the regression line strarts decrease and is going to zero we exit the trade. To profit taking we expect to exit the trade at the upper  Bollinger Band. 

* Bearish asset: the slope of this regression line is lower than a value, and the last close price is higher the line (but not more than the maximum drowdawn expected) we will sell that asset expecting it to maintain the tendency and its momentum. If later the slope of the regression line strarts decrease and is going to zero we exit the trade. To profit taking we expect to exit the trade atthe lower Bollinger Band.

### Running the script:

```
$ python trend_follow_algo.py
```

## Statistical Arbitrage algo:
The scritp that makes this strategy is: stat_arb.py

The basics of this strategy is that it is possible that the same asset can have different prices among crypto exchanges. The idea is to buy the asset in the exchange where the price is higher and sell the same asset into the exchange whith the lower price. The idea is similar to a pairs trade. We short the difference between prices expecting it to mean reverse and close the trade when the higher price exchange is now below the other exchange price.


### Running the script:

```
& python stat_arb.py
```

#### 
NOTE:Helper function: get_crypto_data_ohcl.py
Functions for retrieving crypto data last price or historical prices. Run the functions depending the data you need.

* If you want to make them to work live you will need to write the functions to send those trades to the exchange instead of sending the messages to your Telegram bot.
