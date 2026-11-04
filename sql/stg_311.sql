-- Snowflake-compatible staging model (example, not a live deployment).
-- Source: raw 311 requests landed from S3 via Snowpipe (see CODE_AND_DATA_README.md).
-- In a real dbt project this would be a dbt model; here it is plain SQL
-- showing the same transformations.

CREATE OR REPLACE TABLE STG_311 AS
SELECT
    UNIQUE_KEY::NUMBER AS unique_key,
    TO_TIMESTAMP(CREATED_DATE) AS created_date,
    -- Closed date may be empty for open requests.
    CASE
        WHEN CLOSED_DATE IS NULL OR CLOSED_DATE = '' THEN NULL
        ELSE TO_TIMESTAMP(CLOSED_DATE)
    END AS closed_date,
    TRIM(COMPLAINT_TYPE) AS complaint_type,
    TRIM(DESCRIPTOR) AS descriptor,
    TRIM(BOROUGH) AS borough,
    TRIM(AGENCY) AS agency,
    TRIM(STATUS) AS status,
    DATE_TRUNC('MONTH', TO_TIMESTAMP(CREATED_DATE)) AS created_month
FROM RAW_311_REQUESTS
WHERE UNIQUE_KEY IS NOT NULL
  AND CREATED_DATE IS NOT NULL
  AND COMPLAINT_TYPE IS NOT NULL;
