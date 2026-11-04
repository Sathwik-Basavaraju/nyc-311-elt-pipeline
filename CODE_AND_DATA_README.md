# NYC 311 ELT Pipeline — Starter Code and Synthetic Sample Data

> **Important — read first:** The sample data in this folder is **synthetic
> for demonstration only**. It was generated locally (seed 42) and is **not**
> the original production data from the LinkedIn project. Likewise, the
> cloud pipeline (AWS Lambda / S3 / Snowflake / Snowpipe / dbt / Airflow)
> is shown here as **code, SQL and DAG examples only** — this is **not a
> live cloud deployment**, and no production results are claimed for this
> sample run. In particular, do **not** read the LinkedIn project's
> 1M+ rows / 40+ tests figures as results of running this starter code.

## What each file does

- `data/sample_311_requests.csv` — 900 synthetic 311 rows (see below).
- `src/generate_sample_data.py` — Generates that CSV deterministically
  with seed 42. Columns: `unique_key, created_date, closed_date,
  complaint_type, descriptor, borough, agency, status`. Boroughs:
  Manhattan, Brooklyn, Queens, Bronx, Staten Island.
- `src/ingest.py` — Simulates the Lambda ingest step locally: reads the
  sample CSV, validates required fields, drops duplicates by
  `unique_key`, writes `data/raw/311_requests_clean.csv`, and prints
  input / invalid / duplicate / output row counts.
- `sql/stg_311.sql` — Snowflake-compatible staging SQL: casts and cleans
  the raw data into `STG_311`, including a `created_month` column.
- `sql/mart_311_by_borough.sql` — Snowflake-compatible mart SQL:
  aggregates by borough, complaint type and month into
  `MART_311_BY_BOROUGH`, clustered/ordered by created month.
- `sql/data_quality_tests.sql` — A handful of example checks
  (uniqueness, nulls, borough/status domain, closed-after-created).
  These are examples only, **not** a claim of 40 tests.
- `airflow/dag_311_elt.py` — Airflow DAG skeleton, daily schedule, with
  tasks `ingest -> stage -> mart`. Airflow imports are guarded so the
  file compiles and imports even without Airflow installed. Its tasks
  are placeholders that log their step; they do not call any cloud service.
- `analysis/dashboard_charts.py` — pandas + matplotlib only. Reads the
  clean CSV and creates charts in `outputs/charts/`:
  requests by borough, by complaint type (top 10), and by month.
- `requirements.txt` — `pandas`, `matplotlib` only (both verified available).

## How to run

```bash
pip install -r requirements.txt

# 1. Generate the synthetic sample data
python3 src/generate_sample_data.py

# 2. Ingest / clean it (simulated Lambda step)
python3 src/ingest.py

# 3. Create the dashboard charts
python3 analysis/dashboard_charts.py

# Charts will be in outputs/charts/
```

## Cloud pipeline, as shown here

| LinkedIn project step | Representation in this starter |
|---|---|
| AWS Lambda ingest | `src/ingest.py` (local simulation) |
| S3 landing | `data/` CSV files (local stand-in) |
| Snowpipe load into Snowflake | `sql/stg_311.sql` (Snowflake-compatible SQL, example) |
| dbt models + tests | `sql/mart_311_by_borough.sql`, `sql/data_quality_tests.sql` (example SQL) |
| Airflow orchestration | `airflow/dag_311_elt.py` (DAG skeleton) |
| Dashboard | `analysis/dashboard_charts.py` (matplotlib charts) |

To turn this into a real cloud pipeline, you would need to provision
Lambda, S3, Snowflake/Snowpipe, dbt and Airflow yourself and point them
at real (authorised) 311 data — none of that is deployed by this code.

## Alignment update — 2026-11-04 review
New files added in this review, to align the repo with the LinkedIn tech list:
- `dbt/dbt_project.yml`, `dbt/models/stg_311.sql`, `dbt/models/mart_311_by_borough.sql`, `dbt/models/schema.yml` — dbt project/models/tests (example tests only, not 40).
- `sql/snowpipe_setup.sql` — Snowflake stage/pipe example for S3 -> Snowpipe loading.
- `data/sample_311_requests.json` — first 200 sample records as JSON, matching the README's "raw JSON in S3" description; the full sample is still the CSV.
See ALIGNMENT.md for the full claim-to-file mapping.
