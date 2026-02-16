# Module 4 Homework Answers - Analytics Engineering with dbt (2026 Cohort)

---

## Question 1: dbt Lineage and Execution

If you run `dbt run --select int_trips_unioned`, what models will be built?

**Answer:** int_trips_unioned only

---

## Question 2: dbt Tests

Your model fct_trips has been running successfully for months. A new value 6 now appears in the source data for payment_type (which only accepts values [1, 2, 3, 4, 5]).

What happens when you run `dbt test --select fct_trips`?

**Answer:** dbt will fail the test, returning a non-zero exit code

---

## Question 3: Counting Records in fct_monthly_zone_revenue

What is the count of records in the fct_monthly_zone_revenue model?

**Answer:** 12,184

---

## Question 4: Best Performing Zone for Green Taxis (2020)

Which pickup zone had the highest total revenue for Green taxi trips in 2020?

**Answer:** East Harlem North

---

## Question 5: Green Taxi Trip Counts (October 2019)

What is the total number of trips (total_monthly_trips) for Green taxis in October 2019?

**Answer:** 421,509

---

## Question 6: Build a Staging Model for FHV Data

What is the count of records in stg_fhv_tripdata (after filtering out records where dispatching_base_num IS NULL)?

**Answer:** 43,244,693

---
