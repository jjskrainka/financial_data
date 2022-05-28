import pandas as pd
from sqlalchemy import create_engine


class PgPipeline:

    def __init__(self):
        pass

    def main(self, df: pd.DataFrame(), user: str, password: str, host: str, port: int, db_name: str) -> None:
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
        engine.connect()

        print(pd.io.sql.get_schema(df, name=db_name, con=engine))
        df.head(0).to_sql(name=db_name, con=engine, if_exists='replace')

        #  TODO: chunk insert
        df.to_sql(name=db_name, con=engine, if_exists='append')


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Load dataframe into postgres.')
    parser.add_argument('--user', '-u', type=str, required=True, dest='user',
                        help='Username for pg database.')
    parser.add_argument('--password', '-p', type=str, required=True, dest='password', 
                        help='Password for pg databse.')
    parser.add_argument('--host', '-h', type=str, required=True, dest='host',
                        help='Host name for pg database.')
    parser.add_argument('--port', '-p', type=str, required=True, dest='port',
                        help='Port for pg database.')
    args = parser.parse_args()
    
    PricePipeline().main(args.stock, args.market, args.date)

