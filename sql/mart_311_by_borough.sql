-- Snowflake-compatible mart model (example, not a live deployment).
-- Aggregates staged 311 requests by borough, complaint type and month.
-- Clustered / ordered by created_date, mirroring the LinkedIn project's
-- approach of clustering the largest mart table on created date.

CREATE OR REPLACE TABLE MART_311_BY_BOROUGH
CLUSTER BY (created_month)
AS
SELECT
    borough,
    complaint_type,
    created_month,
    COUNT(*) AS request_count,
    COUNT_IF(status = 'Closed') AS closed_count,
    COUNT_IF(status = 'Open') AS open_count,
    MIN(created_date) AS first_created_date,
    MAX(created_date) AS last_created_date
FROM STG_311
GROUP BY borough, complaint_type, created_month
ORDER BY created_month, borough, complaint_type;
