-- Question 5: Biggest pickup zone
SELECT 
    z."Zone",
    SUM(t.total_amount) as total_revenue
FROM green_taxi_trips t
JOIN taxi_zones z ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_revenue DESC
LIMIT 1;