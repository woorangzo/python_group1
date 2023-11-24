# import pandas as pd
#
# stock_data = pd.read_csv('data/NVDA.csv')
#
# # save original 'Open' prices for later
# original_open = stock_data['Open'].values
# # separate dates for future plotting
# dates = pd.to_datetime(stock_data['Date'])
#
# # variables for training
# cols = list(stock_data)[1:6]
# # new dataframe with only training data - 5 columns
# stock_data = stock_data[cols].astype(float)
#
# # normalize the dataset
# class StandardScaler:
#     pass
#
#
# scaler = StandardScaler()
# scaler = scaler.fit(stock_data)
# stock_data_scaled = scaler.transform(stock_data)
#
# # split to train data and test data
# n_train = int(0.9*stock_data_scaled.shape[0])
# train_data_scaled = stock_data_scaled[0: n_train]
# train_dates = dates[0: n_train]
#
# test_data_scaled = stock_data_scaled[n_train:]
# test_dates = dates[n_train:]