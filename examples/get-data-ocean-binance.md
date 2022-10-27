## Get Binance ETH/USDT price feed via Ocean

This is published as a free asset in Ocean. Under the hood, it queries the Binance API.

You can see it on Ocean Market [here](https://market.oceanprotocol.com/asset/did:op:0dac5eb4965fb2b485181671adbf3a23b0133abf71d2775eda8043e8efc92d19).

### 0. Setup

From [predict-eth2.md](../predict-eth2.md), do:
- [x] Setup

### 1. Get Data

In Python console:

```python
ETH_USDT_did = "did:op:0dac5eb4965fb2b485181671adbf3a23b0133abf71d2775eda8043e8efc92d19"

file_name = ocean.assets.download_file(ETH_USDT_did, alice_wallet)

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
