<!--
Copyright 2022 Ocean Protocol Foundation
SPDX-License-Identifier: Apache-2.0
-->

# Predict ETH Price: Round Two 

This is the main readme for the [Ocean Data Challenge :: ETH Prediction Round 2](https://questbook.app/explore_grants/about_grant/?grantId=0x9f248741962aaf27bd10f2c50aeec2d13f343611&chainId=137). 

- Kickoff: Nov 14, 2022
- Submission deadline: Dec 11, 2022 at 23:59 UTC
- Prediction at times: Dec 12, 2022 at 1:00 UTC, 2:00, ..., 12:00 (12 predictions total).
- Winners announced: within one week
- To be considered for winning, and for 250 OCEAN reward for a valid submission, prediction error must (a) lower than if the "prediction" was simply a constant (b) lower than any of the end-to-end examples' prediction errors

This readme describes a basic flow to predict future ETH price, and submit your predictions to contest judges.

Here are the steps:

1. Basic Setup
2. Get data locally
3. Make predictions
4. Publish & share predictions

## 1. Setup

### 1.1 Prerequisites & installation

Follow [Ocean.py installation guide](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/install.md)

Now, let's install Python libraries.

```python
# Install other libraries
pip3 install matplotlib pybundlr ccxt
```

You'll be using [Arweave Bundlr](https://docs.bundlr.network/docs/about/introduction) to share tamper-proof predictions. The `pybundlr` library (installed above) needs the Bundlr CLI installed. So, in the terminal do the following. (If you encounter issues, please see the Appendix.) 
```
npm install -g @bundlr-network/client
```


### 1.2 Create Polygon Account (One-Time)

You'll be using Polygon network. So, please ensure that you have a Polygon account that holds some MATIC (at least a few $ worth). [More info](https://polygon.technology/matic-token/). 

### 1.3 Set envvars, for Polygon address

Environment variables (envvars) are set differently in Windows and Mac/Linux:

Windows
```console
set REMOTE_TEST_PRIVATE_KEY1=<your Polygon private key>
```

Linux and Mac
```console
export REMOTE_TEST_PRIVATE_KEY1=<your Polygon private key>
```

### 1.4 Load helper functions

Go to [helpers.md](../support/helpers.md) and follow the instructions.

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

Predictions must be one prediction every hour on the hour, for a 12h period. The specific times were given above. There are 12 predictions total. The output is a list with 12 items.

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

You'll upload to Arweave permanent decentralized file storage, via Bundlr. This makes the predictions tamper-proof. Bundlr enables you to pay via MATIC from your Polygon account. (If you encounter issues, please see the Appendix.)

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

Load helper functions: Go to [helpers.md](../support/helpers.md) and follow the instructions.

In the same Python console:
```python
# setup
ocean = create_ocean_instance()
alice_wallet = create_alice_wallet(ocean) #you're Alice

# specify target times
start_dt = datetime.datetime(2022, 12, 12, 1, 00) #Dec 12, 2022 at 1:00am UTC
target_uts = target_12h_unixtimes(start_dt)
print_datetime_info("target times", target_uts)

# get predicted ETH values
did = <value shared by you>
order_tx_id = ocean.assets.pay_for_access_service(ddo, alice_wallet)
file_name = ocean.assets.download_asset(ddo, alice_wallet, './', order_tx_id)
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

### Appendix: If you have Arweave / Bundlr issues

This README has you upload to Arweave permanent decentralized file storage, so that predictions are tamper-proof. Above, it provided instructions to install Bundlr, which wraps Arweave. 

If you encountered issues installing it, then you need to upload to Arweave in a different way. At the end of the process, you need a shareable url. The Arweave ecosystem has several webapps that you might consider. One of the leading apps is ArDrive. [Here's an ArDrive tutorial](https://docs.rawrshak.io/tutorials/developer/rawrshak-dapp/upload-data-to-arweave) to get going. 


