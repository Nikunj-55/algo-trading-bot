import yfinance as yf
import pandas as pd

def fetch_stock_data(tickers, period="6mo", interval="1d"):
    stock_data = {}
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")

        # Use yf.download() to avoid metadata rows
        df = yf.download(ticker, period=period, interval=interval)
        
        # Reset index so "Date" is a column
        df.reset_index(inplace=True)

        # Save clean CSV (no index, no metadata)
        df.to_csv(f"{ticker}_data.csv", index=False)

        stock_data[ticker] = df
    return stock_data

if __name__ == "__main__":
    nifty_stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
    fetch_stock_data(nifty_stocks)
