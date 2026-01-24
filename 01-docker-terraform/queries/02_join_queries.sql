-- GROUP BY with JOINs
-- Module 1: Docker & Terraform

-- ============================================
-- 1. Revenue by Dropoff Location
-- ============================================

SELECT 
    CONCAT(zdo."Borough", ' / ', zdo."Zone") AS dropoff_loc,
    COUNT(*) AS trip_count,
    SUM(t.total_amount) AS total_revenue,
    AVG(t.total_amount) AS avg_revenue
FROM 
    yellow_taxi_trips t
JOIN zones zdo ON t."DOLocationID" = zdo."LocationID"
GROUP BY dropoff_loc
ORDER BY total_revenue DESC
LIMIT 20;

-- ============================================
-- 2. Daily Revenue by Dropoff Location
-- ============================================

SELECT 
    DATE(t.tpep_dropoff_datetime) AS dropoff_day,
    CONCAT(zdo."Borough", ' / ', zdo."Zone") AS dropoff_loc,
    COUNT(*) AS trip_count,
    SUM(t.total_amount) AS total_revenue,
    MAX(t.total_amount) AS max_amount
FROM 
    yellow_taxi_trips t
JOIN zones zdo ON t."DOLocationID" = zdo."LocationID"
GROUP BY 
    DATE(t.tpep_dropoff_datetime),
    CONCAT(zdo."Borough", ' / ', zdo."Zone")
ORDER BY 
    dropoff_day ASC,
    total_revenue DESC;

-- ============================================
-- 3. Using Column Numbers in ORDER BY
-- ============================================

SELECT 
    DATE(t.tpep_dropoff_datetime) AS dropoff_day,
    CONCAT(zdo."Borough", ' / ', zdo."Zone") AS dropoff_loc,
    COUNT(*) AS trip_count,
    SUM(t.total_amount) AS total_revenue
FROM 
    yellow_taxi_trips t
JOIN zones zdo ON t."DOLocationID" = zdo."LocationID"
GROUP BY 1, 2
ORDER BY 1 ASC, 4 DESC;

-- ============================================
-- 4. Top Pickup-Dropoff Pairs
-- ============================================

SELECT 
    CONCAT(zpu."Borough", ' / ', zpu."Zone") AS pickup_loc,
    CONCAT(zdo."Borough", ' / ', zdo."Zone") AS dropoff_loc,
    COUNT(*) AS trip_count,
    AVG(t.total_amount) AS avg_fare
FROM 
    yellow_taxi_trips t
JOIN zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN zones zdo ON t."DOLocationID" = zdo."LocationID"
GROUP BY 1, 2
ORDER BY trip_count DESC
LIMIT 20;