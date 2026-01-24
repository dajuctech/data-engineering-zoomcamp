-- Basic SQL Queries for NYC Taxi Data
-- Module 1: Docker & Terraform

-- ============================================
-- 1. Exploring the Data
-- ============================================

-- Check first few rows of taxi trips
SELECT * FROM yellow_taxi_trips LIMIT 10;

-- Count total records
SELECT COUNT(*) FROM yellow_taxi_trips;

-- Check zones table
SELECT * FROM zones LIMIT 10;

-- Count zones
SELECT COUNT(*) FROM zones;

-- ============================================
-- 2. Basic Aggregations
-- ============================================

-- Maximum tip amount
SELECT MAX(tip_amount) FROM yellow_taxi_trips;

-- Maximum total amount
SELECT MAX(total_amount) FROM yellow_taxi_trips;

-- Average fare
SELECT AVG(fare_amount) AS avg_fare FROM yellow_taxi_trips;

-- ============================================
-- 3. GROUP BY Queries
-- ============================================

-- Trips per day
SELECT 
    DATE(tpep_pickup_datetime) AS pickup_day,
    COUNT(*) AS trip_count
FROM yellow_taxi_trips
GROUP BY DATE(tpep_pickup_datetime)
ORDER BY pickup_day;

-- Trips per day with revenue
SELECT 
    DATE(tpep_pickup_datetime) AS pickup_day,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS daily_revenue,
    MAX(total_amount) AS max_fare,
    MAX(tip_amount) AS max_tip
FROM yellow_taxi_trips
GROUP BY DATE(tpep_pickup_datetime)
ORDER BY pickup_day;