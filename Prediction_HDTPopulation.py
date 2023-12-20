# Import of python related libraries ********************************************
import warnings
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA

# Plot parameterization and data import ******************************************
## Plot defaults 
plt.rcParams['font.sans-serif']=['SimHei'] 
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['figure.figsize'] = (25.0, 10.0)
plt.rcParams.update({'font.size': 12})
plt.style.use('ggplot')

## Load the data 
data = pd.read_csv('data.csv')    #Change to the path of the time series data you need to forecast
data['Year']=pd.to_datetime(data['Year'], format='%Y')
data.set_index(['Year'], inplace=True)

## Plot the data
data.plot()
plt.ylabel('Y')
plt.xlabel('Year')
plt.show()

# main ---- Prediction of HDT population ******************************************
## ACF and PACF Plotting
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(data,lags=5,ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(data,lags=5,ax=ax2)
plt.show()

## Define the q, d and q parameters to take any value between 0 and 4
q = range(0, 5)
d = range(0, 5)
p = range(0, 5)

## Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

print('Examples of parameter combinations for Seasonal ARIMA...')
print('ARIMA: {}'.format(pdq[1]))
print('ARIMA: {}'.format(pdq[2]))
print('ARIMA: {}'.format(pdq[3]))
print('ARIMA: {}'.format(pdq[4]))

warnings.filterwarnings("ignore") # specify to ignore warning messages

## Model evaluation metrics ---- AIC and BIC
AIC = []
ARIMA_model = []
for param in pdq:
    try:
        mod = ARIMA(data, order=param)
        results = mod.fit()
        AIC.append(results.aic)
        ARIMA_model.append(param)
    except:
        continue
print('The smallest AIC is {} for model ARIMA{}'.format(min(AIC), ARIMA_model[AIC.index(min(AIC))]))

BIC = []
ARIMA_model = []
for param in pdq:
    try:
        mod = ARIMA(data, order=param)
        results = mod.fit()
        BIC.append(results.bic)
        ARIMA_model.append(param)
    except:
        continue
ARIMA_model[BIC.index(min(BIC))]
print('The smallest BIC is {} for model ARIMA{}'.format(min(BIC), ARIMA_model[BIC.index(min(BIC))]))

# Selection of the optimal parameters of the model taking into account ACF, PACF and evaluation metrics
mod = ARIMA(data,order=(1,1,1))
ARIMA_model = mod.fit()
pred = ARIMA_model.get_forecast('2035')
pred_ci = pred.conf_int()
pred.predicted_mean['2021':'2035'].to_csv('data_precict.csv')
