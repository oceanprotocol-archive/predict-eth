<!--
Copyright 2022 Ocean Protocol Foundation
SPDX-License-Identifier: Apache-2.0
-->

# End-to-end example: Raw Ocean data and linear models

## Introduction

This example predicts ETH price via raw data published in Ocean, and linear models.

The raw data is: 'Open', 'High', 'Low', 'Close' and 'Volume' values, at 1 hour intervals. Predictions are at 1-hour intervals into the future.

## 1. Setup


From [Challenge 2](../challenges/main2.md), do:
- [x] Setup

## 2. Get data locally

In Python:

```python

# Download file from Ocean market (free)
ETH_USDT_did = "did:op:0dac5eb4965fb2b485181671adbf3a23b0133abf71d2775eda8043e8efc92d19"
file_name = ocean.assets.download_file(ETH_USDT_did, alice_wallet)

# Extracts dates and ether price values
allcex_uts, allcex_vals = load_from_ohlc_data(file_name)
print_datetime_info("CEX data info", allcex_uts)

# Transform timestamps to dates
dts = to_datetimes(allcex_uts)

# create a Data Frame with two columns [date,eth-prices] with dates given in intervals of 1-hour
import pandas as pd
data = pd.DataFrame({"ds": dts, "y": allcex_vals})
```

## 3.  Make predictions

### 3.1  Build an AI model

In Python:

```python
# use the last 12 hours of testing set, all the previous data is used as training
train_data = data.iloc[0:-12,:]
test_data = data.iloc[-12:,:]

# fit a linear model (Open sourced Facebook's Prophet model: https://facebook.github.io/prophet/)
# As the data is subdaily, the model will fit daily seasonality
from prophet import Prophet
model = Prophet()
model.fit(train_data)
```

### 3.2  Run the AI model to make future ETH price predictions

```python
#Predict ETH values over the range of the test set
forecast = model.predict(pd.DataFrame({"ds":test_data.ds}))
pred_vals = forecast.set_index('ds')['yhat'][-12:].to_numpy()
```

### 3.3 Calculate NMSE

```python
nmse = calc_nmse(test_data.y, pred_vals)
print(f"NMSE = {nmse}")
```

Keep iterating in step 3 until you're satisfied with accuracy. Then...


## 4.  Publish predictions
From [Challenge 2](../challenges/main2.md), do:
- [x] Publish predictions