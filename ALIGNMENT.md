# Alignment — NYC 311 Service Requests ELT Pipeline

Main README (original LinkedIn description) vs files in this repo.
Sample data is synthetic; original production figures are NOT claimed
as results of this starter code. See CODE_AND_DATA_README.md.

| README claim | Representation in this repo | Status |
|---|---|---|
| Daily ingest via AWS Lambda | `src/ingest.py` (local simulation) + `airflow/dag_311_elt.py` ingest task | Example, not live Lambda |
| Raw JSON landed in Amazon S3 | `data/sample_311_requests.json` (200 records) + `sql/snowpipe_setup.sql` stage | Example; full sample is CSV |
| Load 1M+ rows into Snowflake via Snowpipe | `sql/snowpipe_setup.sql`, `sql/stg_311.sql` | Example only; sample is 900 rows |
| dbt staging and mart models | `dbt/models/stg_311.sql`, `dbt/models/mart_311_by_borough.sql`, `dbt/dbt_project.yml` | dbt form, example only |
| 40+ data quality tests | `sql/data_quality_tests.sql` (6 examples) + `dbt/models/schema.yml` (example tests) | Examples only, NOT 40 tests |
| Airflow orchestration | `airflow/dag_311_elt.py` (daily, ingest -> stage -> mart) | Skeleton, guarded imports |
| Warehouse ~$25/month, X-Small, 60s auto-suspend | Stated in main README only; no live warehouse here | Original project context only |
| Cluster largest mart on created date, 35% scan cut | `sql/mart_311_by_borough.sql` clusters by created_month | Mart grain is month; see SQL comment |
| 6 hours/week manual prep saved | Stated in main README only | Original project context only |

What was fixed in the 2026-11-04 review: added dbt project files,
Snowpipe setup SQL, and a JSON sample — these were previously only
mentioned in comments. No main README content was changed.
