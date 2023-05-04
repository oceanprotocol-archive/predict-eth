<!--
Copyright 2023 Ocean Protocol Foundation
SPDX-License-Identifier: Apache-2.0
-->

# Predict-ETH Round 5

## 0. Introduction

This is the main readme for Predict-ETH Round 5.

### 0.1 Prizes
Prize Pool: $5,000 USD worth of OCEAN

- 1st place: $2,500
- 2nd place: $1,500
- 3rd place: $1,000

We will identify winners by the blockchain account they use in the competition (on Mumbai), and send the OCEAN to that account on Ethereum mainnet. We will not be sending notifications by email or DMing (we aren’t tracking that!)

### 0.2 Key dates

- Submission deadline: Wed May 3, 2023, 2023 at 23:59 UTC
- Prediction at times: Thu May 4, 2023 at 00:05 UTC, 00:10, ..., 1:00 (12 predictions total).

### 0.3 Criteria to win

The winner = whoever has lowest prediction error. That's all. :chart_with_upwards_trend:

To be eligible, competitors must produce the outcomes that this README guides. This includes:
- :white_check_mark: Created an Ocean data NFT
- :white_check_mark: On the data NFT, set a value correctly: correct field label, correct # predictions, prediction values following correct formatting, predictions encrypted with proper encoding on judges' public key
- :white_check_mark: Transferred data NFT to Ocean judges before the submission deadline
- :white_check_mark: All on _Mumbai_ network, not another network

(This is different than Rounds 1–3 which required submitting a presentation. And Round 4 which required Desights. Those are no longer requirements).

### 0.4 Developer Support

**Support.** If you encounter issues, feel free to reach out :raised_hand: 
- [Ocean #dev-support Discord](https://discord.com/channels/612953348487905282/720631837122363412)
- [Ocean #data-challenges Discord](https://discord.com/channels/612953348487905282/993828971408003152).

### 0.5 Workshops

We host workshops to walk through READMEs, and hold Q&A with our core team. 

Dates:
- Apr 25 at 3PM UTC (8 days before deadline of Wed May 3)

Location:
- [Special event on Ocean Discord](https://discord.com/invite/5VWDytWG?event=1097944942564876409)


### 0.6 Outline of this README

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
pip install predict-eth
```

### 1.3 Install other Python libraries

The READMEs use several numerical & ML libraries. In the console:
```
pip install ccxt eth_account matplotlib numpy pandas prophet requests sklearn
```

### 1.4 Do Ocean remote setup

In ocean.py's [setup-remote.md](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/setup-remote.md), follow all steps.

Make sure you're in running in Mumbai!

### 1.5 Load helper functions

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

Predictions must be one prediction every 5mins, for a 60min period. The specific times were given above. There are 12 predictions total. The output is a list with 12 items.

Here's an example with random numbers. In the same Python console:
```python
#get predicted ETH values
mean, stddev = 1650, 25.0
pred_vals = list(np.random.normal(loc=mean, scale=stddev, size=(12,)))
```

### 3.3 Calculate NMSE

We use normalized mean-squared error (NMSE) as the accuracy measure.

In the same Python console:

```python
# get the time range we want to test for
start_dt = datetime.datetime.utcnow() - datetime.timedelta(minutes=120) #must be >= 60min ago; we use 120
start_dt = round_to_nearest_timeframe(start_dt) # so that times line up
target_uts = target_12_unixtimes(start_dt)
print_datetime_info("target times", target_uts)

# get the actual ETH values at that time
import ccxt
allcex_x = ccxt.binance().fetch_ohlcv('ETH/USDT', '5m')
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

## 4.1  Publish & share via Python

In the same Python console:

```python
# Imports
from ocean_lib.ocean import crypto

# Create data NFT
data_nft = ocean.data_nft_factory.create({"from": alice}, 'Data NFT 1', 'DN1')
print(f"Created data NFT with address={data_nft.address}")

# Encrypt predictions with judges' public key, so competitors can't see. 
# NOTE: public key is *not* the same thing as address. Using address will not work.
judges_pubkey = '0x3d87bf8bde8c093a16ca5441b5a1053d34a28aca75dc4afffb7a2a513f2a16d2ac41bac68d8fc53058ed4846de25064098bbfaf0e1a5979aeb98028ce69fab6a'
pred_vals_str = str(pred_vals)
pred_vals_str_enc = crypto.asym_encrypt(pred_vals_str, judges_pubkey)

# Store predictions to data NFT, on-chain
data_nft.set_data("predictions", pred_vals_str_enc, {"from": alice})

# Transfer the data NFT to judges, for prediction tamper-resistance
judges_address = '0xA54ABd42b11B7C97538CAD7C6A2820419ddF703E'
token_id = 1
tx = data_nft.safeTransferFrom(alice.address, judges_address, token_id, {"from": alice})

# Ensure the transfer was successful
assert tx.events['Transfer']['to'].lower() == judges_address.lower()

# Print txid, as we'll use it in the next step
print(f"txid from transferring the nft: {tx.txid}")
````

## 4.3 Double-check that you submitted everything

Section 0.2 "Criteria to win" has a checklist of things you need to have done. Ensure that you've done these. If you missed any, you will _not_ be eligible.

And if that's good, then...

Congratulations! You've now made your submission to the challenge! :tada:

## Appendix: What judges will do

(You can go through this too, in order to see how it looks.)

In the terminal:
```console
export REMOTE_TEST_PRIVATE_KEY1=<judges' private key, having address 0xA54A..>
```

In the same Python console:
```python
# setup
from ocean_lib.models.data_nft import DataNFT
from ocean_lib.ocean import crypto
from predict_eth.helpers import *

ocean = create_ocean_instance("polygon-test")
alice = create_alice_wallet(ocean) # the judge is Alice

# specify target times
# start_dt = round_to_nearest_hour(datetime.datetime.now() - datetime.timedelta(hours=24)) # use this if you're following up from above
start_dt = datetime.datetime(2023, 5, 3, 23, 59) #May 3, 2023 at 23.59 UTC # judges use this
target_uts = target_12_unixtimes(start_dt)
print_datetime_info("target times", target_uts)

# get predicted ETH values
data_nft_addr = <addr of your data NFT. Judges will find this from the chain>
data_nft = DataNFT(ocean.config_dict, data_nft_addr)
pred_vals_str_enc = data_nft.get_data("predictions")
pred_vals_str = crypto.asym_decrypt(pred_vals_str_enc, alice.private_key)
pred_vals = [float(s) for s in pred_vals_str[1:-1].split(',')]

# get actual ETH values (final)
import ccxt
cex_x = ccxt.binance().fetch_ohlcv('ETH/USDT', '5m')
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


