# Real time 1 hour ETH prediction using raw data, moving average and exponential moving average

Moving Average (MA) and Exponential Moving Average (EMA) are two of the most frequently used investor indicators.

Investors often use the 21 datapoint interval.

This example presents the predictive power of 'Open', 'High', 'Low', 'Close' and 'Volume' for 1 hour intervals of ETH price.

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

---

## 1. Create en environment and install the libraries

Step 1: Creating an environment named "example":
```
python -m venv example
```

Step 2: Activate the environment in Linux or Windows:
```
source ./example/bin/activate
```
For Windows:
```
example\Scripts\activate
```

Step 3: Install the Pandas, ccxt and scikit-learn libraries using pip:
```
pip install pandas
```
```
pip install ccxt
```
```
pip install -U scikit-learn
```

Step 4: Create a python file (you can use any name for the file, for example 'predict1h_eth'):
```
touch predict1h_eth.py
```

Step 5: Open the file and import these libraries:
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
```

---


## Setup

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

# nmse helper function
def calc_nmse(y, yhat) -> float:
    assert len(y) == len(yhat)
    mse_xy = np.sum(np.square(np.asarray(y) - np.asarray(yhat)))
    mse_x = np.sum(np.square(np.asarray(y)))
    nmse = mse_xy / mse_x
    return nmse
```


## Raw Data

```python
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
predictions = model.predict(X_test)

# Evaluate the model
r2 = r2_score(y_test, predictions)
nmse = calc_nmse(y_test, predictions)

# Print results
print(f'r2 is {r2}')
print(f'nmse is {nmse}')
```


## MA-21

We use the code of the raw data scenario.

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


## EMA-21

We use the code of the raw data scenario.

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
