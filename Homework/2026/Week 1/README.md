# Module 1 Homework: Docker & SQL

## Question 1: pip Version
**Answer**: 25.1

**Command used**:
```bash
docker run --rm python:3.13 pip --version
```

## Question 2: Docker Networking
**Answer**: db:5432

**Explanation**: Inside Docker networks, containers use service names as hostnames, and connect via internal ports.

## Question 3: Short Trips Count
**Answer**: 8,007

**SQL Query**:
```sql
SELECT COUNT(*) as short_trips
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```

## Question 4: Longest Trip Day
**Answer**: 2025-11-14

**SQL Query**:
```sql
SELECT 
    DATE(lpep_pickup_datetime) as pickup_date,
    MAX(trip_distance) as max_distance
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance < 100
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY max_distance DESC
LIMIT 1;
```

## Question 5: Biggest Pickup Zone
**Answer**: East Harlem North

**SQL Query**:
```sql
SELECT 
    z."Zone",
    SUM(t.total_amount) as total_revenue
FROM green_taxi_trips t
JOIN taxi_zones z ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_revenue DESC
LIMIT 1;
```

## Question 6: Largest Tip
**Answer**: Yorkville West

**SQL Query**:
```sql
SELECT 
    dz."Zone" as dropoff_zone,
    MAX(t.tip_amount) as max_tip
FROM green_taxi_trips t
JOIN taxi_zones pz ON t."PULocationID" = pz."LocationID"
JOIN taxi_zones dz ON t."DOLocationID" = dz."LocationID"
WHERE pz."Zone" = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01'
  AND t.lpep_pickup_datetime < '2025-12-01'
GROUP BY dz."Zone"
ORDER BY max_tip DESC
LIMIT 1;
```

## Question 7: Terraform Workflow
**Answer**: terraform init, terraform apply -auto-approve, terraform destroy

**Explanation**:
- `terraform init`: Downloads provider plugins and sets up backend
- `terraform apply -auto-approve`: Generates and executes changes automatically
- `terraform destroy`: Removes all managed resources