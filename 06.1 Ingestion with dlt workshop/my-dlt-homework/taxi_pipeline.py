import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig

@dlt.source
def taxi_pipeline_rest_api_source():
    """Ingest NYC Taxi data from the public REST API."""
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
        },
        "resources": [
            {
                "name": "nyc_taxi_trips",
                "endpoint": "/",
                "params": {},
                "pagination": {
                    "type": "page",
                    "parameter": "page",
                    "start": 1,
                    "increment": 1,
                    "stop_condition": "empty_page"
                }
            }
        ],
        # No authentication needed
    }
    yield from rest_api_resources(config)

pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="ny_taxi",
    progress="log",
)

if __name__ == "__main__":
    load_info = pipeline.run(taxi_pipeline_rest_api_source())
    print(load_info)
