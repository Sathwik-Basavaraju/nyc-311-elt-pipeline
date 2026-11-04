-- dbt model: mart_311_by_borough (example only).
-- Aggregates stg_311 by borough, complaint type and month.
-- In Snowflake, clustering on created_month mirrors the LinkedIn
-- project's approach of clustering the largest mart table on
-- created date (here truncated to month for the mart grain).

{{ config(
    materialized='table',
    cluster_by=['created_month']
) }}

select
    borough,
    complaint_type,
    created_month,
    count(*) as request_count,
    count_if(status = 'Closed') as closed_count,
    count_if(status = 'Open') as open_count,
    min(created_date) as first_created_date,
    max(created_date) as last_created_date
from {{ ref('stg_311') }}
group by borough, complaint_type, created_month
order by created_month, borough, complaint_type
