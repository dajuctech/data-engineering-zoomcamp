# Module 5 Homework — Answers (2026 Cohort)

---

Q1. What are the required files/directories in a Bruin project?
.bruin.yml and pipeline.yml

Q2. Which materialization strategy for the staging layer (time-based, deduplicating)?
time_interval

Q3. How do you override `taxi_types` to only process yellow taxis?
bruin run --var 'taxi_types=["yellow"]'

Q4. Run `ingestion/trips.py` plus all downstream assets?
bruin run ingestion/trips.py --downstream

Q5. Ensure `pickup_datetime` never has NULL values?
not_null

Q6. Command to visualize the dependency graph?
bruin lineage

Q7. Flag to create tables from scratch on first run?
--full-refresh
