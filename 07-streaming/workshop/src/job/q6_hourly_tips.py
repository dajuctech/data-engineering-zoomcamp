"""
Q6: PyFlink job — 1-hour tumbling window, total tip_amount per hour
    across all locations.

Create the PostgreSQL table first:
    CREATE TABLE IF NOT EXISTS hourly_tips (
        window_start TIMESTAMP,
        total_tip    DOUBLE PRECISION
    );

Submit:
    docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q6_hourly_tips.py

Query results:
    SELECT window_start, total_tip
    FROM hourly_tips
    ORDER BY total_tip DESC
    LIMIT 3;

Answer: 2025-10-01 18:00:00
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
            'properties.group.id'           = 'flink-q6',
            'scan.startup.mode'             = 'earliest-offset',
            'format'                        = 'json'
        )
    """)

    # Sink: PostgreSQL
    t_env.execute_sql("""
        CREATE TABLE hourly_tips (
            window_start TIMESTAMP(3),
            total_tip    DOUBLE
        ) WITH (
            'connector'  = 'jdbc',
            'url'        = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'hourly_tips',
            'username'   = 'postgres',
            'password'   = 'postgres',
            'driver'     = 'org.postgresql.Driver'
        )
    """)

    # 1-hour tumbling window — total tip amount across all locations
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
