import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

class Stock:
    def __init__(self, ticker, start_date: str = str(date.today() - timedelta(days=90)), end_date: str = str(date.today())):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.df = None

    def get_info(self):
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            info = {
                "name": info.get('longName', 'N/A'),
                "description": info.get("longBusinessSummary", 'N/A'),
                "city": info.get("city", 'N/A'),
                "state": info.get("state", 'N/A'),
                "country": info.get("country", 'N/A'),
                "logo_url": info.get("logo_url", 'N/A')
            }
            return info
        except Exception as e:
            print(f"Error retrieving stock info: {e}")
            raise

    def get_graphs(self):
        if self.get_data():
            open_close_graph = self.open_close_graph()
            moving_avg_graph = self.moving_average_graph()
            return open_close_graph, moving_avg_graph
        else:
            raise ConnectionError("Failed to retrieve data.")

    def get_data(self):
        try:
            df = yf.download(
                tickers=self.ticker,
                start=self.start_date,
                end=self.end_date
            )
            df.reset_index(inplace=True)
            self.df = df
            return True
        except Exception as e:
            print(f"Error retrieving stock data: {e}")
            return False

    def open_close_graph(self):
        if self.df is not None:
            fig = px.line(
                self.df,
                x="Date",
                y=["Close", "Open"],
                title="Open and Close Price",
                height=500, width=800
            )
            return fig
        else:
            raise ValueError("Data not available.")

    def moving_average_graph(self):
        if self.df is not None:
            self.df['EWA_20'] = self.df['Close'].ewm(span=20, adjust=False).mean()
            fig = px.line(
                self.df,
                x='Date',
                y=['EWA_20'],
                title="Moving Averages",
                height=500, width=800
            )
            return fig
        else:
            raise ValueError("Data not available.")
