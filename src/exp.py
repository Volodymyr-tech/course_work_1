import yfinance as yf
import pandas as pd

# Загрузка данных о стоимости акций S&P 500, например, Apple (AAPL)
stock = yf.Ticker("AAPL")
stock_info = stock.history(period="1d")
stock_info.index = stock_info.index.tz_localize(None)
stock_info.to_excel(r'C:\Users\Владимир\PycharmProjects/stock_data.xlsx', index=True)

