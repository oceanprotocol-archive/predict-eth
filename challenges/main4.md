<!--
Copyright 2023 Ocean Protocol Foundation
SPDX-License-Identifier: Apache-2.0
-->

# Predict ETH Price: Round Four

## 0. Introduction

This is the main readme for the Ocean Data Challenge :: ETH Prediction Round 4.

### 0.1 Key dates

- Kickoff: Tue Mar 7, 2023. (Criteria may change before kickoff.)
- Submission deadline: Wed Apr 5, 2023 at 23:59 UTC
- Prediction at times: Thu Apr 6, 2023 at 1:00 UTC, 2:00, ..., 12:00 (12 predictions total).
- Winners announced: within one week. See previous challenge results [here]( https://blog.oceanprotocol.com/introducing-the-winners-of-the-eth-price-prediction-data-challenge-edition-2-6acdccb9271)

### 0.2 Criteria to win


The winner = whoever has lowest prediction error. That's all.

To be eligible, competitors must produce the outcomes that this README guides. This includes:
- Creating an Ocean data NFT
- On the data NFT, setting a value correctly: correct field label, correct # predictions, prediction values following correct formatting, predictions encrypted with proper encoding on judges' public key
- Data NFT transfered to Ocean judges before the deadline
- All on Mumbai network, not another network

The following are _not_ criteria:
- Feedback. You can give feedback here (FIXME) and we appreciate it! However, it does not count towards winning.
- Presentation. There is no presentation needed.
- How well the flow was followed. Rather, you either followed it or you didn't. You are only eligible if you followed it.

Competitors do _not_ use Desights platform to submit. Rather, just follow the steps within this README. Desights will only be used to announce winners.


### 0.3 Outline of this README

This readme describes a basic flow to predict future ETH price, and submit your predictions to contest judges. We'll be using Mumbai, which is Polygon's testnet.

Here are the steps:

1. Setup
2. Get data locally
3. Make predictions
4. Publish & share predictions

## 1. Setup

### 1.1 Install Ocean

In ocean.py's [install.md](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/install.md), follow all steps.

### 1.2 Install predict-eth

The [predict-eth library](https://pypi.org/project/predict-eth) has a specific error calculation function, and [other functions](https://github.com/oceanprotocol/predict-eth/blob/main/predict_eth/helpers.py) specific to this competition. In the console:

```console
pip3 install predict-eth
```

### 1.3 Install other Python libraries

The READMEs use several numerical & ML libraries. In the console:
```
pip3 install ccxt eth_account matplotlib numpy pandas prophet requests sklearn
```


### 1.5 Do Ocean remote setup

In ocean.py's [setup-remote.md](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/setup-remote.md), follow all steps.

### 1.6 Load helper functions

In the Python console:

```python
from predict_eth.helpers import *
```

## 2. Get data locally

Here, use whatever data you wish. It can be static data or streams, free or priced, raw data or feature vectors or otherwise. It can be published via Ocean, or not. The [main README](../README.md) links to some options.

This demo flow skips getting data because it will generate random predictions (no data needed).

## 3.  Make predictions

### 3.1  Build a simple AI model

Here, build whatever AI/ML model you want, leveraging the data from the previous step. The [main README](../README.md) links to some options. 

This demo flow skips building a model because it will generate random predictions (no model needed).

### 3.2  Run the AI model to make future ETH price predictions

Predictions must be one prediction every hour on the hour, for a 12h period. The specific times were given above. There are 12 predictions total. The output is a list with 12 items.

Here's an example with random numbers. In the same Python console:
```python
#get predicted ETH values
mean, stddev = 1500, 25.0
pred_vals = list(np.random.normal(loc=mean, scale=stddev, size=(12,)))
```

### 3.3 Calculate NMSE

We use normalized mean-squared error (NMSE) as the accuracy measure.

In the same Python console:

```python
# get the time range we want to test for
start_dt = datetime.datetime.now() - datetime.timedelta(hours=24) #must be >= 12h ago; we use 24
start_dt = round_to_nearest_hour(start_dt) # so that times line up
target_uts = target_12h_unixtimes(start_dt)
print_datetime_info("target times", target_uts)

# get the actual ETH values at that time
import ccxt
allcex_x = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h')
allcex_uts = [xi[0]/1000 for xi in allcex_x]
allcex_vals = [xi[4] for xi in allcex_x]
print_datetime_info("allcex times", allcex_uts)

cex_vals = filter_to_target_uts(target_uts, allcex_uts, allcex_vals)

# now, we have predicted and actual values. Let's find error, and plot!
nmse = calc_nmse(cex_vals, pred_vals)
print(f"NMSE = {nmse}")
plot_prices(cex_vals, pred_vals)
```

Keep iterating in step 3 until you're satisfied with accuracy. Then...

## 4.  Publish & share predictions

### 4.1 Encrypt predictions with judges' public key

We encrypt, so that your competitors can't see your predictions.

FIXME

### 4.2 Create data NFT

FIXME

### 4.3 Store encrypted predictions on data NFT

Set ERC725 key label ="predictions", value = encrypted predictions

FIXME

### 4.4 Send data nft to judges

Why: for prediction tamper-resistance after the deadline.

FIXME

## Appendix: What judges will do

FIXME

In the terminal:
```console
export REMOTE_TEST_PRIVATE_KEY1=<judges' private key, having address 0xA54A..>
```

In the same Python console:
```python
# setup
from predict_eth.helpers import *

ocean = create_ocean_instance("polygon-test") # change the network name if needed
alice = create_alice_wallet(ocean) #you're Alice

# specify target times
start_dt = datetime.datetime(2022, 12, 12, 1, 00) #Dec 12, 2022 at 1:00am UTC
target_uts = target_12h_unixtimes(start_dt)
print_datetime_info("target times", target_uts)

# get predicted ETH values
did = <value shared by you>
order_tx_id = ocean.assets.pay_for_access_service(ddo, {"from":alice})
file_name = ocean.assets.download_asset(ddo, alice, './', order_tx_id)
pred_vals = load_list(file_name)

# get actual ETH values (final)
import ccxt
cex_x = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h')
allcex_uts = [xi[0]/1000 for xi in cex_x]
allcex_vals = [xi[4] for xi in cex_x]
print_datetime_info("all CEX data info", allcex_uts)

cex_vals = filter_to_target_uts(target_uts, allcex_uts, allcex_vals)
print(f"cex ETH price is ${cex_vals[0]} at start_dt of {start_dt}")
print(f"cex_vals: {cex_vals}")

# calc nmse, plot
nmse = calc_nmse(cex_vals, pred_vals)
print(f"NMSE = {nmse}")
plot_prices(cex_vals, pred_vals)
```


