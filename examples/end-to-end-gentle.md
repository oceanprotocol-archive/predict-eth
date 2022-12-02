# End-to-end example: Gentle introduction

This is an example full submission to the challenge. You can use it as starting point, for your own work.

Remember:
-  You do not have to win, just make a full submission (like this one)
-  This competition has several rounds, you can always make improvements for the next edition.

A few remarks:
- The code presented here is repetitive and does not benefit from neither Python's nor Pandas methods.
- Our purpose with this code is to present a very expressive example that everybody can understand in their first read.

Requirements:
- The code presented here and the instructions work for all operating systems.
- You need to have a Python 3.x version installed.
- There are several ways to make this code significantly shorter, more efficient and not repetitive. This code did not benefit from any of these opportunities. Our objective is to present a submission as clearly as possible for all sorts of audiences.

Our recommendations:
- Think deeply about which variables you can use to predict the price correctly -- **this is where your magic comes in!**
- If it is your first time in this competition; please concentrate on submitting a full and correct entry. You will have more opportunities to improve on your approach in subsequent editions.

Ready?, let's start! :rocket: :rocket: :rocket:

---

## 0. Understanding the Challenge

In this example we plan to predict the daily Binance ETH price.

In essence, what we are being asked to do is present a model.

In Data Science a model is just an equation that renders a value when some variables are submitted.

A model often looks like this:

**ETH_Price = Predictor Variable 1 + Predictor Variable 2 + ... + Predictor Variable n + Error**

So this is what is being asked: ETH_Price is the sum of a group of features (in Data Science the Predictor Variables are called features).

But... there is a catch. The error. The error affects the features and hence the prediction.

To get a good prediction we have to make the error as small as possible.

Can we do it? Let's give it a try by first gathering the data for our model.

---

## 1. Setup

From [Challenge 2](../challenges/main2.md), do:
- [x] Setup

In the console:
```console
# Install libraries using pip
pip install pandas ccxt
pip install -U scikit-learn
```

Now, create a python file. You can use any filename. In the console:
```console
touch predict_eth.py
```

Open the file. Add the following content to the file:
```python
#import libraries
import pandas as pd
import numpy as np
import ccxt
import time
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
```

---

## 2. Getting the Data:

### 2.1 Introduction

We need the ETH Price data and the Predictor variables data.

The ETH Price will help us know how accurate is our model when we compare its result to the true price.

The Predictor variables data include all sorts of data that you think have an influence in the ETH Price.

Of course, please remember that a big part of the competition is about you using your magic to find better predictor variables than the ones presented here.

Remember: A good analysis starts with good data.

