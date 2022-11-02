# Quickstart: Algorithmic Trading Flow

This quickstart supports those in the DeFi community that are interested in algorithmically trading cryptocurrencies.

A custom trading strategy hosted on Ocean Protocol's Goerli Test Net collaborates with the open-source project, [Freqtrade](https://github.com/freqtrade/freqtrade), to demonstrate an algorithmic crypto trading use case.

# 1\. Setup

## Prerequisites and Installation

This example uses an algo crypto trading bot from [Freqtrade](https://github.com/freqtrade/freqtrade). Before installing your Freqtrade trading bot, you will need to do the following three actions:
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Install [Telegram](https://telegram.org/)
3. [Create a Telegram bot](https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot)

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
? Select exchange ftx
? Do you want to enable Telegram? Yes
? Insert Telegram token **********************************************
? Insert Telegram chat id **********
? Do you want to enable the Rest API (includes FreqUI)? Yes
? Insert Api server Listen Address (0.0.0.0 for docker, otherwise best left unto
uched) 0.0.0.0
? Insert api-server username freqtrader
? Insert api-server password <Enter your password here>
```

Congratulations! The configuration file is now available at ft_userdata/user_data/config.json

Navigate to the config.json file and underneath `"dry_run": true,` add `"dry_run_wallet": 10000,`

* This dry\_run\_wallet value tells your bot to begin trading with $10,000 USD and the `"stake_amount": "unlimited"` tells the bot to reinvest any gains + the $10,000 principal. If this stake amount was hard-coded to $10,000 USD, for example, then the bot would only trade a base amount of up to $10,000 and no more.

* * *

# 2\. Implement A Trading Strategy

Now for the fun part.

We're going to download an Ocean Protocol custom trading strategy located on the [Ocean Market](https://market.oceanprotocol.com/). Navigate to the [market](https://market.oceanprotocol.com/) and connect your wallet to the Goerli test network.

[Next, click here to go to the Custom OP Trading Strategy's page.](https://market.oceanprotocol.com/asset/did:op:736282af36d3088a40ea1a947bb8d9eade32e641f2a995394f5f7817ee873e8a)

On the trading strategy's web page, click the pink Get button on the right side panel. You will need some Goerli ETH to approve the transaction. [Click here for the Goerli ETH faucet](https://goerlifaucet.com/) if you need more Goerli ETH.

Put the file in the directory ft_userdata/user_data/strategies/

Add the Strategy's ***class name*** to the docker-compose.yml file in ft_userdata/ by replacing `--strategy SampleStrategy` at the bottom of the .yml file with `--strategy customOPstrategy`. The SampleStrategy is run by default.

# 3\. Go Live!

We're ready to go live!

Turn on the bot from the command line:

`docker-compose up -d`

You'll now see fresh activity on your Telegram chat with your trading bot. Your bot will indicate that it is using your custom trading strategy. Allow a few minutes for your bot to find trading pairs - it can take a while for your bot to find trading pairs that satisfy all the trading signals in your strategy depending on current market conditions.

Helpful hints:

- In the Telegram chat with your bot, you can type /help to see a full list of commands.
- Anytime you change the config.json file, then you need to reload the config file. In Telegram, you simply type /reload_config in the chat.
- Anytime you change the docker-compose.yml file, then you need to bring the bot down and then bring it back up via the command line for the changes to take effect: `docker-compose down` then `docker-compose up -d`
- Check out the Freqtrade UI at 0.0.0.0:8080 in your browser to observe the bot's performance

# 4\. About the OP custom trading strategy

This trading strategy uses three technical indicators to buy and sell cryptocurrency pairs:
- [Relative Strength Index (RSI)](https://www.investopedia.com/articles/active-trading/042114/overbought-or-oversold-use-relative-strength-index-find-out.asp)
- [Bollinger Bands](https://www.investopedia.com/terms/b/bollingerbands.asp)
- [Triple Exponential Moving Average (TEMA)](https://www.investopedia.com/ask/answers/041315/why-triple-exponential-moving-average-tema-important-traders-and-analysts.asp)

Furthermore, the candlesticks are customized in the [Heiken Ashi](https://www.investopedia.com/terms/h/heikinashi.asp) style.

Let's review the BUY signal code:

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > 33) &
                (dataframe['tema'] <= dataframe['bb_middleband']) &  # Guard: tema below BB middle
                (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard: tema is raising
                (dataframe['ha_open'] < dataframe['ha_close'])  # green bar
            ),
            'enter_long'] = 1

        return dataframe
		

1. Buy a cryptocurrency pair when the RSI crosses **above** at least 33: 

RSI is a momentum indicator showing that the cryptocurrency pair is moving upwards as a bullish sign! When the RSI is lower than 33, then the strategy deems the RSI too risky to buy the currency pair.

AND

2. The triple exponential moving average (TEMA) is **lower** than the the middle bollinger band:

Although the RSI may be up, if the TEMA is less than the middle bollinger band, then the cryptocurrency pair is at a bargain.

AND

3. The triple exponential moving average crosses **above** that triple exponential moving average value of the PREVIOUS candle:

This indicates that the momentum of the cryptocurrency pair is moving upward in a bullish direction.
NOTE: the code `.shift(1)` denotes the previous candle

AND

4. The open of the Heiken Ashi candle is **less** than the close. 

This is equivalent to saying that the candle's closing price is HIGHER than the open -> Bullish indicator!

When these 4 conditions are satisfied, then the bot buys the crypto currency pair.

The SELL signal code is converse to the buy signal code, except to note that when the RSI is greater than 62 then the cryptocurrency pair is overbought and it's time to sell.

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > 62) &
                (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard: tema above BB middle
                (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard: tema is falling
                (dataframe['ha_open'] > dataframe['ha_close'])  # red bar
            ),

            'exit_long'] = 1

        return dataframe

# 5\. Live Trade with Caution

All the above steps are a great start with creating your algo trading bot. 

However, it is not recommended to trade with real money until you have at least backtested your strategy. It is also recommended to hyperopt your strategy's parameters with ML. The Freqtrade project luckily gives you these abilities!

Learn how:

- [Backtest your strategy](https://www.freqtrade.io/en/stable/backtesting/)
- [Hyperopt your strategy](https://www.freqtrade.io/en/stable/hyperopt/)

Helpful hint:

You will need to define a static pairlist in your config.json file in order to backtest.

More detailed information to customize your Freqtrade bot is [here](https://www.freqtrade.io/en/stable/docker_quickstart/).
