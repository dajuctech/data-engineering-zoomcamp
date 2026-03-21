# Module 7: Streaming — Homework Answers (2026)

Course: Data Engineering Zoomcamp 2026
Topic: Stream Processing with Redpanda (Kafka) + PyFlink

---

## Setup

```bash
cd 07-streaming/workshop/
docker compose build
docker compose up -d
```

Services started:
- Redpanda (Kafka-compatible broker) → `localhost:9092`
- Flink Job Manager UI → `http://localhost:8081`
- Flink Task Manager
- PostgreSQL → `localhost:5432` (user: postgres / password: postgres)

---

## Question 1 — Redpanda Version

**Command:**
```bash
docker exec -it workshop-redpanda-1 rpk version
```

**Answer: `v25.3.9`**

The `docker-compose.yml` uses image `redpandadata/redpanda:v25.3.9`.

---

## Question 2 — Sending Data to Redpanda

**Setup:**
```bash
docker exec -it workshop-redpanda-1 rpk topic create green-trips
```

**Producer code (`src/producers/producer_green.py`):**
```python
import pandas as pd
import json
from kafka import KafkaProducer
from time import time

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=json_serializer
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
    'total_amount'
]
df = df[columns]

# Convert datetime columns to strings
df['lpep_pickup_datetime'] = df['lpep_pickup_datetime'].astype(str)
df['lpep_dropoff_datetime'] = df['lpep_dropoff_datetime'].astype(str)

t0 = time()

for _, row in df.iterrows():
    producer.send('green-trips', value=row.to_dict())

producer.flush()

t1 = time()
print(f'took {(t1 - t0):.2f} seconds')
```

**Answer: `10 seconds`**

---

## Question 3 — Consumer: Trip Distance > 5.0

**Consumer code (`src/consumers/consumer_green.py`):**
```python
import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'green-trips',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

count = 0
total = 0

for message in consumer:
    trip = message.value
    total += 1
    if trip['trip_distance'] > 5.0:
        count += 1
    # Stop after reading all messages (no new ones)
    if consumer.assignment() and all(
        consumer.position(tp) >= consumer.end_offsets([tp])[tp]
        for tp in consumer.assignment()
    ):
        break

print(f'Total trips: {total}')
print(f'Trips with distance > 5.0: {count}')
```

**Answer: `9506`**

---

## Part 2: PyFlink (Questions 4–6)

### Important Notes
- All job files go in `workshop/src/job/` → mounted at `/opt/src/job/` in the container
- Submit jobs: `docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/<file>.py`
- Use `env.set_parallelism(1)` — green-trips has only 1 partition
- Create PostgreSQL tables before running jobs
- Let each job run 1–2 minutes, then query results, then cancel from `http://localhost:8081`
- If duplicate data: `docker exec -it workshop-redpanda-1 rpk topic delete green-trips` then recreate

### Timestamp DDL pattern for all Flink jobs:
```sql
lpep_pickup_datetime VARCHAR,
event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
```

---

## Question 4 — Tumbling Window: Pickup Location (5-minute)

**Create PostgreSQL table:**
```sql
CREATE TABLE IF NOT EXISTS pickup_location_5min (
    window_start TIMESTAMP,
    PULocationID INTEGER,
    num_trips BIGINT
);
```

**Flink job (`src/job/q4_tumbling_pickup.py`):**
```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    env.enable_checkpointing(10000)
    t_env = StreamTableEnvironment.create(env)

    t_env.execute_sql("""
        CREATE TABLE green_trips_source (
            lpep_pickup_datetime VARCHAR,
            lpep_dropoff_datetime VARCHAR,
            PULocationID INTEGER,
            DOLocationID INTEGER,
            passenger_count DOUBLE,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            total_amount DOUBLE,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-trips',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'properties.group.id' = 'flink-q4',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
    """)

    t_env.execute_sql("""
        CREATE TABLE pickup_location_5min (
            window_start TIMESTAMP(3),
            PULocationID INTEGER,
            num_trips BIGINT
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'pickup_location_5min',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        )
    """)

    t_env.execute_sql("""
        INSERT INTO pickup_location_5min
        SELECT
            TUMBLE_START(event_timestamp, INTERVAL '5' MINUTE) AS window_start,
            PULocationID,
            COUNT(*) AS num_trips
        FROM green_trips_source
        GROUP BY
            TUMBLE(event_timestamp, INTERVAL '5' MINUTE),
            PULocationID
    """).wait()

if __name__ == '__main__':
    main()
```

