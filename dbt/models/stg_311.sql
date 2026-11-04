-- dbt model: stg_311 (example only, not a live Snowflake deployment).
-- Mirrors sql/stg_311.sql, in dbt form. Source RAW_311_REQUESTS is
-- the table landed from S3 via Snowpipe (see sql/snowpipe_setup.sql).
-- In a real dbt project, define the source in dbt/models/sources.yml.

{{ config(materialized='table') }}

select
    unique_key::number as unique_key,
    to_timestamp(created_date) as created_date,
    case
        when closed_date is null or closed_date = '' then null
        else to_timestamp(closed_date)
    end as closed_date,
    trim(complaint_type) as complaint_type,
    trim(descriptor) as descriptor,
    trim(borough) as borough,
    trim(agency) as agency,
    trim(status) as status,
    date_trunc('month', to_timestamp(created_date)) as created_month
from {{ source('raw', 'raw_311_requests') }}
where unique_key is not null
  and created_date is not null
  and complaint_type is not null
