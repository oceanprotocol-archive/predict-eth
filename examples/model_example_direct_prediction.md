
### 1. Testing different models for direct price prediction from 1- 12 Hours

Given the task of predicting ETH for 12 hours in the future, there are several approaches that are possible. These appraoches involve either learning an independent model to predict the prices at ech hour or to learn a model that makes direct predictions.

This readme describe the implementation of four different algorithms to predict the price of ether uisng the previous values of it as features. The models use 12 previous hours prices to predict the 12 hours future values. The implemented models are Linear Regression, Random Forest regression, Support vector machines and a two layer desily connected neuran nework.

## 1. Setup

From [Challenge 2](../challenges/main2.md), do:
- [x] Setup

In the console:
```console
pip install pandas numpy requests
```

## 2. Get data locally

In Python:

```python

import pandas as pd
import numpy as np
import requests

# get ETH/USD prices for the latest 500 hours.
# the datasurce returns timestamp, open, max, min, close and volume
resp = requests.get(
    "https://cexa.oceanprotocol.io/ohlc?exchange=binance&pair=ETH/USDT")


# create a dataframe with the received data
data = pd.DataFrame(resp.json(), columns=['date', 'open', 'max', 'min', 'close', 'volume'])
print(data.shape)
data['date'] = pd.to_datetime(data['date'],unit='ms')

# Divide the data in training and tetsing set. Because the data has temporal structure, for the sake of this example we split the data # in two blocks rather than selecting sample points randomly to be part of the training and testing sets.
# 90% of the data is used for training and 10 is used for testing
train_rate = 0.9
n = data.shape[0]
ntrain = int(np.floor(n*train_rate))
train_data = data.iloc[0:ntrain,:]
test_data = data.iloc[ntrain:,:]


# create feature vectors
# define how many smaples in the past are used to predict future values. 
# it also define the number of smaples to be predicted in the future
max_lag = 12 

# Create feature vectors with 12 columns, each representing a time-lag from the current time point
# that is x(t-1), x(t-2)...x(t-12) for close and open values (different features could be grouped using the same logic)
full_train_close = pd.concat([train_data['close'].shift(i) for i in range(0,max_lag)],axis=1).dropna().values
full_train_volume = pd.concat([train_data['open'].shift(i) for i in range(0,max_lag)],axis=1).dropna().values
# targets are multivariate, with the values of eth from 1 - 12 hours ahead of the curent time
y_train = full_train_close[max_lag:,:]
# train set is lagged with respect to the targets
x_train = np.concatenate((full_train_close[0:-max_lag,:],full_train_volume[0:-max_lag,:]),axis=1)


# Repeat the feature vector creation as above for the test set
full_test_close = pd.concat([test_data['close'].shift(i) for i in range(0,max_lag)],axis=1).dropna().values
full_test_volume = pd.concat([test_data['open'].shift(i) for i in range(0,max_lag)],axis=1).dropna().values
y_test = full_test_close[max_lag:,:]
x_test = np.concatenate((full_test_close[0:-max_lag,:],full_test_volume[0:-max_lag,:]),axis=1)

```

## 3.  Make predictions



### 3.1  rain model and calculate prediction error in the test set

In the same Python console:

```python
# Create models
from sklearn.multioutput import RegressorChain
from tensorflow import keras
from tensorflow.keras import Sequential, Model
from tensorflow.keras.layers import Input, Dense
import numpy as np
import matplotlib.pyplot as plt

# normalized mean-squared-error, consistent with elsewhere in predict-eth
def nmse(y, yhat) -> float:
    range_y = max(y) - min(y)    
    return np.sqrt(np.average(((yhat - y) / range_y) ** 2))


# regression using a base estimator and RegressionChain
def fit_and_predict_reg(base_model,x_train,y_train,x_test,y_test):
  chain = RegressorChain(base_estimator=base_model).fit(x_train, y_train)  
  yhat_test = chain.predict(x_test)
  return nmse(y_test,yhat_test)

# Neural network using Keras, 2 hidden layers with relu activations, output layer with linear activations 
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


# multioutput linear regression
from sklearn.linear_model import LogisticRegression, LinearRegression
linreg = LinearRegression()
linreg_error = fit_and_predict_reg(linreg,x_train,y_train,x_test,y_test)

# multiputput random forest regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
rfr = RandomForestRegressor(max_depth=10)
rfr_error = fit_and_predict_reg(rfr,x_train,y_train,x_test,y_test)

# multiputput suport vector machines
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

### 3.2 Select the best performant model and make final predictions

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

## 4.  Publish predictions
From [Challenge 2](../challenges/main2.md), do:
- [x] Publish predictions

## 5. Discussion

The algorithms presented are just shown as introductory approaches but are not production ready. For instance, we use the close value as the real eth value and an extra feature including the open price is added, however many other (more informative) variables could be incorporated. Some of the methods proposed need tuning of hyper parameters, such as the regularization parameter C in the SVR, number of estimators in the Random forest method, etc.

Furthermore, these methods base their prediction in the previous 12 hours and do not take into consideration trends nor other possible variables such as holidays, seasons etc. all this motivates using models that model time and allow for latten variable modeling such as Hidden Markov Models or Recurrent Neural networks (including LSTMS)