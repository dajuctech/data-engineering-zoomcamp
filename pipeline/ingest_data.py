#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# Read a sample of the data
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
df = pd.read_csv(prefix + '/yellow_tripdata_2021-01.csv.gz', nrows=100)

# Display first rows
df.head()

# Check data types
df.dtypes

# Check data shape
df.shape


# In[2]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    prefix + '/yellow_tripdata_2021-01.csv.gz',
    ##nrows=100
    dtype=dtype,
    parse_dates=parse_dates
)


# In[3]:


len(df)


# In[4]:


df.head()


# In[5]:




# In[6]:


# how to connect to the database
from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[7]:




# In[ ]:


#df.to_sql(name='yellow_taxi_data', con=engine)
df.to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[ ]:


# schema that will be created inside the database
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[ ]:


# Create the table:
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[ ]:


# Define variables
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)


# In[ ]:


df_iter


# In[ ]:


for df_chunk in df_iter:
    print(len(df_chunk))


# In[ ]:


# Define variables
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'

dtype = {
    'VendorID': 'Int64',
    'passenger_count': 'Int64',
    'trip_distance': 'float64',
    'RatecodeID': 'Int64',
    'store_and_fwd_flag': 'object',
    'PULocationID': 'Int64',
    'DOLocationID': 'Int64',
    'payment_type': 'Int64',
    'fare_amount': 'float64',
    'extra': 'float64',
    'mta_tax': 'float64',
    'tip_amount': 'float64',
    'tolls_amount': 'float64',
    'improvement_surcharge': 'float64',
    'total_amount': 'float64',
    'congestion_surcharge': 'float64'
}

parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']


# In[ ]:


# Create iterator
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)


# In[ ]:


# Process chunks
for df_chunk in df_iter:
    print(f"Processing chunk with {len(df_chunk)} rows")
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append', index=False)
    print("Chunk inserted")


# In[ ]:




# In[ ]:


# insert into the database
from tqdm.auto import tqdm


# In[ ]:


from tqdm.auto import tqdm

for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[ ]:




