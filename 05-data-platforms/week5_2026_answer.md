# Module 5 Homework — Answers (2026 Cohort)

> Full explanations: [module_guide.md](module_guide.md) — Part 11

---

| # | Question | Answer |
|---|---|---|
| Q1 | What are the required files/directories in a Bruin project? | **B** — `.bruin.yml` and `pipeline.yml` (assets can be anywhere) |
| Q2 | Which materialization strategy for the staging layer (time-based, deduplicating)? | **C** — `time_interval` |
| Q3 | How do you override `taxi_types` to only process yellow taxis? | **C** — `bruin run --var 'taxi_types=["yellow"]'` |
| Q4 | Run `ingestion/trips.py` plus all downstream assets? | **B** — `bruin run ingestion/trips.py --downstream` |
| Q5 | Ensure `pickup_datetime` never has NULL values? | **B** — `not_null` check |
| Q6 | Command to visualize the dependency graph? | **C** — `bruin lineage` |
| Q7 | Flag to create tables from scratch on first run? | **C** — `--full-refresh` |
