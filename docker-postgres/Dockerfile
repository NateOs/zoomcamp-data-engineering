FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2 requests sqlalchemy_utils

WORKDIR /app
COPY . /app

CMD ["python", "ingesting_data.py"]

  # python ingesting_data.py \
    #     --user root \
    #     --password root \
    #     --host localhost \
    #     --port 5432 \
    #     --db postgres \
    #     --table_name yellow_taxi_data \
    #     --url https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2019-01.csv

	# docker run -it --name ingesting_data_container ingesting_data_image \
    # --user root \
    # --password root \
    # --host localhost \
    # --port 5432 \
    # --db ny_taxi \
    # --table_name yellow_taxi_data \
    # --url https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2019-01.csv