"""
Q3: Consumer — reads all messages from 'green-trips' and counts trips
    where trip_distance > 5.0 km.

Run:
    python src/consumers/consumer_green.py
"""

import json
from kafka import KafkaConsumer
from kafka import TopicPartition


def main():
    consumer = KafkaConsumer(
        'green-trips',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        consumer_timeout_ms=10000,  # stop after 10s of no new messages
    )

    count_over_5 = 0
    total = 0

    for message in consumer:
        trip = message.value
        total += 1
        if trip.get('trip_distance', 0) > 5.0:
            count_over_5 += 1

    consumer.close()

    print(f'Total trips read     : {total}')
    print(f'Trips with distance > 5.0 km: {count_over_5}')


if __name__ == '__main__':
    main()
