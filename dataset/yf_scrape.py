import yfinance as yf
from datetime import datetime
import pandas as pd

from setup_logger import logger


class YfScrape:
    """
    Given a date, stock, and market which the stock trades in, the format of the inputs is validated, yahoo finance api is called and put into a dataframe
    """
    
    def __init__(self):
        pass

    def main(self, stock: str, market: str, date: str) -> pd.DataFrame():
        
        self.validate(date)

        share_price_df = self.get_yf_share_price(stock, market, date)

        logger.debug(f"get_yf_share_price dataframe\n{share_price_df.head(5)}")
        return share_price_df

    def get_yf_share_price(self, stock, market, date) -> pd.DataFrame():
        symbols = [stock, market]

        # Create a dataframe of historical stock prices
        # The date entered represents the first historical date prices will be returned
        # Highly encouraged to leave 'Adj Close' as is
        data = yf.download(symbols, date)['Adj Close']
        data = data.rename(columns={stock: "stockprice", market: "marketprice"})
        return data

    @staticmethod
    def validate(date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            logger.debug(f"date input: {date_text}")
            raise ValueError("Incorrect data format, should be YYYY-MM-DD.")       

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Ingest beta for a single stock into db.')
    parser.add_argument('--stock', '-s', type=str, required=True, dest='stock',
                        help='Ticker symbol for stock to get beta for.')
    # TODO: --market arg required=False, if not specified we should be able to determine the market the stock trades on.
    parser.add_argument('--market', '-m', type=str, required=True, dest='market', 
                        help='Market to reference stock beta.')
    parser.add_argument('--date', '-d', type=str, required=True, dest='date',
                        help='Date period to calculate beta over. YYYY-MM-DD')
    args = parser.parse_args()
    
    YfScrape().main(args.date, args.stock, args.market)

