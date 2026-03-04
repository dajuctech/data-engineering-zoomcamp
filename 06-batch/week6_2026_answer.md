# Module 6 Homework — Answers

## Question 1: Install Spark and PySpark

What's the output of `spark.version`?

**Answer: 4.1.1**

---

## Question 2: Yellow November 2025

Read the November 2025 Yellow data, repartition to 4 partitions and save to parquet.
What is the average size of the Parquet files created?

**Answer: 25MB**

> Actual average: ~20.6 MB per file (4 files × ~20.6 MB each). Closest option is 25MB.

---

## Question 3: Count records

How many taxi trips were there on the 15th of November?

**Answer: 162,604**

---

## Question 4: Longest trip

What is the length of the longest trip in the dataset in hours?

**Answer: 90.6**

---

## Question 5: User Interface

Spark's User Interface runs on which local port?

**Answer: 4040**

---

## Question 6: Least frequent pickup location zone

What is the name of the LEAST frequent pickup location Zone?

**Answer: Governor's Island/Ellis Island/Liberty Island**

> Only 1 trip recorded from this zone in November 2025.