In Data Science a [DataFrame](https://pandas.pydata.org/docs/getting_started/intro_tutorials/01_table_oriented.html) is the equivalent to an spreadsheet.

We will create a DataFrame for every piece of data we gather.

Each DataFrame will have a column named "Date".

We will make sure that every "Date" column has the type 'datetime', so we can compare them when we merge all the DataFrames.


### 2.2 Getting data from Ocean - hourly stock prices

There are many sites with great data and, of course, you are welcome to use any of them.

In this example we are using hourly stock price data of Tesla, Amazon, Google and Apple for the last three months.

The data is available on Ocean market for free:
[https://market.oceanprotocol.com/asset/did:op:59e8ce4a599e7d3efc3f23ce68c6ae92b08e5764c0a8f801c47ae00c47db1522](https://market.oceanprotocol.com/asset/did:op:59e8ce4a599e7d3efc3f23ce68c6ae92b08e5764c0a8f801c47ae00c47db1522)

For each stock we have 5 variables: open, close, high, low and volume -- all for every hour and for the last three months.

To build a DataFrame for each stock we will import the csv, rename the columns, and type the date to datetime (so we can compare dates later).

```python
# Apple Stock
df_tech_apple = pd.read_csv('AAPL_1hr.csv', usecols=['time','open', 'high', 'low', 'close', 'volume']) #open csv
df_tech_apple = df_tech_apple.rename(columns={'time': 'Date','open': 'AAPL_Open', 'high': 'AAPL_High', 'low': 'AAPL_Low', 'close': 'AAPL_Close', 'volume': 'AAPL_Vol'}) # rename the columns
df_tech_apple['Date'] = pd.to_datetime(df_tech_apple['Date'], format="%m/%d/%Y %H:%M") # date to datetime type
```
We repeat the same process for the other three stocks:
```python
# Google Stock
df_tech_google = pd.read_csv('GOOG_1hr.csv', usecols=['time','open', 'high', 'low', 'close', 'volume'])
df_tech_google = df_tech_google.rename(columns={'time': 'Date','open': 'GOOG_Open', 'high': 'GOOG_High', 'low': 'GOOG_Low', 'close': 'GOOG_Close', 'volume': 'GOOG_Vol'})
df_tech_google['Date'] = pd.to_datetime(df_tech_google['Date'], format="%m/%d/%Y %H:%M")

# Tesla Stock
df_tech_tesla = pd.read_csv('TSLA_1hr.csv', usecols=['time','open', 'high', 'low', 'close', 'volume'])
df_tech_tesla = df_tech_tesla.rename(columns={'time': 'Date','open': 'TSLA_Open', 'high': 'TSLA_High', 'low': 'TSLA_Low', 'close': 'TSLA_Close', 'volume': 'TSLA_Vol'})
df_tech_tesla['Date'] = pd.to_datetime(df_tech_tesla['Date'], format="%m/%d/%Y %H:%M")

# Amazon Stock
df_tech_amazon = pd.read_csv('AMZN_1hr.csv', usecols=['time','open', 'high', 'low', 'close', 'volume'])
df_tech_amazon = df_tech_amazon.rename(columns={'time': 'Date','open': 'AMZN_Open', 'high': 'AMZN_High', 'low': 'AMZN_Low', 'close': 'AMZN_Close', 'volume': 'AMZN_Vol'})
df_tech_amazon['Date'] = pd.to_datetime(df_tech_amazon['Date'], format="%m/%d/%Y %H:%M")
```


### 2.3 Getting ETH price data

For this data, we use the [ccxt](https://github.com/ccxt/ccxt) package.

This library comes with a limitation, there is a limit of 500 rows per request.

We will need to repeat the query a few times to get to the last three months of data.

After that we will concatenate the queries to get the ETH_Price DataFrame.

Here is how to get the first 500 results:
```python
# Introduce the initial date (August 9th, 2022) in a datetime function
first_500 = datetime(2022, 8, 9)

# Transform the datetime to a timestamp (for this function ccxt only takes timestamps)
first_500_timestamp_2022 = time.mktime(first_500.timetuple())

# ccxt requires removing the decimals and adding miliseconds
first_500_timestamp_2022 = int(first_500_timestamp_2022) * 1000

# Our first 500 results
data_first_500 = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h', since=first_500_timestamp_2022, limit=500)

# Create DataFrame with this data
df_first_500 = pd.DataFrame(data_first_500)

# Add column names
df_first_500 = df_first_500.rename(columns={0: 'TimeStamp', 1: 'Open', 2: 'Highest', 3: 'Lowest', 4: 'Close', 5: 'Volume'})

# Convert unix time (provided in miliseconds) to a Date (remember that we need datetime to compare)
df_first_500['TimeStamp'] = pd.to_datetime(df_first_500['TimeStamp'], unit='ms')

# Rename column TimeStamp to Date
df_first_500 = df_first_500.rename(columns={'TimeStamp': 'Date'})
```

The code to get the other four DataFrames:
```python
second_500 = datetime(2022, 8, 29)
second_500_timestamp_2022 = time.mktime(second_500.timetuple())
second_500_timestamp_2022 = int(second_500_timestamp_2022) * 1000
data_second_500 = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h', since=second_500_timestamp_2022, limit=500)
df_second_500 = pd.DataFrame(data_second_500)
df_second_500 = df_second_500.rename(columns={0: 'TimeStamp', 1: 'Open', 2: 'Highest', 3: 'Lowest', 4: 'Close', 5: 'Volume'})
df_second_500['TimeStamp'] = pd.to_datetime(df_second_500['TimeStamp'], unit='ms')
df_second_500 = df_second_500.rename(columns={'TimeStamp': 'Date'})

third_500 = datetime(2022, 9, 18)
third_500_timestamp_2022 = time.mktime(third_500.timetuple())
third_500_timestamp_2022 = int(third_500_timestamp_2022) * 1000
data_third_500 = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h', since=third_500_timestamp_2022, limit=500)
df_third_500 = pd.DataFrame(data_third_500)
df_third_500 = df_third_500.rename(columns={0: 'TimeStamp', 1: 'Open', 2: 'Highest', 3: 'Lowest', 4: 'Close', 5: 'Volume'})
df_third_500['TimeStamp'] = pd.to_datetime(df_third_500['TimeStamp'], unit='ms')
df_third_500 = df_third_500.rename(columns={'TimeStamp': 'Date'})

fourth_500 = datetime(2022, 10, 8)
fourth_500_timestamp_2022 = time.mktime(fourth_500.timetuple())
fourth_500_timestamp_2022 = int(fourth_500_timestamp_2022) * 1000
data_fourth_500 = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h', since=fourth_500_timestamp_2022, limit=500)
df_fourth_500 = pd.DataFrame(data_fourth_500)
df_fourth_500 = df_fourth_500.rename(columns={0: 'TimeStamp', 1: 'Open', 2: 'Highest', 3: 'Lowest', 4: 'Close', 5: 'Volume'})
df_fourth_500['TimeStamp'] = pd.to_datetime(df_fourth_500['TimeStamp'], unit='ms')
df_fourth_500 = df_fourth_500.rename(columns={'TimeStamp': 'Date'})

fifth_500 = datetime(2022, 10, 28)
fifth_500_timestamp_2022 = time.mktime(fifth_500.timetuple())
fifth_500_timestamp_2022 = int(fifth_500_timestamp_2022) * 1000
data_fifth_500 = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h', since=fifth_500_timestamp_2022, limit=200)
df_fifth_500 = pd.DataFrame(data_fifth_500)
df_fifth_500 = df_fifth_500.rename(columns={0: 'TimeStamp', 1: 'Open', 2: 'Highest', 3: 'Lowest', 4: 'Close', 5: 'Volume'})
df_fifth_500['TimeStamp'] = pd.to_datetime(df_fifth_500['TimeStamp'], unit='ms')
df_fifth_500 = df_fifth_500.rename(columns={'TimeStamp': 'Date'})
```

Finally we concatenate the DataFrames:
```python
# Concatenate the DataFrames
ETH_Price = pd.concat([df_first_500, df_second_500, df_third_500, df_fourth_500, df_fifth_500])

# Remove all columns but Date and Price
ETH_Price.drop(['Open', 'Highest', 'Lowest', 'Volume'], axis=1, inplace=True)

# Rename the column 'Close' to 'ETH_Price'
ETH_Price = ETH_Price.rename(columns={'Close': 'ETH_Price'})

# Sort the values by date and reset the indexes of the DataFrame:
ETH_Price = ETH_Price.sort_values(by="Date", ascending=False)
ETH_Price.reset_index(drop=True, inplace=True)
```

### 2.4 Put it all together in a 'base' DataFrame

Good job! We now have the ETH_Price and four major technology stocks prices. All per hour and for the last three months.

In addition, all DataFrames have a column named 'Date' that is of the datetime type. So we can compare them all.

Let's build the "base" DataFrame. Which is an initial DataFrame that contains all the raw data.

If you explore the DataFrames you will see that there are significant differences. There is missing data, some rows are missing, etc.

Fortunately Pandas will take of these differences for us.

We will only merge into the base DataFrame those dates and times that are common to all our DataFrames.

```python
base = pd.merge(ETH_Price, df_tech_apple, how='inner', on='Date') # Create the 'base' DataFrame out of ETH_Price and 'df_tech_apple'
base = pd.merge(base, df_tech_google, how='inner', on='Date') # add 'df_tech_google' to base
base = pd.merge(base, df_tech_tesla, how='inner', on='Date') # add 'df_tech_tesla' to base
base = pd.merge(base, df_tech_amazon, how='inner', on='Date') # add 'df_tech_amazon' to base
```

Ready to start the analysis! As you can see in Data Science gathering the data is quite a labor intensive process.

In this section we have achieved a lot:
- Explained in detail how to get a true ETH price from ccxt
- Gathered and processed four technology stock predictors for ETH
- Created the base DataFrame, which contains all the raw data for our analysis

Good job! 

---

## 3. Data Exploration

Before running the model we check that there are no NaN or empty values and that all cells have the correct type

```python
base.info()
```

We can also explore the relationship between variables with a correlation table

```python
base.corr(method='pearson', numeric_only=True)
```

### 3.1 Model

Let's give it a try by using a model that includes all the data

```python
# Instantiate a model object
model = LinearRegression()

# Add predictor variables
X = base[['AAPL_Open', 'AAPL_High', 'AAPL_Low', 'AAPL_Close', 'AAPL_Vol', 'GOOG_Open', 'GOOG_High', 'GOOG_Low', 'GOOG_Close', 'GOOG_Vol', 'TSLA_Open', 'TSLA_High', 'TSLA_Low', 'TSLA_Close', 'TSLA_Vol', 'AMZN_Open', 'AMZN_High', 'AMZN_Low', 'AMZN_Close', 'AMZN_Vol']]

# Add the target
y = base['ETH_Price']


# We use the last 12 hours for testing, all the rest of data is for training

# Target y_test and y_train
y_test = y.iloc[0:12]
y_train = y.iloc[12:]

# # Predictors X_test and X_train
X_test = X.iloc[0:12]
X_train = X.iloc[12:]

# Create the fitted model
model.fit(X_train, y_train)

# These are the next 12 predictions to submit to the judges
pred_vals = model.predict(X_test)
print() # [1305.27447798, 1304.7120102, 1304.9693135, ... , 1339.98662918, 1281.38973626]
```

### 3.2 Improving our model using normalized mean-squared error (NMSE)

Now that we have our predictions, let's get the real numbers so we can compare them.

The nmse is a frequently used accuracy measurement for these sort of comparisons.

We are using the nmse for comparing our pred_vals with the next 12 real prices of the target (in our case ETH)

```python
# To start we get the most recent date from our base dataset
most_recent_date_base = base.at[0,'Date'] # 2022-11-04 20:00:00

# Same as before we create a datetime function
most_recent_date_base_datetime = most_recent_date_base.to_pydatetime()

# The initial datetime will be the next rounded hour
initial_time = most_recent_date_base_datetime + timedelta(hours=1) # 2022-11-04 21:00:00

# Same as before we transform the initial datetime to a timestamp
initial_time_timestamp = time.mktime(initial_time.timetuple())

# as ccxt requires, we remove the decimals and add miliseconds
initial_time_timestamp = int(initial_time_timestamp) * 1000

# With ccxt we get the next 12 real values of the target ETH price
cex_vals_array = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h', since=initial_time_timestamp, limit=12)

# We know that in the array that is returned from ccxt
# the fourth value is the 'close'
# We can get all the closes with a list comprehension
cex_vals = [close[4] for close in cex_vals_array]

# The nmse compares our predictions with the real values for the next 12 hours
nmse = calc_nmse(cex_vals, predictions)
print(f'NMSE = {nmse}') # result is 0.0481
```


These numbers are quite acceptable for an initial submission! good job!

But we have one question:

While going through this example; didn't you notice things that could be improved to get a better prediction and a lower nmse?

This full example shows how to create the model and evaluate it before even making a submission.

But, as you have probably figured by now, there are plenty of opportunities to make it more accurate (number of datapoints, normalization, etc.)

And that is what Ocean's ETH Predict challenge is all about.

So, can you help us improve this?

---

## 4. Publish Predictions

Once you have your predictions you can publish them following these easy steps:

From [Challenge 2](../challenges/main2.md), do:
- [x] Publish predictions
