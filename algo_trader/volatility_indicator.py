"""
===================================================
Script Name:       volatility_indicator.py
Author:            Tim Tanner, tim.tanner@gmail.com
Description:       Brief Description
Version:           1.0.0
Release History:
    07mar2025: 1.0.0 - Initial release

Created on:        07mar2025
===================================================
"""

__author__ = "Tim Tanner, tim.tanner@gmail.com"
__version__ = "1.0.0"
__date__ = "07mar2025"
__license__ = "MIT"

# Your code starts here...
## source medium: Implementing 5 Volatility Indicators to Improve Market Timing
import yfinance as yf

ticker = "Abc"
start = "2022-01-01"
end = "2025-01-01"

# Get data from yfinance
def get_stock_data(ticker, start_date, end_date):

	stock_data = yf.download(ticker, start=start_date, end=end_date)
	stock_data.columns = ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
	stock_data.ffill(inplace=True)
	return stock_data

# Add a moving average filter
def moving_average_filter(data, window=50):
    data['MA'] = data['Close'].rolling(window=window).mean()
    return data

def rsi(data, rsi_window=14):
	data['RSI'] = 100 - (100 / (1 + data['Close'].diff(1).clip(lower=0).rolling(window=rsi_window).mean() /
                            -data['Close'].diff(1).clip(upper=0).rolling(window=rsi_window).mean()))

    return data

def macd(data, macd_short=12, macd_long=26, macd_signal=9):
    data['MACD'] = data['Close'].ewm(span=macd_short, adjust=False).mean() - data['Close'].ewm(span=macd_long, adjust=False).mean()
    data['MACD_Signal'] = data['MACD'].ewm(span=macd_signal, adjust=False).mean()

    return data

# Define the Chaikin Volatility function
def chaikin_volatility(data, period=10):
    data['HL'] = data['High'] - data['Low']
    data['CHV'] = data['HL'].ewm(span=period, adjust=False).mean()
    data['ChaikinVolatility'] = data['CHV'].pct_change(periods=period) * 100
    return data

# Define the Donchian Channels function
def donchian_channels(data, period=20):
    data['Upper'] = data['High'].rolling(window=period).max()
    data['Lower'] = data['Low'].rolling(window=period).min()
    data['Middle'] = (data['Upper'] + data['Lower']) / 2
    return data

# Define the Keltner Channels function
def keltner_channels(data, period=20, atr_multiplier=2):
    data['TR'] = data[['High', 'Low', 'Close']].apply(
        lambda x: max(
            x['High'] - x['Low'],
            abs(x['High'] - x['Close']),
            abs(x['Low'] - x['Close'])
        ), axis=1
    )
    data['ATR'] = data['TR'].rolling(window=period).mean()
    data['Middle'] = data['Close'].rolling(window=period).mean()
    data['Upper'] = data['Middle'] + atr_multiplier * data['ATR']
    data['Lower'] = data['Middle'] - atr_multiplier * data['ATR']
    return data

# Define the Relative Volatility Index (RVI) function
def relative_volatility_index(data, period=14):
    # Calculate the difference between the Close and Open prices
    data['Upward Volatility'] = np.where(data['Close'] > data['Open'], data['Close'] - data['Open'], 0)
    data['Total Volatility'] = abs(data['Close'] - data['Open'])

    # Calculate the rolling sum of Upward Volatility and Total Volatility
    data['Upward Volatility Sum'] = data['Upward Volatility'].rolling(window=period).sum()
    data['Total Volatility Sum'] = data['Total Volatility'].rolling(window=period).sum()

    # Calculate RVI as the ratio of Upward Volatility to Total Volatility
    data['RVI'] = data['Upward Volatility Sum'] / data['Total Volatility Sum'] * 100

    return data

# Define the standard deviation function
def standard_deviation(data, period=20):
    data['Std_Dev'] = data['Close'].rolling(window=period).std()
    return data

# Calculate Bollinger Bands
def bollinger_bands(data, window=20, no_of_std=2):

    rolling_mean = data['Close'].rolling(window).mean()
    rolling_std = data['Close'].rolling(window).std()


    data['Bollinger_High'] = rolling_mean + (rolling_std * no_of_std)
    data['Bollinger_Low'] = rolling_mean - (rolling_std * no_of_std)
    return data

