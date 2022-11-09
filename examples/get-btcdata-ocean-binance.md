## Get Binance BTC/USDT price feed via Ocean

This is published as a free asset in Ocean. Under the hood, it queries the Binance API.

You can see it on Ocean Market [here](https://market.oceanprotocol.com/asset/did:op:b4584760f5133b27d91c337b9c10b56448b84a1bae39b8c1037d0de33023b4dc).

### 0. Setup

From [Challenge 2](../challenges/main2.md), do:

- [x] Setup

### 1. Get Data

In Python console:

```python
BTC_USDT_did = "did:op:b4584760f5133b27d91c337b9c10b56448b84a1bae39b8c1037d0de33023b4dc"

file_name = ocean.assets.download_file(BTC_USDT_did, alice_wallet)
```

### 2. Prepare a DataFrame with the data ready for your analysis
```
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

### 3. Get the data for the hour of the day that makes sense for your analysis
```
# If you only want the data at 19h every day
data_at_19h = df[df['Datetime'].dt.hour == 19]

# If you want the data every 12 hours, for example at midnight and at 12h every day
data_every_12h = df[(df['Datetime'].dt.hour == 0) | (df['Datetime'].dt.hour == 12)]
```
