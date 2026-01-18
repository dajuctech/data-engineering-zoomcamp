import sys

import pandas as pd

print("arguments:", sys.argv)

# Check if enough arguments are provided
if len(sys.argv) < 3:
    print("Usage: python pipeline.py <day> <month>")
    print("Example: python pipeline.py 10 1")
    sys.exit(1)

day = int(sys.argv[1])
month = int(sys.argv[2])

df = pd.DataFrame({"day": [1, 2], "num_passengers": [3, 4]})
df['month'] = month
print(df.head())

df.to_parquet(f"output_{month}.parquet")

print(f'hello pipeline, month={month}')