<!--
Copyright 2022 Ocean Protocol Foundation
SPDX-License-Identifier: Apache-2.0
-->

# Quickstart: Predict Future ETH Price

This quickstart describes a flow to predict future ETH price via a local AI model using data published in Ocean and accessed via The Graph using graphQL queries.

## Setup

From [challenge 1](../challenges/main1.md), do:
- [x] Setup


### Script

In Python:

```python

# Download file from Ocean market (free)
ETH_USDT_did = "did:op:deb138bcabdc21f126bc064489cd58d16792f782d2e145f0227e4d9778650243"
file_name = ocean.assets.download_file(ETH_USDT_did, alice_wallet)

# Read downloaded file
import json
f = open(file_name)

# Create dataframes, select timestamps and close value from data
# values are presented in intervals of 1 hour
import pandas as pd
data_full = pd.DataFrame(json.load(f)['data']['tokenHourDatas'])
data = pd.DataFrame({"ds": data_full.periodStartUnix, "y": data_full.close})
data.ds = ph.to_datetimes(data.ds)
data.y = data['y'].astype(float)


# use the last 12 hours of testing set, all the previous data is used as training
train_data = data.iloc[0:-12,:]
test_data = data.iloc[-12:,:]

# fit a linear model (Open sourced Facebook's Prophet model: https://facebook.github.io/prophet/)
# As the data is subdaily, the model will fit daily seasonality
from prophet import Prophet
model = Prophet()
model.fit(train_data)

#Predict ETH values over the range of the test set
forecast = model.predict(pd.DataFrame({"ds":test_data.ds}))
pred_vals = forecast.set_index('ds')['yhat'][-12:].to_numpy()

# Calculate Normalized Mean Squared Error between predictions and true (test) values
nmse = calc_nmse(test_data.y, pred_vals)
print(f"NMSE = {nmse}")

# Plot predicted and real values for ETH price
plot_prices(test_data.y, pred_vals)

