FROM python:3.9.1

RUN pip install pandas sqlalchemy psycopg2 yfinance

WORKDIR /app
COPY dataset/ ./dataset/

RUN ls | grep "dataset"

ENTRYPOINT [ "python", "dataset/price_pipeline.py" ]

