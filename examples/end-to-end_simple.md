<!--
Copyright 2022 Ocean Protocol Foundation
SPDX-License-Identifier: Apache-2.0
-->

# Simple End-to-end Example

## 0. Introduction

This example predicts future ETH price, using simple input data (just historical ETH price) and a simple model (linear dynamical model).

Predictions are 1h, 2h, ..., 12h into the future.

## 1. Setup

We assume you've already done [main3.md](../challenges/main3.md#1-setup) "Setup".

If needed, re-setup in Python:
- Do ocean.py [setup-remote.md](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/setup-remote.md#6-setup-in-python) "Setup in Python"
- And do: `from predict_eth.helpers import *`


## 2. Get data locally

In the Python console:

```python

import ccxt
cex_x = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h')
allcex_uts = [xi[0]/1000 for xi in cex_x] # timestamps
allcex_vals = [xi[4] for xi in cex_x] # ETH prices

# # Extracts dates and ether price values
print_datetime_info("CEX data info", allcex_uts)

# Transform timestamps to dates
dts = to_datetimes(allcex_uts)

# create a Data Frame with two columns [date,eth-prices] with dates given in intervals of 1-hour
import pandas as pd
data = pd.DataFrame({"ds": dts, "y": allcex_vals})
```

## 3.  Make predictions

### 3.1  Build an AI model

In the same Python console:

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

In the same Python console:

```python
#Predict ETH values over the range of the test set
forecast = model.predict(pd.DataFrame({"ds":test_data.ds}))
pred_vals_test = forecast.set_index('ds')['yhat'][-12:].to_numpy()
```

### 3.3 Calculate NMSE and make final predictions

In the same Python console:

```python
# now, we have predicted and actual values. Let's find error, and plot!
cex_vals = test_data.y
nmse = calc_nmse(cex_vals, pred_vals_test)
print(f"NMSE = {nmse}")
plot_prices(cex_vals, pred_vals_test)
```

Keep iterating in step 3 until you're satisfied with accuracy. Then...

```python
# fit model with all the available data
model = Prophet()
model.fit(data)

# generate dates for prediction (12 hours ahead of the latest datapoint in the data time)
future_dates = model.make_future_dataframe(periods=12, freq="h", include_history=False)

# predcit eth values on future_dates
forecast = model.predict(future_dates)
pred_vals = forecast.set_index('ds')['yhat'].to_numpy()

```


## 4.  Publish predictions
From [Challenge 3](../challenges/main3.md), do:
- [x] Publish predictions