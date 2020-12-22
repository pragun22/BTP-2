import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import pandas as pd
import math
import statsmodels.api as sm
import statsmodels.tsa.api as smt
import statsmodels.formula.api as smf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt

import itertools
import uuid
# makes rainfall prediction by running ARIMA model
def pred():
	# data read and preprocessing
	filename = 'modified_rainfall2.csv'
	rainfall_data_matrix = pd.read_csv(filename, header = 0,delimiter=',')
	rainfall_data_matrix.set_index("Year", inplace=True)
	rainfall_data_matrix = rainfall_data_matrix.transpose()
	dates = pd.date_range(start='1970-01', freq='MS', periods=len(rainfall_data_matrix.columns)*12)
	rainfall_data_matrix_np = rainfall_data_matrix.transpose().to_numpy()
	shape = rainfall_data_matrix_np.shape
	rainfall_data_matrix_np = rainfall_data_matrix_np.reshape((shape[0] * shape[1], 1))
	rainfall_data = pd.DataFrame({'Precipitation': rainfall_data_matrix_np[:,0]})
	rainfall_data.set_index(dates, inplace=True)
	test_rainfall_data = rainfall_data.loc['1995':'2000']
	rainfall_data = rainfall_data.loc[: '1994']
	
	# best values identified for the model in BTP-1
	best_pdq = (1, 0, 0)
	best_seasonal_pdq = (0, 1, 1, 12)
	best_model = sm.tsa.statespace.SARIMAX(rainfall_data,
	                                      order=best_pdq,
	                                      seasonal_order=best_seasonal_pdq,
	                                      enforce_stationarity=True,
	                                      enforce_invertibility=True)
	best_results = best_model.fit()
	pred_dynamic = best_results.get_prediction(start=pd.to_datetime('1990-01-01'), dynamic=True, full_results=True)
	pred_dynamic_ci = pred_dynamic.conf_int()
	rainfall_predicted = pred_dynamic.predicted_mean
	rainfall_truth = rainfall_data['1990':].Precipitation
	
	# calculate mean squared error
	mse = math.sqrt(((rainfall_predicted - rainfall_truth) ** 2).mean())
	rainfall_data.index[-1]
	rainfall_dummy_data = rainfall_data
	rainfall_dummy_data.columns = ['Train data']
	n_steps = 96
	pred_uc_95 = best_results.get_forecast(steps=n_steps, alpha=0.05) 
	pred_ci_95 = pred_uc_95.conf_int()
	index = pd.date_range(rainfall_data.index[-1], periods=n_steps, freq='MS')
	forecast_data = pd.DataFrame(np.column_stack([pred_uc_95.predicted_mean, pred_ci_95]), 
	                     index=index, columns=['forecast', 'lower_ci_95', 'upper_ci_95'])
	dummy_test_data = test_rainfall_data
	dummy_test_data.columns = ['Test data']
	y_true = test_rainfall_data['1995-01-01':]['Test data']
	y_forecast = forecast_data['forecast']
	XX = ["Jan","Feb", "Mar", "Apr","May","June","July","Aug","Sep","Oct","Nov","Dec"]
	yy = y_forecast[-12:].values.tolist()
	plt.title("Rainfall prediction for 2021")
	plt.xlabel("Month")
	plt.ylabel("Rainfall in mm")
	# creating plot for next year
	plt.plot(XX, yy)
	filename = "static" + "/" + str(uuid.uuid4()) + ".jpg"
	plt.savefig(filename, dpi=100)
	return filename