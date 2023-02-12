## Get Binance ETH/USDT price feed via Binance API direct

Here, we directly query the Binance API "Kline/Candlestick Data". [Here's the docs](https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data). 

We use Python [requests](https://requests.readthedocs.io/en/latest/) library to make queries.

### 0. Setup

We assume you've already done [main3.md](../challenges/main3.md#1-setup) "Setup".

If needed, re-setup in Python:
- Do ocean.py [setup-remote.md](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/setup-remote.md#6-setup-in-python) "Setup in Python"
- Do this repo's [helpers.md](../support/helpers.md)

### 1. Get Data

In the Python console:
```python
import requests
url = f"https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1h"
r = requests.get(url)
cex_x = r.json()

# cex_x is a list 500 items, one for every hour, on the hour. 
#
# Each item has a list of 12 entries: 
# (0) timestamp (1) open price (2) high price (3) low price (4) close price (5) Vol ..
#
# Example item: [1662998400000, 1706.38, 1717.87, 1693, 1713.56, ..]
# Timestamp is unix time, but in ms. To get unix time (in s), divide by 1000

# Example: get unix timestamps
uts = [xi[0]/1000 for xi in cex_x]

# Example: get close prices
close_prices = [float(xi[4]) for xi in cex_x]
```

Here's a different example, restricting data to just the previous week.
```
from datetime import datetime, timedelta
end_datetime = datetime.now() 
start_datetime = end_datetime - timedelta(days=7)

url = f"https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1h&startTime={int(start_datetime.timestamp())*1000}&endTime={int(end_datetime.timestamp())*1000}"

# the rest is the same. cex_x should have just 168 items (number of hours in the week)
```
