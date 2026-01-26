# Module 1 Homework: Docker & SQL (2026 Cohort)

## Question 1. Understanding Docker images
**Question**: Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container. What's the version of pip in the image?

**Answer**: 25.3

**Command used**:
```bash
docker run --rm -it --entrypoint bash python:3.13
pip --version
```

**Explanation**: The `--entrypoint bash` flag overrides the default entrypoint to give us an interactive bash shell where we can run `pip --version` to check the installed version.

---

## Question 2. Understanding Docker networking and docker-compose
**Question**: Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

**Answer**: db:5432

**Explanation**: 
- Inside Docker Compose networks, containers communicate using **service names** as hostnames (not container names)
- The service name is `db` (not `postgres`, which is the container name)
- Inside the network, containers use **internal ports** (5432), not external mapped ports (5433)
- The external port 5433 is only for accessing from the host machine
- Therefore, pgAdmin connects to `db:5432`

---

## Question 3. Counting short trips
**Question**: For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

**Answer**: 8,007

**SQL Query**:
```sql
SELECT COUNT(*) as short_trips
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```

**Explanation**: The query filters trips in November 2025 with distance ≤ 1 mile. Note the exclusive upper bound (`<` not `<=`).

---

## Question 4. Longest trip for each day
**Question**: Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles.

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

**Explanation**: 
- Groups trips by pickup date
- Filters out trips ≥ 100 miles (data errors)
- Finds the maximum distance for each day
- Returns the day with the longest trip

---

## Question 5. Biggest pickup zone
**Question**: Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

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

**Explanation**: 
- Joins trips with zones table on pickup location
- Filters for November 18th, 2025
- Calculates total revenue per zone
- Returns the zone with highest revenue

---

## Question 6. Largest tip
**Question**: For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

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

**Explanation**: 
- Joins trips with zones twice (pickup zone `pz` and dropoff zone `dz`)
- Filters for pickups in "East Harlem North" during November 2025
- Groups by dropoff zone
- Finds the maximum tip for each dropoff zone
- Returns the zone with the largest tip

---

## Question 7. Terraform Workflow
**Question**: Which of the following sequences describes the workflow for: (1) Downloading provider plugins and setting up backend, (2) Generating proposed changes and auto-executing the plan, (3) Remove all resources managed by terraform?

**Answer**: terraform init, terraform apply -auto-approve, terraform destroy

**Explanation**:
- **`terraform init`**: Downloads provider plugins (e.g., google, aws) and initializes the backend (state storage)
- **`terraform apply -auto-approve`**: Generates execution plan and automatically applies changes without prompting for confirmation
- **`terraform destroy`**: Removes all resources that Terraform currently manages (as recorded in state file)

**Why other options are wrong**:
- `terraform import`: Imports existing resources into Terraform state (not for initial setup)
- `terraform plan -auto-apply`: Not a valid flag combination
- `terraform run`: Not a valid Terraform command
- `terraform rm`: Not a valid command (should be `terraform state rm` for removing from state)

