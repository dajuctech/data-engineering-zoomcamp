"""
Q4: PyFlink job — 5-minute tumbling window, count trips per PULocationID.

Create the PostgreSQL table first:
    CREATE TABLE IF NOT EXISTS pickup_location_5min (
        window_start TIMESTAMP,
        "PULocationID" INTEGER,
        num_trips BIGINT
    );

Submit:
    docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q4_tumbling_pickup.py

Query results:
    SELECT "PULocationID", num_trips
    FROM pickup_location_5min
    ORDER BY num_trips DESC
    LIMIT 3;

Answer: PULocationID 74
"""

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)  # green-trips has only 1 partition
    env.enable_checkpointing(10000)

    t_env = StreamTableEnvironment.create(env)

    # Source: Kafka / Redpanda
    t_env.execute_sql("""
        CREATE TABLE green_trips_source (
            lpep_pickup_datetime  VARCHAR,
            lpep_dropoff_datetime VARCHAR,
            PULocationID          INTEGER,
            DOLocationID          INTEGER,
            passenger_count       DOUBLE,
            trip_distance         DOUBLE,
            tip_amount            DOUBLE,
            total_amount          DOUBLE,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector'                     = 'kafka',
            'topic'                         = 'green-trips',
            'properties.bootstrap.servers'  = 'redpanda:29092',
            'properties.group.id'           = 'flink-q4',
            'scan.startup.mode'             = 'earliest-offset',
            'format'                        = 'json'
        )
    """)

    # Sink: PostgreSQL
    t_env.execute_sql("""
        CREATE TABLE pickup_location_5min (
            window_start  TIMESTAMP(3),
            PULocationID  INTEGER,
            num_trips     BIGINT
        ) WITH (
            'connector'  = 'jdbc',
            'url'        = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'pickup_location_5min',
            'username'   = 'postgres',
            'password'   = 'postgres',
            'driver'     = 'org.postgresql.Driver'
        )
    """)

    # 5-minute tumbling window aggregation
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
