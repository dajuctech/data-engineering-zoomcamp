-- Check for Missing Data / Data Quality
-- Module 1: Docker & Terraform

-- ============================================
-- 1. Check for LocationIDs not in zones table
-- ============================================

-- Find pickup locations not in zones
SELECT DISTINCT t."PULocationID"
FROM yellow_taxi_trips t
WHERE t."PULocationID" NOT IN (SELECT "LocationID" FROM zones);

-- Find dropoff locations not in zones
SELECT DISTINCT t."DOLocationID"
FROM yellow_taxi_trips t
WHERE t."DOLocationID" NOT IN (SELECT "LocationID" FROM zones);

-- ============================================
-- 2. Check for NULL values
-- ============================================

SELECT 
    COUNT(*) AS total_rows,
    COUNT("PULocationID") AS non_null_pickup,
    COUNT("DOLocationID") AS non_null_dropoff,
    COUNT(total_amount) AS non_null_amount
FROM yellow_taxi_trips;

-- ============================================
-- 3. Data Range Validation
-- ============================================

SELECT 
    MIN(tpep_pickup_datetime) AS earliest_pickup,
    MAX(tpep_pickup_datetime) AS latest_pickup,
    MIN(total_amount) AS min_amount,
    MAX(total_amount) AS max_amount,
    MIN(trip_distance) AS min_distance,
    MAX(trip_distance) AS max_distance
FROM yellow_taxi_trips;

-- ============================================
-- 4. Delete a zone for LEFT JOIN demonstration
-- ============================================

-- WARNING: This modifies data - use for learning only!
-- DELETE FROM zones WHERE "LocationID" = 142;

-- Verify deletion
-- SELECT * FROM zones WHERE "LocationID" = 142;