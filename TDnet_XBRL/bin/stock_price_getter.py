import yfinance as yf
import pandas as pd


class StockPriceGettr():
    def __init__(self, startday, ticker):
        self.startday = startday
        self.ticker = ticker

    def get_stock_price(self):
        data = yf.download(self.ticker, start=self.startday)
        #data.to_csv("toyota_stock_data.csv")
        return data['Adj Close'], data.index


if __name__ == '__main__':
    startday = "2019-01-01"
    ticker = "2780.T"
    stockpricegetter = StockPriceGettr(startday, ticker)
    stock_price, date = stockpricegetter.get_stock_price()

    print(type(stock_price))
    print(date)
