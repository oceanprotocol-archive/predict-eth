## Get Binance ETH/USDT price feed via Ocean

This is published as a free asset in Ocean. Under the hood, it queries the Binance API.

You can see it on Ocean Market [here](https://market.oceanprotocol.com/asset/did:op:0dac5eb4965fb2b485181671adbf3a23b0133abf71d2775eda8043e8efc92d19).

### 0. Setup

We assume you've already done [main3.md](../challenges/main3.md#1-setup) "Setup".

If needed, re-setup in Python:
- Do ocean.py [setup-remote.md](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/setup-remote.md#6-setup-in-python) "Setup in Python"
- And do: `from predict_eth.helpers import *`

### 1. Download data

In the Python console:

```python
ETH_USDT_did = "did:op:0dac5eb4965fb2b485181671adbf3a23b0133abf71d2775eda8043e8efc92d19"
ETH_USDT_ddo = ocean.assets.resolve(ETH_USDT_did)
ETH_USDT_datatoken = ocean.get_datatoken(ETH_USDT_ddo.datatokens[0]["address"])

from ocean_lib.ocean.util import to_wei
ETH_USDT_datatoken.dispense(to_wei(1), {"from":alice_wallet})
order_tx_id = ocean.assets.pay_for_access_service(ETH_USDT_ddo, {"from": alice_wallet})
file_name = ocean.assets.download_asset(ETH_USDT_ddo, alice_wallet,"./", order_tx_id)
```

The next two steps show two different approaches to open the file: Python native support, and Pandas Dataframes.

### 2. Approach: Open data via Python native file support

In the same Python console:
```python
with open(file_name, "r") as file:
    data_str = file.read().rstrip().replace('"', '')
    cex_x = eval(data_str) #list of lists

# cex_x is a list of 1000 items, one for every hour, on the hour. 
#
# Each item has a list of 5 entries: 
# (0) timestamp (1) open price (2) high price (3) low price (4) close price
#
# Example item: [1662998400000, 1706.38, 1717.87, 1693, 1713.56]
# Timestamp is unix time, but in ms. To get unix time (in s), divide by 1000

# Example: get unix timestamps
uts = [xi[0]/1000 for xi in cex_x]

# Example: get close prices
close_prices = [xi[4] for xi in cex_x]
```

### 3. Approach: Open data via Pandas dataframe

In the same Python console:
```python
import pandas as pd

# cex_x is a list of 1000 items, one for every hour, on the hour.
# Each item has a list of 5 entries:
# (0) timestamp (1) open price (2) high price (3) low price (4) close price

# Create initial DataFrame
df = pd.read_json(file_name)

# Add names to columns
df = df.rename(columns={0: 'TimeStamp', 1: 'Open', 2: 'Highest', 3: 'Lowest', 4: 'Close', 5: 'Volume'})

# Transform Timestamp from miliseconds to DateTime
df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], unit="ms")

# Rename column Timestamp to Datetime
df = df.rename(columns={'TimeStamp': 'Datetime'})
```

To take this further, let's get the data for the hour of the day that makes sense for your analysis.

In the same Python console:
```python
# If you only want the data at 19h every day
data_at_19h = df[df['Datetime'].dt.hour == 19]

# If you want the data every 12 hours, for example at midnight and at 12h every day
data_every_12h = df[(df['Datetime'].dt.hour == 0) | (df['Datetime'].dt.hour == 12)]
```
