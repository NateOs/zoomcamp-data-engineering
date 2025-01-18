import argparse
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from time import time
import requests

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv'

    # download the csv file
    response = requests.get(url)
    with open(csv_name, 'wb') as file:
        file.write(response.content)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Create database if it does not exist
    if not database_exists(engine.url):
        create_database(engine.url)

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, compression='gzip')
    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        try:
            t_start = time()
            df = next(df_iter)
            
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(name=table_name, con=engine, if_exists='append')
            
            t_end = time()
            print('inserted another chunk..., took %.3f second' % (t_end - t_start))
        except StopIteration:
            print("All chunks have been processed.")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)

    # python ingesting_data.py \
    #     --user root \
    #     --password root \
    #     --host localhost \
    #     --port 5432 \
    #     --db postgres \
    #     --table_name yellow_taxi_data \
    #     --url https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2019-01.csv