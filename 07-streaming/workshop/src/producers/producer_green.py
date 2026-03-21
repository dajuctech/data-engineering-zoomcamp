"""
Q2: Producer — sends green taxi trip data to the 'green-trips' Redpanda topic.

Setup:
    docker exec -it workshop-redpanda-1 rpk topic create green-trips

Run:
    python src/producers/producer_green.py

Dataset: green_tripdata_2025-10.parquet (place in workshop/ folder)
"""

import json
import pandas as pd
from kafka import KafkaProducer
from time import time


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


def main():
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=json_serializer,
    )

    df = pd.read_parquet('green_tripdata_2025-10.parquet')

    columns = [
        'lpep_pickup_datetime',
        'lpep_dropoff_datetime',
        'PULocationID',
        'DOLocationID',
        'passenger_count',
        'trip_distance',
        'tip_amount',
        'total_amount',
    ]
    df = df[columns]

    # Convert datetime columns to strings for JSON serialisation
    df['lpep_pickup_datetime'] = df['lpep_pickup_datetime'].astype(str)
    df['lpep_dropoff_datetime'] = df['lpep_dropoff_datetime'].astype(str)

    print(f"Sending {len(df)} rows to 'green-trips' topic...")

    t0 = time()

    for _, row in df.iterrows():
        producer.send('green-trips', value=row.to_dict())

    producer.flush()

    t1 = time()
    print(f'took {(t1 - t0):.2f} seconds')


if __name__ == '__main__':
    main()
