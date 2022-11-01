## Get Binance ETH/USDT price feed via Ocean

This is published as a free asset in Ocean. Under the hood, it queries the uniswap-v3-subgraph.

You can see it on Ocean Market [here](https://market.oceanprotocol.com/asset/did:op:deb138bcabdc21f126bc064489cd58d16792f782d2e145f0227e4d9778650243).

### 0. Setup

From [predict-eth2.md](../predict-eth2.md), do:
- [x] Setup

### 1. Get Data

In Python console:

```python
ETH_USDT_did = "did:op:deb138bcabdc21f126bc064489cd58d16792f782d2e145f0227e4d9778650243"
file_name = ocean.assets.download_file(ETH_USDT_did, alice_wallet)

# Each item in the json file has 8 entries:
# (0) periodStartUnix (1) priceUSD (2) open (3) high (4) low (5) close (6) volume (7) VolumeUSD

# create dataframe with the required variables
data = pd.read_json(file_name)
data = pd.json_normalize(data.data.tokenHourDatas)

# The DataFrame data contains 5 columns. This information can be sued as predictors
# in a machine learning model (i.e an autoregressive model)
```