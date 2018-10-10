# Crypto Trading
In this repository we will try several cryptocurrencies algorithmic trading strategies. All this strategies are real time ones but without sending the trades to an exchange*. There is an option to set a Telgram bot to send you messages to your Telegram account for trades executed and equity balance information. 

The different strategies tried are:

* Momentum
* Statistical Arbitrage

## Momentum algo:
The scritp that makes this strategy is: trend_follow_algo.py.

The basics of this strategy is that if one asset (crypto) is going up (or down) it will keep going up (down) for the next periods. We don't know how many periods the asset will keep going up (or down), but as a rule of thumb if a tendency is bigger then it will last more time that one that is more flat. 

So with that on mind, we code a trend following algorithm that computes a regression to the previous 12 data closing prices of the asset and if the slope of this regression line is greather than a value, and the last close price is lower the line (but not lower than the maximum drowdawn expected) we will buy that asset expecting it to maintain the tendency and its momentum. If later the slope of the regression line strarts dectrease and is going to zero we exit the trade. To profit taking we expect to exit the trade at the upper  Bollinger Band (if we are on a long trade) or in the lower Bollinger Band (if we are on a short trade)

## Statistical Arbitrage algo:
stat_arb.py




*NOTE: If you want to make them to work live you will need to write the functions to send those trades to the exchange instead of sending the messages to your Telegram bot.
