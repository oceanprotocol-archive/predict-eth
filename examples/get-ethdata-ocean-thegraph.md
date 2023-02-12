## Get Binance ETH/USDT price feed via Ocean

This is published as a free asset in Ocean. Under the hood, it queries the uniswap-v3-subgraph.

You can see it on Ocean Market [here](https://market.oceanprotocol.com/asset/did:op:deb138bcabdc21f126bc064489cd58d16792f782d2e145f0227e4d9778650243).

### 0. Setup

We assume you've already done [main3.md](../challenges/main3.md#1-setup) "Setup".

If needed, re-setup in Python:
- Do ocean.py [setup-remote.md](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/setup-remote.md#6-setup-in-python) "Setup in Python"
- Do this repo's [helpers.md](../support/helpers.md)

### 1. Get Data

In the Python console:

```python
ETH_USDT_did = "did:op:deb138bcabdc21f126bc064489cd58d16792f782d2e145f0227e4d9778650243"
ETH_USDT_ddo = ocean.assets.resolve(ETH_USDT_did)
ETH_USDT_datatoken = ocean.get_datatoken(ETH_USDT_ddo.datatokens[0]["address"])

from ocean_lib.ocean.util import to_wei
ETH_USDT_datatoken.dispense(to_wei(1), {"from":alice_wallet})
order_tx_id = ocean.assets.pay_for_access_service(ETH_USDT_ddo, {"from": alice_wallet})
file_name = ocean.assets.download_asset(ETH_USDT_ddo, alice_wallet,"./", order_tx_id)

# Each item in the json file has 8 entries:
# (0) periodStartUnix (1) priceUSD (2) open (3) high (4) low (5) close (6) volume (7) VolumeUSD

# create dataframe with the required variables
import pandas as pd
data = pd.read_json(file_name)
data = pd.json_normalize(data.data.tokenHourDatas)

# The DataFrame data contains 8 columns. This information can be sued as predictors
# in a machine learning model (i.e an autoregressive model)
```