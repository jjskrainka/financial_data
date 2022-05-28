from setup_logger import logger
from pg_pipeline import PgPipeline
from yf_scrape import YfScrape

import pandas as pd


class PricePipeline:

    def __init__(self, user: str, password: str, host: str, port: int):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def main(self, stock: str, market: str, date: str):

        share_price_df = YfScrape().main(stock, market, date)

        db = PgPipeline().main(share_price_df, self.user, self.password, self.host, self.port, "price_facts")

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


    parser.add_argument('--user', type=str, required=True, dest='user',
                        help='Username for pg database.')
    parser.add_argument('--password', type=str, required=True, dest='password', 
                        help='Password for pg databse.')
    parser.add_argument('--host', type=str, required=True, dest='host',
                        help='Host name for pg database.')
    parser.add_argument('--port', type=int, required=True, dest='port',
                        help='Port number for pg_database.'),

    args = parser.parse_args()
    
    PricePipeline(args.user, args.password, args.host, args.port).main(args.stock, args.market, args.date)

