# End-to-end example: Compare models

Given the task of predicting ETH for 12 hours in the future, several approaches  are possible. They either learn an independent model to predict the prices at each hour, or learn a model that makes direct predictions.

In this README, each model uses the previous 12 hours' of prices to predict the next 12 hours' worth.  

Four modeling approaches are used: Linear Regression, Random Forests, Support Vector Machine, and a two-layer densely-connected neural nework.

## 1. Setup

We assume you've already done [main3.md](../challenges/main3.md#1-setup) "Setup".

Let's install TensorFlow. We do it here, and not earlier, because it's 500MB. In the console:

```console
pip3 install tensorflow
```

Finally, re-setup in Python:
- Do ocean.py [setup-remote.md](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/setup-remote.md#6-setup-in-python) "Setup in Python"
- Do this repo's [helpers.md](../support/helpers.md)


## 2. Get data locally

In the Python console:

```python
import ccxt
import pandas as pd
import numpy as np
import requests

cex_x = ccxt.binance().fetch_ohlcv('ETH/USDT', '1h')

# create a Data Frame with two columns [date,eth-prices] with dates given in intervals of 1-hour
import pandas as pd
data = pd.DataFrame(cex_x, columns=['date', 'open', 'max', 'min', 'close', 'volume'])
data['date'] = pd.to_datetime(data['date'],unit='ms')

# Divide the data in training and testing set. Because the data has temporal structure, we split the data in two blocks, vs. selecting randomly.
# 90% of the data is used for training and 10 is used for testing
train_rate = 0.9
n = data.shape[0]
ntrain = int(np.floor(n*train_rate))
train_data = data.iloc[0:ntrain,:]
test_data = data.iloc[ntrain:,:]

# Create feature vectors
# - Define how many samples in the past are used to predict future values. 
# - This also defines the number of smaples to be predicted in the future.
max_lag = 12 

# Create feature vectors with 12 columns, each representing a time-lag from the current time point
# - That is: x(t-1), x(t-2)...x(t-12) for close and open values (different features could be grouped using the same logic)
full_train_close = pd.concat([train_data['close'].shift(i) for i in range(0,max_lag)],axis=1).dropna().values
full_train_open = pd.concat([train_data['open'].shift(i) for i in range(0,max_lag)],axis=1).dropna().values
# targets are multivariate, with the values of eth from 1 - 12 hours ahead of the curent time
y_train = full_train_close[max_lag:,:]
# train set is lagged with respect to the targets
x_train = np.concatenate((full_train_close[0:-max_lag,:],full_train_open[0:-max_lag,:]),axis=1)

# Repeat the feature vector creation as above for the test set
full_test_close = pd.concat([test_data['close'].shift(i) for i in range(0,max_lag)],axis=1).dropna().values
full_test_open = pd.concat([test_data['open'].shift(i) for i in range(0,max_lag)],axis=1).dropna().values
y_test = full_test_close[max_lag:,:]
x_test = np.concatenate((full_test_close[0:-max_lag,:],full_test_open[0:-max_lag,:]),axis=1)
```

## 3.  Make predictions

### 3.1 Build a simple AI model

In the same Python console:

```python
# Create models
from sklearn.multioutput import RegressorChain
from tensorflow import keras
from tensorflow.keras import Sequential, Model
from tensorflow.keras.layers import Input, Dense
import numpy as np
import matplotlib.pyplot as plt

# regression using a base estimator and RegressionChain
def fit_and_predict_reg(base_model,x_train,y_train,x_test,y_test):
  chain = RegressorChain(base_estimator=base_model).fit(x_train, y_train)  
  yhat_test = chain.predict(x_test)
  return nmse(y_test,yhat_test)

# Neural network using Keras, 2 hidden layers with RELU activations, output layer with linear activations 
def fit_andpredict_fcnn(x_train,y_train,x_test,y_test):
  inputs = Input(shape=(x_train.shape[1],))
  x = Dense(128,activation='relu')(inputs)
  x = Dense(64,activation='relu')(x)
  outputs = Dense(12,activation='linear')(x)
  model = Model(inputs=inputs,outputs=outputs)
  # set compiling parameters
  model.compile( optimizer="adam", loss='mean_absolute_percentage_error',metrics=[])
  # Fit model
  model.fit(x_train,y_train,batch_size=100, epochs=500, validation_split=0.1, verbose=0)
  # predict
  yhat_test = model.predict(x_test)
  return nmse(y_test,yhat_test)

# multi-output linear regression
from sklearn.linear_model import LinearRegression 
linreg = LinearRegression()
linreg_error = fit_and_predict_reg(linreg,x_train,y_train,x_test,y_test)

# multi-output random forest regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
rfr = RandomForestRegressor(max_depth=10)
rfr_error = fit_and_predict_reg(rfr,x_train,y_train,x_test,y_test)

# multi-output support vector machines
from sklearn.svm import SVR
svr = SVR(kernel='rbf', C=1000, epsilon=.1)
svr_error = fit_and_predict_reg(svr,x_train,y_train,x_test,y_test)

# Dense NN
dnn_error = fit_andpredict_fcnn(x_train,y_train,x_test,y_test)


# Plot results

info = {'LR':linreg_error_2, 'RFR':rfr_error_2, 'SVR':svr_error_2,'NN':dnn_error_2}
methods = list(info.keys())
values = list(info.values())
  
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(methods, values, color ='maroon', width = 0.4)
 
plt.xlabel("Methods")
plt.ylabel("NMSE")
plt.title("Comparison of different methods for predicting ETH value 1-12 hours ahead")
plt.show()
```

### 3.2 Run the AI model to make future ETH price predictions"

#### 3.2.1 Select the best performant model and make final predictions

Looking at the averaged error on the test set, we observe that the Random Forest Regression provides the lowest NMSE.The ranking of the methods will change depending on the hyper parameters selected and in the case of Neural Networks, initialization is critical. With the RFR selected, we proceed to retrain the model using all the available data up to the current time.

In the same Python Console:

```python
full_data_close = pd.concat([data['close'].shift(i) for i in range(0,max_lag)],axis=1).dropna().values
full_data_open = pd.concat([data['open'].shift(i) for i in range(0,max_lag)],axis=1).dropna().values
Y = full_data_close[max_lag:,:]
X = np.concatenate((full_data_close[0:-max_lag,:],full_data_open[0:-max_lag,:]),axis=1)
model = RegressorChain(base_estimator=rfr).fit(X, Y)  
```
Then we create the prediction for the future values 1h, 2h, ... 12h. For this example, the input is the feature vector corresponding to the latest observed data point:

```python
# predict future 12 hours prices using latest 12 values observed
input_data = np.concatenate((full_data_close[-1:,:],full_data_open[-1:,:]),axis=1)
pred_vals = model.predict(input_data)
```

### 3.3 Calculate NMSE

The NMSE was already calculated in section 3.1. The Random Forest had the lowest error.

## 4.  Publish predictions
From [Challenge 3](../challenges/main3.md), do:
- [x] Publish predictions

## 5. Discussion

There are many ways to reduce error further, including: more data, tuning hyperparameters, better feature vectors, better modeling algorithms including time-aware ones (e.g. recurrent neural networks).
