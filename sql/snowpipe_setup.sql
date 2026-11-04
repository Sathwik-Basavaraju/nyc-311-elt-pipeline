-- Snowflake Snowpipe setup (EXAMPLE ONLY, not a live deployment).
-- Replace <your_bucket>, <your_warehouse>, <your_database> and
-- <your_schema> with real values before running in Snowflake.
-- This shows how raw JSON landed in S3 would be loaded, matching
-- the LinkedIn project description: Lambda -> S3 -> Snowpipe -> Snowflake.

-- 1. Storage integration / stage for the S3 bucket (placeholder values).
CREATE OR REPLACE STAGE nyc_311_stage
  URL = 's3://<your_bucket>/nyc-311/'
  FILE_FORMAT = (TYPE = 'JSON');

-- 2. Raw table for landed JSON records.
CREATE OR REPLACE TABLE raw_311_requests (
    raw_variant VARIANT
);

-- 3. Pipe that auto-ingests new files from the stage into the raw table.
CREATE OR REPLACE PIPE nyc_311_pipe
  AUTO_INGEST = TRUE
AS
COPY INTO raw_311_requests (raw_variant)
FROM @nyc_311_stage
FILE_FORMAT = (TYPE = 'JSON');

-- 4. In the staging model (sql/stg_311.sql / dbt/models/stg_311.sql),
--    fields are extracted from raw_variant / the landed CSV columns
--    and cast/cleaned into STG_311. The sample data in this repo is
--    a CSV representation of those records (see data/sample_311_requests.csv
--    and data/sample_311_requests.json), not a live S3 load.
