"""
===================================================
Script Name:       yfinance_data_handler.py
Author:            Tim Tanner, tim.tanner@gmail.com
Description:       Abstraction class to fetch data from yfinance
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

import yfinance as yf
import pandas as pd
import os

class YahooFinanceData:
    """
    A class to retrieve stock data from Yahoo Finance and provide functionality
    to save the data locally in CSV or Pickle format. This class is designed to
    be extended in the future to support SQL database storage.
    """
    def __init__(self, ticker: str, start: str, end: str):
        """
        Initialize the data abstraction class.
        :param ticker: The stock ticker symbol (e.g., "AAPL").
        :param start: The start date for data retrieval (YYYY-MM-DD).
        :param end: The end date for data retrieval (YYYY-MM-DD).
        """
        self.ticker = ticker
        self.start = start
        self.end = end
        self.data = None

    def fetch_data(self):
        """Retrieve stock data from Yahoo Finance."""
        try:
            self.data = yf.download(self.ticker, start=self.start, end=self.end)
            if self.data.empty:
                print("No data retrieved. Please check the ticker symbol and date range.")
        except Exception as e:
            print(f"Error retrieving data: {e}")

    def save_data(self, file_path: str, file_format: str = "csv"):
        """
        Save the retrieved data to a local file (CSV or Pickle).
        :param file_path: The file path to save the data.
        :param file_format: The format of the file ('csv' or 'pickle').
        """
        if self.data is None or self.data.empty:
            print("No data to save. Fetch data first.")
            return

        try:
            if file_format.lower() == "csv":
                self.data.to_csv(file_path, index=True, header=True)
            elif file_format.lower() == "pickle":
                self.data.to_pickle(file_path)
            else:
                print("Unsupported file format. Use 'csv' or 'pickle'.")
                return
            print(f"Data saved successfully at {file_path}")
        except Exception as e:
            print(f"Error saving data: {e}")

# Example usage
if __name__ == "__main__":
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2024-01-01"

    data_handler = YahooFinanceData(ticker, start_date, end_date)
    data_handler.fetch_data()
    data_handler.save_data("apple_stock_data.csv", "csv")

