import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import datetime
from pg_pipeline import PgPipeline
from typing import Any, Union

from setup_logger import logger
from yf_scrape import YfScrape


class LinRegBeta:

    def __init__(self):
        pass

    def main(self, stock: str, market: str, date: str):
        
        share_price_df = YfScrape().main(stock, market, date)

        price_pct_df = self.get_beta_from_pct(share_price_df)
        
        self.logger.debug(f"get_beta_from_pct dataframe\n{price_pct_df.head(5)}")

        share_price_df = share_price_df.join(price_pct_df, on="Date")

    def get_beta_from_pct(self, df) -> pd.DataFrame():
        # Convert historical stock prices to daily percent change
        pct_df = df.pct_change()

        # Deletes row one containing the NaN
        # NaN will cause error in linreg
        prepd_df = pct_df.drop(pct_df.index[0])

        beta = self.set_beta(prepd_df)[0]
        pct_df = self.add_col(pct_df, {"beta": beta})
        pct_df = pct_df.rename(columns={"stockprice": "stockpct", "marketprice": "marketpct"})

        return pct_df

    def set_beta(self, df: pd.DataFrame()) -> float:
        # Create arrays for x and y variables in the regression model
        x = np.array(df["stockprice"]).reshape((-1,1))
        y = np.array(df["marketprice"])

        # Define the model and type of regression
        model = LinearRegression().fit(x, y)
        beta = model.coef_

        # logs the beta to log file 
        logging.info(f'Beta for {self.stock} from {self.date}: {beta}')

        return beta
