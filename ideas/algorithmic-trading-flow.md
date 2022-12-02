# Quickstart: Algorithmic Trading Flow

This quickstart supports those in the DeFi community that are interested in algorithmically trading cryptocurrencies.

It's a custom trading strategy published as an Ocean asset on Polygon. It leverages the open-source project [Freqtrade](https://github.com/freqtrade/freqtrade) to demonstrate an algorithmic crypto trading use case.

# 1\. Setup

## Prerequisites

This example uses an algo crypto trading bot from [Freqtrade](https://github.com/freqtrade/freqtrade). Before installing your Freqtrade trading bot, you will need to do the following three actions:

1.  Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2.  Install [Telegram](https://telegram.org/)
3.  [Create a Telegram bot](https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot)

## Installation

Then, follow the Terminal commands to install your local Freqtrade bot:

```Bash
mkdir ft_userdata
cd ft_userdata/
# Download the docker-compose file from the repository
curl https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml -o docker-compose.yml

# Pull the freqtrade image
docker-compose pull

# Create user directory structure
docker-compose run --rm freqtrade create-userdir --userdir user_data

# Create configuration - Requires answering interactive questions
docker-compose run --rm freqtrade new-config --config user_data/config.json
```

To fill out your configuration file for the first time, the following answers are encouraged:

```
? Do you want to enable Dry-run (simulated trades)? Yes
? Please insert your stake currency: USD
? Please insert your stake amount (Number or 'unlimited'): unlimited
? Please insert max_open_trades (Integer or -1 for unlimited open trades): 5
? Time Have the strategy define timeframe.
? Please insert your display Currency (for reporting): USD
? Select exchange kraken
? Do you want to enable Telegram? Yes
? Insert Telegram token **********************************************
? Insert Telegram chat id **********
? Do you want to enable the Rest API (includes FreqUI)? Yes
? Insert Api server Listen Address (0.0.0.0 for docker, otherwise best left unto
uched) 0.0.0.0
? Insert api-server username freqtrader
? Insert api-server password <Enter your password here>
```

Congratulations! The configuration file is now available at ft\_userdata/user\_data/config.json

* * *

# 2\. Implement A Trading Strategy

Now for the fun part.

We're going to download a custom Ocean Protocol trading strategy located on the Ocean Market. Navigate to the [market](https://market.oceanprotocol.com/) and connect your wallet to the Polygon network.

[Next, click here to go to the Trading Strategy's page.](https://market.oceanprotocol.com/asset/did:op:f2bbe839cc3911cb8a5ac19c4126501237fe1c2218677e2344bfeaabe56cd289)

On the trading strategy's web page, you will see the asset titled "Algorithmic Cryptocurrency Trading (Freqtrade) - Strategy #2". Click the pink Get button on the right side panel. You will need some Matic to approve the transaction.

Once you approve the transaction, the pink button will say Download. Click this button to download the file into a location of your choosing.

Put the file in the directory ft\_userdata/user\_data/strategies/

Add the Strategy's ***class name*** to the docker-compose.yml file in ft_userdata/ by replacing `--strategy SampleStrategy` at the bottom of the .yml file with `--strategy emaCrossStrategy`. The SampleStrategy is run by default.

# 3\. Go Live!

We're ready to go live!

Turn on the bot from the command line:

`docker-compose up -d`

You'll now see fresh activity on your Telegram chat with your trading bot. Your bot will indicate that it is using your custom trading strategy. Allow time for your bot to find trading pairs - it can take a few minutes or even hours for your bot to find trading pairs that satisfy all the trading signals in your strategy depending on current market conditions.

Helpful hints:

- In the Telegram chat with your bot, you can type /help to see a full list of commands.
- Anytime you change the config.json file, then you need to reload the config file. In Telegram, you simply type /reload_config in the chat.
- Anytime you change the docker-compose.yml file, then you need to bring the bot down and then bring it back up via the command line for the changes to take effect: `docker-compose down` then `docker-compose up -d`
- Check out the Freqtrade UI at 0.0.0.0:8080 in your browser to observe the bot's performance.

# 4\. About the trading strategy

This trading strategy uses three technical indicators to buy and sell cryptocurrency pairs:

- [Relative Strength Index (RSI)](https://www.investopedia.com/articles/active-trading/042114/overbought-or-oversold-use-relative-strength-index-find-out.asp)
- [Bollinger Bands](https://www.investopedia.com/terms/b/bollingerbands.asp)
- [Exponential Moving Average (EMA)](https://www.investopedia.com/terms/e/ema.asp)

## BUY Code

Let's review the BUY signal code:

```
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                ((dataframe['rsi'] > 29) & 
                (dataframe['close'] < dataframe['bb_lowerband'])) | 
                ((dataframe['ema5'] > dataframe['ema21']) &  
                (dataframe['ema5'].shift(1) <= dataframe['ema21'])) 
            ),
        'buy'] = 1

        return dataframe
```

1.  Buy a cryptocurrency pair when the RSI is **above** 29:

RSI is a momentum indicator that indicates a bullish sign as the RSI value increases. When the RSI is lower than 29, then the strategy deems the cryptocurrency pair too risky to buy. Thus, the buy condition requires the RSI to be above 29.

AND

2.  The close of the current candle is **less** than the the lower Bollinger band:

When the close of the current candle is less than that of the lower Bollinger Band, then the cryptocurrency pair is selling at a bargain because the currency pair is oversold.

OR

3.  The exponential moving average 5 crosses **above** the exponential moving average 21 value:

This EMA movement is called a "Golden Cross". The exponential moving average is a type of Moving Average that is exponentially weighted to react more quickly to recent price changes. The EMA5 reacts even more quickly to recent price changes than the EMA21, so this indicates a bullish signal.

AND

4.  The EMA5 of the previous candle was **less than or equal to** the EMA21 of the current candle:

Coupled with condition #3, this indicates that the momentum of the cryptocurrency pair is moving upward in a bullish direction.

NOTE: the code `.shift(1)` denotes the previous candle

**When either conditions 1 & 2 OR conditions 3 & 4 are satisfied, then the bot *buys* the crypto currency pair.**

## SELL Code

The SELL signal code is converse to the buy signal code:

```
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
 
        dataframe.loc[
            (
                ((dataframe['rsi'] > 71) &
                (dataframe['close'] > dataframe['bb_middleband'])) | 
                ((dataframe['ema5'] < dataframe['ema21']) & 
                (dataframe['ema5'].shift(1) > dataframe['ema21'])) 
            ),
        'sell'] = 1

        return dataframe
```

1.  Sell a cryptocurrency pair when the RSI is **above** 71:

When the RSI is above 71, then the strategy deems the cryptocurrency pair too risky to hold because the currency pair is overbought.

AND

2.  The close of the current candle is **greater** than the the middle Bollinger band:

When the close of the current candle is greater than that of the middle Bollinger Band, then the cryptocurrency pair is selling at a premium because the currency pair is overbought.

OR

3.  The exponential moving average 5 crosses **below** the exponential moving average 21 value:

This EMA movement is called a "Death Cross". Recall that the EMA5 reacts even more quickly to recent price changes than the EMA21, so this indicates a bearish signal.

AND

4.  The EMA5 of the previous candle was **greater than** the EMA21 of the current candle:

This indicates that the momentum of the cryptocurrency pair is moving downward in a bearish direction.

**When either conditions 1 & 2 OR conditions 3 & 4 are satisfied, then the bot *sells* the crypto currency pair.**

# 5\. Live Trade with Caution

All the above steps are a _great start_ with creating your algo trading bot.

However, it is not recommended to trade with real money until you have at least backtested your strategy. It is also recommended to hyperopt your strategy's parameters with machine learning. The Freqtrade project luckily gives you these abilities!

Learn how to:

- [Backtest your strategy](https://www.freqtrade.io/en/stable/backtesting/)
- [Hyperopt your strategy](https://www.freqtrade.io/en/stable/hyperopt/)

Helpful hint:

You will need to define a static pairlist in your config.json file in order to backtest.

More detailed information to customize your Freqtrade bot is [here](https://www.freqtrade.io/en/stable/docker_quickstart/).
