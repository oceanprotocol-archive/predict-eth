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
- Do this repo's [helpers.md](../support/helpers.md)


## 2. Get data locally

In the Python console:

```python
import ccxt
cex_x = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h')
allcex_uts = [xi[0]/1000 for xi in cex_x] # timestamps
allcex_vals = [xi[4] for xi in cex_x] # ETH prices

# Extracts dates and ether price values
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

```python continuation
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

```python continuation
#Predict ETH values over the range of the test set
forecast = model.predict(pd.DataFrame({"ds":test_data.ds}))
pred_vals_test = forecast.set_index('ds')['yhat'][-12:].to_numpy()
```

### 3.3 Calculate NMSE

In the same Python console:

```python continuation
# now, we have predicted and actual values. Let's find error, and plot!
cex_vals = test_data.y
nmse = calc_nmse(cex_vals, pred_vals_test)
print(f"NMSE = {nmse}")
plot_prices(cex_vals, pred_vals_test)
```

### 3.4 Optimize hyperparameters for better NMSE! (Optional)

In the same Python console:

#### 3.4.1 Imports & suppress spam logs

```python continuation
# Do the imports
import itertools
import numpy as np
import logging
from prophet.diagnostics import (
    cross_validation, performance_metrics
)

# Suppress spam debug and info logs from cmdstanpy
logger = logging.getLogger('cmdstanpy')
logger.addHandler(logging.NullHandler())
logger.propagate = False
logger.setLevel(logging.CRITICAL)
```

#### 3.4.2 Generate cross-validation parameters

If you are wondering what these parameters are and/or what cross-validation mean, [here](https://blog.oceanprotocol.com/capitalize-with-ocean-protocol-a-predict-eth-tutorial-b2da136633f0) you can find a brief introduction to what Prophet does under the hood.
```python continuation
# Set parameters for doing cross-validation
horizon = "12 hours"
initial = "15 days"
period = "12 hours"
```

#### 3.4.3 Generate hyperparameters combination
```python continuation
# Generate grid for hyperparameters
param_grid = {  
    "changepoint_prior_scale": [0.001, 0.01, 0.1, 0.5],
    "seasonality_prior_scale": [0.01, 0.1, 1.0, 10.0],
    "changepoint_range": [0.8, 0.85, 0.95],
}
all_params = [
    dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())
]
```

#### 3.4.4 Execute cross-validation and retrieve best set of hyperparameters
```python continuation
# Empty list that will contain RMSEs for each combination of hyperparams
rmses = []

# Iterate over hyperparameters and save results to compare
for params in all_params:
    m = Prophet(**params).fit(train_data)  # Fit model with given params
    df_cv = cross_validation(m, initial=initial, horizon=horizon, period=period, parallel="processes")
    df_p = performance_metrics(df_cv, rolling_window=1)
    rmses.append(df_p['rmse'].values[0])

# Find the best parameters
tuning_results = pd.DataFrame(all_params)
tuning_results['rmse'] = rmses
print(tuning_results) # It will give you an idea of the results

# Extract best set of hyperparameters and print them
best_params = all_params[np.argmin(rmses)]
print(best_params)
```

#### 3.4.5 NMSE Comparison before and after tuning

Now that we have found the best hyperparameters, we should run again 3.1 to 3.3 to compute the NSME with the new hyparameters.

```python continue
model = Prophet(**best_params)
model.fit(train_data)
forecast = model.predict(pd.DataFrame({"ds":test_data.ds}))
pred_vals_test = forecast.set_index('ds')['yhat'][-12:].to_numpy()
cex_vals = test_data.y
nmse = calc_nmse(cex_vals, pred_vals_test)
print(f"NMSE = {nmse}")
```
Doing this exercise the NMSE goes from `0.00066` to `0.00033` having a relative improvement of 50%.

### 3.5 Make final predictions

In the same Python console:

```python continuation
# fit model with all the available data

model = Prophet(**best_params) # Change to Prophet() if 3.4 skipped
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