**Submit:**
```bash
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q4_tumbling_pickup.py
```

**Query results:**
```sql
SELECT PULocationID, num_trips
FROM pickup_location_5min
ORDER BY num_trips DESC
LIMIT 3;
```

**Answer: `74`**

---

## Question 5 — Session Window: Longest Streak (5-minute gap)

**Create PostgreSQL table:**
```sql
CREATE TABLE IF NOT EXISTS session_streaks (
    PULocationID INTEGER,
    session_start TIMESTAMP,
    session_end TIMESTAMP,
    num_trips BIGINT
);
```

**Flink job (`src/job/q5_session_streak.py`):**
```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    env.enable_checkpointing(10000)
    t_env = StreamTableEnvironment.create(env)

    t_env.execute_sql("""
        CREATE TABLE green_trips_source (
            lpep_pickup_datetime VARCHAR,
            lpep_dropoff_datetime VARCHAR,
            PULocationID INTEGER,
            DOLocationID INTEGER,
            passenger_count DOUBLE,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            total_amount DOUBLE,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-trips',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'properties.group.id' = 'flink-q5',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
    """)

    t_env.execute_sql("""
        CREATE TABLE session_streaks (
            PULocationID INTEGER,
            session_start TIMESTAMP(3),
            session_end TIMESTAMP(3),
            num_trips BIGINT
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'session_streaks',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        )
    """)

    t_env.execute_sql("""
        INSERT INTO session_streaks
        SELECT
            PULocationID,
            SESSION_START(event_timestamp, INTERVAL '5' MINUTE) AS session_start,
            SESSION_END(event_timestamp, INTERVAL '5' MINUTE)   AS session_end,
            COUNT(*) AS num_trips
        FROM green_trips_source
        GROUP BY
            SESSION(event_timestamp, INTERVAL '5' MINUTE),
            PULocationID
    """).wait()

if __name__ == '__main__':
    main()
```

**Submit:**
```bash
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q5_session_streak.py
```

**Query results:**
```sql
SELECT PULocationID, num_trips
FROM session_streaks
ORDER BY num_trips DESC
LIMIT 3;
```

**Answer: `51`**

---

## Question 6 — Tumbling Window: Largest Tip per Hour

**Create PostgreSQL table:**
```sql
CREATE TABLE IF NOT EXISTS hourly_tips (
    window_start TIMESTAMP,
    total_tip DOUBLE PRECISION
);
```

**Flink job (`src/job/q6_hourly_tips.py`):**
```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    env.enable_checkpointing(10000)
    t_env = StreamTableEnvironment.create(env)

    t_env.execute_sql("""
        CREATE TABLE green_trips_source (
            lpep_pickup_datetime VARCHAR,
            lpep_dropoff_datetime VARCHAR,
            PULocationID INTEGER,
            DOLocationID INTEGER,
            passenger_count DOUBLE,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            total_amount DOUBLE,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-trips',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'properties.group.id' = 'flink-q6',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
    """)

    t_env.execute_sql("""
        CREATE TABLE hourly_tips (
            window_start TIMESTAMP(3),
            total_tip DOUBLE
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'hourly_tips',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        )
    """)

    t_env.execute_sql("""
        INSERT INTO hourly_tips
        SELECT
            TUMBLE_START(event_timestamp, INTERVAL '1' HOUR) AS window_start,
            SUM(tip_amount) AS total_tip
        FROM green_trips_source
        GROUP BY TUMBLE(event_timestamp, INTERVAL '1' HOUR)
    """).wait()

if __name__ == '__main__':
    main()
```

**Submit:**
```bash
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q6_hourly_tips.py
```

**Query results:**
```sql
SELECT window_start, total_tip
FROM hourly_tips
ORDER BY total_tip DESC
LIMIT 3;
```

**Answer: `2025-10-01 18:00:00`**

---

## Summary of All Answers

| Question | Description | Answer |
|----------|-------------|--------|
| Q1 | Redpanda version | `v25.3.9` |
| Q2 | Time to send all data | `10 seconds` |
| Q3 | Trips with distance > 5.0 | `9506` |
| Q4 | PULocationID with most trips (5-min window) | `74` |
| Q5 | Trips in longest session | `51` |
| Q6 | Hour with highest total tip | `2025-10-01 18:00:00` |
