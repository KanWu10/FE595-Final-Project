# Import Dependencies
import numpy as np
import pandas as pd
import math
import datetime as dt
import pandas_datareader.data as web
from sklearn import preprocessing, svm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate, train_test_split

# Get the stock data
start = dt.datetime(2015, 1, 2)
end = dt.datetime(2017, 12, 31)
tickers = ['AMZN', 'CSCO', 'MSFT', 'AAPL', 'NVDA', 'QCOM']
stock_data = list()
for ticker in tickers:
    df = web.DataReader(ticker, "yahoo", start, end)
    stock_data.append(df)

# Read the sentiment file obtained from last step
sentiment_file = pd.read_excel('Sentiment.xlsx')
# Choose the "Adjusted Price" as the variable to be predicted
forecast_col = 'Adj Close'
# Combine the sentiment score to the current data
stock_data[0]['Sentiment'] = sentiment_file['Sentiment Score']
for i in range(1,6):
    stock_data[i]['Sentiment'] = sentiment_file['Sentiment Score.'+str(i)]

# Create two lists to store model fit sets
stock_Xpred = list()
stock_X = list()
stock_y = list()
# Add columns of price change percentage
for df in stock_data:
    df['HL_PCT'] = (df['High'] - df['Low']) / df['Adj Close'] * 100
    df['PCT_change'] = (df['Close'] - df['Open']) / df['Adj Close'] * 100
    df.drop(columns = ['High', 'Low', 'Open', 'Close'], inplace=True)
    # Fill NA values
    df.fillna(value=-99999, inplace=True)
    # We will predict the 1% length of one year
    forecast_num = int(math.ceil(0.01 * len(df)))
    # Create a new column
    df['label'] = df[forecast_col].shift(-forecast_num)
    X = np.array(df.drop(['label'], 1))
    # Scale the variables
    X = preprocessing.scale(X)
    X_pred = X[-forecast_num:]
    X = X[:-forecast_num]
    df.dropna(inplace = True)
    y = np.array(df['label'])
    stock_X.append(X)
    stock_y.append(y)
    stock_Xpred.append(X_pred)
# Split the sets into training set and test set

# AMZN
X0_train, X0_test, y0_train, y0_test = train_test_split(stock_X[0], stock_y[0], test_size = 0.2)
# CSCO
X1_train, X1_test, y1_train, y1_test = train_test_split(stock_X[1], stock_y[2], test_size = 0.2)
# MSFT
X2_train, X2_test, y2_train, y2_test = train_test_split(stock_X[2], stock_y[2], test_size = 0.2)
# AAPL
X3_train, X3_test, y3_train, y3_test = train_test_split(stock_X[3], stock_y[3], test_size = 0.2)
# NVDA
X4_train, X4_test, y4_train, y4_test = train_test_split(stock_X[4], stock_y[4], test_size = 0.2)
# QCQM
X5_train, X5_test, y5_train, y5_test = train_test_split(stock_X[5], stock_y[5], test_size = 0.2)

# Linear Regression
lr = LinearRegression(n_jobs=-1)
lr.fit(X0_train, y0_train)
lr.fit(X1_train, y1_train)
lr.fit(X2_train, y2_train)
lr.fit(X3_train, y3_train)
lr.fit(X4_train, y4_train)
lr.fit(X5_train, y5_train)
confidence1 = pd.DataFrame([(lr.score(X0_test, y0_test), lr.score(X1_test, y1_test), lr.score(X2_test, y2_test),
                            lr.score(X3_test, y3_test), lr.score(X4_test, y4_test), lr.score(X5_test, y5_test))],
                     columns=tickers)
print(confidence1)

# Support Vector Regression
svrfit = svm.SVR(kernel='linear')
svrfit.fit(X0_train, y0_train)
svrfit.fit(X1_train, y1_train)
svrfit.fit(X2_train, y2_train)
svrfit.fit(X3_train, y3_train)
svrfit.fit(X4_train, y4_train)
svrfit.fit(X5_train, y5_train)
confidence2 = pd.DataFrame([(svrfit.score(X0_test, y0_test), svrfit.score(X1_test, y1_test), svrfit.score(X2_test, y2_test),
                            svrfit.score(X3_test, y3_test), svrfit.score(X4_test, y4_test), svrfit.score(X5_test, y5_test))],
                     columns=tickers)
print(confidence2)