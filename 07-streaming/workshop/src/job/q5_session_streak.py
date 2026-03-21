"""
Q5: PyFlink job — session window with 5-minute gap on PULocationID.
    Finds the location with the longest streak (most trips in one session).

Create the PostgreSQL table first:
    CREATE TABLE IF NOT EXISTS session_streaks (
        "PULocationID" INTEGER,
        session_start  TIMESTAMP,
        session_end    TIMESTAMP,
        num_trips      BIGINT
    );

Submit:
    docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q5_session_streak.py

Query results:
    SELECT "PULocationID", num_trips
    FROM session_streaks
    ORDER BY num_trips DESC
    LIMIT 3;

Answer: longest session has 51 trips
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
            'properties.group.id'           = 'flink-q5',
            'scan.startup.mode'             = 'earliest-offset',
            'format'                        = 'json'
        )
    """)

    # Sink: PostgreSQL
    t_env.execute_sql("""
        CREATE TABLE session_streaks (
            PULocationID  INTEGER,
            session_start TIMESTAMP(3),
            session_end   TIMESTAMP(3),
            num_trips     BIGINT
        ) WITH (
            'connector'  = 'jdbc',
            'url'        = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'session_streaks',
            'username'   = 'postgres',
            'password'   = 'postgres',
            'driver'     = 'org.postgresql.Driver'
        )
    """)

    # Session window — closes after 5-minute gap in events per PULocationID
    t_env.execute_sql("""
        INSERT INTO session_streaks
        SELECT
            PULocationID,
            SESSION_START(event_timestamp, INTERVAL '5' MINUTE) AS session_start,
            SESSION_END(event_timestamp,   INTERVAL '5' MINUTE) AS session_end,
            COUNT(*) AS num_trips
        FROM green_trips_source
        GROUP BY
            SESSION(event_timestamp, INTERVAL '5' MINUTE),
            PULocationID
    """).wait()


if __name__ == '__main__':
    main()
