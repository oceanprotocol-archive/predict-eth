<!--
Copyright 2022 Ocean Protocol Foundation
SPDX-License-Identifier: Apache-2.0
-->

# Quickstart: Predict Future ETH Price

This quickstart describes a flow to predict future ETH price via a local AI model.

It is used for the first [ETH Prediction Challenge](https://blog.oceanprotocol.com/ocean-protocol-announces-the-launch-of-the-eth-prediction-challenge-7b1f04cc820e)

- Kickoff: Oct 2, 2022
- Submission deadline: Oct 16, 2022 at 23:59 UTC
- Prediction at times: Oct 17, 2022 at 1:00 UTC, 2:00 UTC, ..., 23:00, 24:00. (24 predictions total). 
- Winners announced: within one week

Here are the steps:

1. Basic Setup
2. Get data locally. E.g. Binance ETH price feed
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

# Install Ocean library
pip3 install ocean-lib

# Install other libraries
pip3 install matplotlib pybundlr
```

### 1.2 Create Polygon Account (One-Time)

You'll be using Polygon network. So, please ensure that you have a Polygon account that holds some MATIC (at least a few $ worth). [More info](https://polygon.technology/matic-token/). 

### 1.3 Set envvars, for Polygon address

In the terminal:
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

### 2.1 Get ETH price data

Here, we grab Binance ETH/USDT price feed, which is published through Ocean as a free asset. You can see it on Ocean Market [here](https://market.oceanprotocol.com/asset/did:op:0dac5eb4965fb2b485181671adbf3a23b0133abf71d2775eda8043e8efc92d19).

In the same Python console:

```python
# Download file
ETH_USDT_did = "did:op:0dac5eb4965fb2b485181671adbf3a23b0133abf71d2775eda8043e8efc92d19"
file_name = ocean.assets.download_file(ETH_USDT_did, alice_wallet)
allcex_uts, allcex_vals = load_from_ohlc_data(file_name)
print_datetime_info("CEX data info", allcex_uts)
```

## 3.  Make predictions

### 3.1  Build a simple AI model

Here's where you build whatever AI/ML model you want, leveraging the data from the previous step.

This demo flow skips building a model because the next step will simply generate random predictions.

### 3.2  Run the AI model to make future ETH price predictions

Predictions must be one prediction every hour on the hour, for a 24h period: Oct 3 at 1:00am UTC, at 2:00am, at 3:00am, ..., 11.00pm, 12.00am. Therefore there are 24 predictions total.

In the same Python console:
```python
#get predicted ETH values
import random
avg = 1300
rng = 25.0
pred_vals = [avg + rng * (random.random() - 0.5) for i in range(24)]
```

### 3.3 Calculate NMSE

We use normalized mean-squared error (NMSE) as the accuracy measure.

In the same Python console:

```python
#get actual ETH values (for testing)
start_dt = datetime.datetime(2022, 10, 3, 1, 00) #Example time. Oct 14, 2022 at 1:00am
target_uts = target_24h_unixtimes(start_dt)
print_datetime_info("target times", target_uts)
#allcex_uts, allcex_vals = .. # we already have these from section 2.2
cex_vals = filter_to_target_uts(target_uts, allcex_uts, allcex_vals)

#calc nmse, plot
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
data_nft.set_metadata_state(metadata_state=5, from_wallet=alice_wallet)
print(f"New asset created, with did={asset.did}, and datatoken.address={datatoken.address}")
```

Write down the `did` and `datatoken.address`. You'll be needing to share them in the Questbook entry.

### 4.4 Share predictions to judges

In the same Python console:
```python
to_address="0xA54ABd42b11B7C97538CAD7C6A2820419ddF703E" #official judges address
datatoken.mint(to_address, ocean.to_wei(10), alice_wallet)
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

start_dt = datetime.datetime(2022, 10, 17, 1, 00) #Oct 17, 2022 at 1:00am
target_uts = target_24h_unixtimes(start_dt)
print_datetime_info("target times", target_uts)

cex_vals = filter_to_target_uts(target_uts, allcex_uts, allcex_vals)

#calc nmse, plot
nmse = calc_nmse(cex_vals, pred_vals)
print(f"NMSE = {nmse}")
plot_prices(cex_vals, pred_vals)
```