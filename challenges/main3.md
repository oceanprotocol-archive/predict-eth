<!--
Copyright 2022 Ocean Protocol Foundation
SPDX-License-Identifier: Apache-2.0
-->

# Predict ETH Price: Round Three

## 0. Introduction

This is the main readme for the Ocean Data Challenge :: ETH Prediction Round 3.

### 0.1 Key dates

- Kickoff: Jan 16, 2023
- Submission deadline: Sun Feb 19, 2023 at 23:59 UTC
- Prediction at times: Mon Feb 20, 2023 at 1:00 UTC, 2:00, ..., 12:00 (12 predictions total).
- Winners announced: within one week. See previous challenge results [here]( https://blog.oceanprotocol.com/introducing-the-winners-of-the-eth-price-prediction-data-challenge-edition-2-6acdccb9271)

### 0.2 Criteria to win
- Weighting:
  - 50% - lowest prediction error
  - 25% - presentation of approach, and feedback
  - 25% - proper flow was used to submit. This includes: the predictions were stored to arweave, and a datatoken was shared to judges. (This README covers how to do both.)
- To be considered for winning, prediction error must lower than if the "prediction" was simply a constant.

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

### 1.2 Install other Python libraries

In the console:

```console
# Install other libraries
pip3 install ccxt eth_account matplotlib numpy pandas prophet requests sklearn
```

Note: while _this_ README doesn't use all of these modules, several follow-on READMEs do. So we install them all here, for convenience.

### 1.3 Arweave preparation

To share tamper-proof predictions, you'll use Arweave. You have two options, A and B. Please pick one and do the "prepare by" step. 

**Option A: Webapp, using [ardrive.io](https://www.ardrive.io)**
  - Pros: simple webapp
  - Cons: need AR to pay for storage.
  - Prepare by: get AR via [a faucet](https://faucet.arweave.net/) or [buying some](https://www.google.com/search?q=buy+arweave+tokens). For more details follow [this](https://docs.oceanprotocol.com/using-ocean-market/asset-hosting#arweave
) tutorial.
  
**Option B: In code, using pybundlr library**
  - Pros: pay for storage with MATIC, ETH, AR, or [other](https://docs.bundlr.network/sdk/using-other-currencies). (But not fake MATIC)
  - Cons: bundlr CLI installation is finicky, since it needs "`npm install`" globally on your system (`-g` flag)
  - Prepare by: 
    - in console, install pybundlr: `pip install pybundlr`
    - in console, install [Bundlr CLI](https://docs.bundlr.network/about/introduction): `npm install -g @bundlr-network/client`
    - get one of: [MATIC](https://polygon.technology/matic-token/), [ETH](https://ethereum.org/en/get-eth/), or AR (see "get AR via" above)

If you're not sure which option to pick, we recommend Option A because once you get AR, the rest is less error-prone.


### 1.4 Do Ocean remote setup

In ocean.py's [setup-remote.md](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/setup-remote.md), follow all steps.


### 1.5 Load helper functions

In this repo's [helpers.md](../support/helpers.md), follow all steps.

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

## 4.  Publish predictions

### 4.1 Save the predictions as a csv file

In the same Python console:
```python
file_name = "/tmp/pred_vals.csv"
save_list(pred_vals, file_name)
```

The csv will look something like:

```text
[1503.134,1512.490,1498.982,...,1590.673]
```

### 4.2 Put the csv online

You'll upload your csv to Arweave permanent decentralized file storage. This makes the predictions tamper-proof.

Recall "Arweave preparation" from section 1. Proceed the option (A or B) that you had prepared for.

**Option A: Webapp, using ardrive.io**

Go to [ardrive.io](https://www.ardrive.io) webapp and follow the GUI to upload. Copy the url of the uploaded file.

Then, in the same Python console:
```python
url = <url of uploaded file>
```
  
**Option B: In code, using pybundlr library**

In the same Python console:
```python
from pybundlr import pybundlr
file_name = "/tmp/pred_vals.csv"

# This step assumes "matic" currency. You could also use "eth", "ar", etc.
# Whatever network you choose, alice's wallet needs the corresponding funds.
url = pybundlr.fund_and_upload(file_name, "matic", alice_wallet.private_key)

#e.g. url = "https://arweave.net/qctEbPb3CjvU8LmV3G_mynX74eCxo1domFQIlOBH1xU"
print(f"Your csv url: {url}")
```

### 4.3 Publish Ocean asset

In the same Python console:
```python
name = "ETH predictions " + str(time.time()) #time for unique name
(data_nft, datatoken, ddo) = ocean.assets.create_url_asset(name, url, {"from":alice}, wait_for_aqua=False)
metadata_state = 5
data_nft.setMetaDataState(metadata_state, {"from":alice})
print(f"New asset created, with did={ddo.did}, and datatoken.address={datatoken.address}")
```

Write down the `did` and `datatoken.address`. You'll be needing to share them in the Desights entry (see below).

### 4.4 Share predictions to judges

In the same Python console:
```python
from web3.main import Web3
to_address="0xA54ABd42b11B7C97538CAD7C6A2820419ddF703E" #official judges address
datatoken.mint(to_address, Web3.toWei(10, "ether"), {"from": alice})
```

### 4.5 Enter via Desights

[Desights](https://desights.ai) is a decentralized platform for data science competitions. It's hosting Ocean's predict-eth challenges.

Please ensure that you've entered in this competition on Desights.

Now, you're complete! Thanks for being part of this competition.


## Appendix: What judges will do

In the terminal:
```console
export REMOTE_TEST_PRIVATE_KEY1=<judges' private key, having address 0xA54A..>
```

Load helper functions: Go to [helpers.md](../support/helpers.md) and follow the instructions.

In the same Python console:
```python
# setup
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


