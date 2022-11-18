<!--
Copyright 2022 Ocean Protocol Foundation
SPDX-License-Identifier: Apache-2.0
-->

# Predict ETH Price: Round Two 

This readme describes a flow to predict future ETH price via a local AI model.

It is used for the second ETH Prediction Challenge. (Not announced yet.)

- Kickoff: Nov 14, 2022
- Submission deadline: Dec 11, 2022 at 23:59 UTC
- Prediction at times: Dec 12, 2022 at 1:00 UTC, 2:00, ..., 12:00 (12 predictions total).
- Winners announced: within one week
- To be considered for winning, and for 250 OCEAN reward for a valid submission, prediction error must (a) lower than if the "prediction" was simply a constant (b) lower than any of the end-to-end examples' prediction errors

Here are the steps:

1. Basic Setup
2. Get data locally
3. Make predictions
4. Publish & share predictions

## 1. Setup

### 1.1 Prerequisites & installation

Prerequisites:
- Linux/MacOS
- Python 3.8.5+
- [Arweave Bundlr](https://docs.bundlr.network/docs/about/introduction): `npm install -g @bundlr-network/client` 

Now, let's install Python libraries. Open a terminal and:
```console
# Initialize virtual environment and activate it.
python3 -m venv venv
source venv/bin/activate

# Avoid errors for the step that follows
pip3 install wheel

# Install libraries
pip3 install ocean-lib matplotlib pybundlr ccxt

# Install bundlr cli to be able to run pybundlr
npm install -g @bundlr-network/client
```

### 1.2 Create Polygon Account (One-Time)

You'll be using Polygon network. So, please ensure that you have a Polygon account that holds some MATIC (at least a few $ worth). [More info](https://polygon.technology/matic-token/). 

### 1.3 Set envvars, for Polygon address

In the terminal:
```console
export REMOTE_TEST_PRIVATE_KEY1=<your Polygon private key>
```

### 1.4 Load helper functions

Load helper functions. See [helpers.md](../examples/helpers.md). 

### 1.5 Setup in Python, for Polygon

In the terminal, run Python: `python`

In the Python console:
```python
ocean = create_ocean_instance()
alice_wallet = create_alice_wallet(ocean) #you're Alice
```

## 2. Get data locally

Here, use whatever data you wish.

It can be static data or streams, free or priced, raw data or feature vectors or otherwise. It can be published via Ocean, or not.

The [main README](../README.md) links to some options. 

## 3.  Make predictions

### 3.1  Build a simple AI model

Here, build whatever AI/ML model you want, leveraging the data from the previous step. The [main README](../README.md) links to some options. 

This demo flow skips building a model because the next step will simply generate random predictions.

### 3.2  Run the AI model to make future ETH price predictions

Predictions must be one prediction every hour on the hour, for a 12h period: (TBD DATE) at 1am, 2am, 3am, 4am, 5am, 6am, 7am, 8am, 9am, 10am, 11am, 12pm (UTC). Therefore there are 12 predictions total. The output is a list with 12 items.

Here's an example with random numbers. In the same Python console:
```python
#get predicted ETH values
mean, stddev = 1300, 25.0
pred_vals = list(np.random.normal(loc=mean, scale=stddev, size=(12,)))
```

### 3.3 Calculate NMSE

We use normalized mean-squared error (NMSE) as the accuracy measure.

In the same Python console:

```python
# get the time range we want to test for
start_dt = datetime.datetime.now() - datetime.timedelta(hours=24) #must be >= 12h ago
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

You'll upload to Arweave permanent decentralized file storage, via Bundlr. This makes the predictions tamper-proof. Bundlr enables you to pay via MATIC from your Polygon account.

In the same Python console:
```python
from pybundlr import pybundlr
file_name = "/tmp/pred_vals.csv"
url = pybundlr.fund_and_upload(file_name, "matic", alice_wallet.private_key)
#e.g. url = "https://arweave.net/qctEbPb3CjvU8LmV3G_mynX74eCxo1domFQIlOBH1xU"
print(f"Your csv url: {url}")
```

### 4.3 Publish Ocean asset

In the same Python console:
```python
name = "ETH predictions " + str(time.time()) #time for unique name
(data_nft, datatoken, asset) = ocean.assets.create_url_asset(name, url, alice_wallet, wait_for_aqua=False)
metadata_state = 5
data_nft.setMetaDataState(metadata_state, {"from":alice_wallet})
print(f"New asset created, with did={asset.did}, and datatoken.address={datatoken.address}")
```

Write down the `did` and `datatoken.address`. You'll be needing to share them in the Questbook entry.

### 4.4 Share predictions to judges

In the same Python console:
```python
from web3.main import Web3
to_address="0xA54ABd42b11B7C97538CAD7C6A2820419ddF703E" #official judges address
datatoken.mint(to_address, Web3.toWei(10, "ether"), {"from": alice_wallet})
```

Finally, ensure you've filled in your Questbook entry.

Now, you're complete! Thanks for being part of this competition.


## Appendix: What judges will do

In the terminal:
```console
export REMOTE_TEST_PRIVATE_KEY1=<judges' private key, having address 0xA54A..>
```

Do the steps in "Appendix: Load helper functions".

In the same Python console:
```python
#setup
ocean = create_ocean_instance()
alice_wallet = create_alice_wallet(ocean) #you're Alice

#get predicted ETH values
did = <value shared by you>
file_name = ocean.assets.download_file(did, alice_wallet)
pred_vals = load_list(file_name)

#get actual ETH values (final)
ETH_USDT_did = "did:op:0dac5eb4965fb2b485181671adbf3a23b0133abf71d2775eda8043e8efc92d19"
file_name = ocean.assets.download_file(ETH_USDT_did, alice_wallet)
allcex_uts, allcex_vals = load_from_ohlc_data(file_name)
print_datetime_info("CEX data info", allcex_uts)

start_dt = datetime.datetime(2022, 12, 12, 1, 00) #Dec 12, 2022 at 1:00am UTC
target_uts = target_12h_unixtimes(start_dt)
print_datetime_info("target times", target_uts)

cex_vals = filter_to_target_uts(target_uts, allcex_uts, allcex_vals)

#calc nmse, plot
nmse = calc_nmse(cex_vals, pred_vals)
print(f"NMSE = {nmse}")
plot_prices(cex_vals, pred_vals)
```


