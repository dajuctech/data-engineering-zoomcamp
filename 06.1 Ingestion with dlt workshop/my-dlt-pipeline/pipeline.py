import dlt
from dlt.sources.rest_api import rest_api_source


def openlibrary_source(query: str = "harry potter"):
    return rest_api_source({
        "client": {
            "base_url": "https://openlibrary.org",
        },
        "resource_defaults": {
            "primary_key": "key",
            "write_disposition": "replace",
        },
        "resources": [
            {
                "name": "books",
                "endpoint": {
                    "path": "search.json",
                    "params": {
                        "q": query,
                        "limit": 100,
                    },
                    "data_selector": "docs",
                    "paginator": {
                        "type": "offset",
                        "limit": 100,
                        "offset_param": "offset",
                        "limit_param": "limit",
                        "total_path": "numFound",
                    },
                },
            },
        ],
    })


pipeline = dlt.pipeline(
    pipeline_name="ol_demo",
    destination="duckdb",
    dataset_name="ol_data",
    progress="log"
)

# Run the full pipeline (extract + normalize + load)
load_info = pipeline.run(openlibrary_source())

print("\nPipeline complete!")
print(load_info)
