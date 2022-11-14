
# End-to-end example: Raw data, MA and EMA


## Introduction

This example predicts ETH price via raw data from CCXT, Moving Average (MA) and Exponential Moving Average (EMA). MA and EMA are are frequently-used investor indicators.

The raw data is: 'Open', 'High', 'Low', 'Close' and 'Volume' values, at 1 hour intervals. Predictions are at 1-hour intervals into the future.

Relevant information:
- This script is executed in real UTC time.
- It uses 500 datapoints (the ccxt limit per query)
- Data includes weekends and full 24h days.
- The same analysis is conducted in three scenarios: real unaltered data, MA and EMA data.
- Each scenario has two phases. Eliminate features using RFE and present a linear regression with the relevant features. 

Limitations:
- We use the coefficients to determine feature importance in RFE.
- This is an example. Thereby the analysis of spurious statistical relathionships between regressive variables is omitted (hence the results).

Results:
|               |   Raw Data    |      MA       |      EMA      |
| ------------- | ------------- | ------------- | ------------- |
|  r²           |     99.67%    |     98.81%    |     99.93%    |
|  nmse         |  2.37 * 10⁻5  |  8.05 * 10⁻5  |  5.21 * 10⁻6  |


## 1. Setup

From [Challenge 2](../challenges/main2.md), do:
- [x] Setup

In the console:
```console
pip install pandas ccxt 
pip install -U scikit-learn
```

In the same console, run Python console:
```console
python
```

First, let's do some imports. In the Python console:
```python
from datetime import datetime, timezone
import time
import ccxt
import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# add nmse helper function
def calc_nmse(y, yhat) -> float:
    assert len(y) == len(yhat)
    y, yhat = np.asarray(y), np.asarray(yhat)
    range_y = max(y) - min(y)    
    nmse = np.sqrt(np.average(((yhat - y) / range_y) ** 2))
    return nmse

```


## 2. Scenario: make predictions with raw data

In the same Python console:

```python
# Create a UTC datetime object with today's date and current running hour
now = datetime.now(timezone.utc)
now_floor = now.replace(minute=0, second=0, microsecond=0)

# Transform the datetime to a timestamp (for this function ccxt only takes timestamps)
now_floor_timestamp = time.mktime(now_floor.timetuple())

# ccxt requires removing the decimals and adding miliseconds
now_timestamp = int(now_floor_timestamp) * 1000

# Get the 500 items
data_ETH = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h')

# Create DataFrame with this data
df_data_ETH = pd.DataFrame(data_ETH)

# Add column names
df_data_ETH = df_data_ETH.rename(columns={0: 'TimeStamp', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume'})

# Convert unix time (provided in miliseconds) to a Date (remember that we need datetime to compare)
df_data_ETH['TimeStamp'] = pd.to_datetime(df_data_ETH['TimeStamp'], unit='ms')

# Rename column TimeStamp to Date
df_data_ETH = df_data_ETH.rename(columns={'TimeStamp': 'Date'})

# Reset the indexes of the DataFrame
df_data_ETH.reset_index(drop=True, inplace=True)

# Verify that there are no NaN or empty values
df_data_ETH.info()

# Dependent Variable (DV) - to be used in all scenarios
y = df_data_ETH['Close']

# Add predictor variables
X = df_data_ETH[['Open', 'High', 'Low', 'Volume']]

# RFE
estimator = SVR(kernel='linear')
selector = RFE(estimator, step=1)
selector = selector.fit(X, y)
selected= selector.support_.tolist()

# Instantiate a model object
model = LinearRegression()

# Add selected predictor variables
cols_selected = [index for bol, index in zip(selected, X) if bol]
X_selected = df_data_ETH[cols_selected]

# Partition data
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, shuffle=True, train_size=0.3)

# Create the fitted model
model.fit(X_train, y_train)

# Predict the next values
yhat_test = model.predict(X_test)

# Evaluate the model
r2 = r2_score(y_test, yhat_test)
nmse = calc_nmse(y_test, yhat_test)

# Print results
print(f'r2 is {r2}')
print(f'nmse is {nmse}')
```


## 3. Scenario: make predictions with MA-21

MA-21 is Moving Average with 21-datapoint interval. (Investors often use the 21 datapoint interval.)

We use the code of the raw data scenario.

Sections 1 & 2 operated in the Python console. To make things easier for this step: please create your own .py script, and copy & paste Python code from sections 1 & 2 into it. Then do the following changes, to make it work in MA-21 scenario.

Replace the "Add predictor variables" section for this one:

```python
# Add predictor variables
df_MA_data_ETH=df_data_ETH.rolling(21).mean(numeric_only=True) # new DataFrame with 21 MA calculations
df_MA_data_ETH=df_MA_data_ETH.dropna() # remove NaN rows
y = y.iloc[20:] # remove first 20 rows
X = df_MA_data_ETH[['Open', 'High', 'Low', 'Close', 'Volume']]
```

In "Add selected predictor variables" replace only this line:

```python
# Add predictor variables
X_selected = df_data_ETH[cols_selected] # Remove this line
X_selected = df_MA_data_ETH[cols_selected] # Add this line
```


## 4. Scenario: make predictions with EMA-21

EMA-21 is Exponential Moving Average with 21-datapoint interval.

Just like the previous section: create a .py script and copy & paste the code from sections 1 & 2 into it. Then do the following changes, to make it work in EMA-21 scenario.

Replace the "Add predictor variables" section for this one:

```python
# Add predictor variables
df_EMA_data_ETH=df_data_ETH.ewm(span=21, adjust=False).mean(numeric_only=True) # new DataFrame with 21 EMA calculations
X = df_EMA_data_ETH[['Open', 'High', 'Low', 'Close', 'Volume']]
```

In "Add selected predictor variables" replace only this line:

```python
# Add predictor variables
X_selected = df_data_ETH[cols_selected] # Remove this line
X_selected = df_EMA_data_ETH[cols_selected] # Add this line
```
