## Get Binance ETH/USDT price feed via CCXT

Here, we use the the ccxt library, "a collection of available crypto exchanges or exchange classes. Each class implements the public and private API for a particular crypto exchange." [Here are ccxt docs](https://docs.ccxt.com/en/latest/manual.html). [Here's ccxt on github](https://github.com/ccxt/ccxt).

Under the hood, ccxt queries the Binance API for Binance data.


### 0. Setup

We assume you've already done [main3.md](../challenges/main3.md#1-setup) "Setup".

If needed, re-setup in Python:
- Do ocean.py [setup-remote.md](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/setup-remote.md#6-setup-in-python) "Setup in Python"
- Do this repo's [helpers.md](../support/helpers.md)

### 1. Get Data
 
In the Python console:

```python
import ccxt
cex_x = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h')

# cex_x is a list of 500 items, one for every hour, on the hour.
#
# Each item has a list of 6 entries:
# (0) timestamp (1) open price (2) high price (3) low price (4) close price (5) volume
# Example item: [1662998400000, 1706.38, 1717.87, 1693, 1713.56, 2186632.9224]
# Timestamp is unix time, but in ms. To get unix time (in s), divide by 1000

# Example: get unix timestamps
uts = [xi[0]/1000 for xi in cex_x]

# Example: get close prices
close_prices = [xi[4] for xi in cex_x]
```
