# NYC 311 Service Requests ELT Pipeline
Jun-Aug 2026
Built an automated ELT pipeline that ingests NYC 311 service requests daily through AWS Lambda, lands raw JSON in Amazon S3, and loads 1M+ rows into Snowflake with Snowpipe.
Developed dbt staging and mart models with 40+ data quality tests covering uniqueness, null checks, and referential integrity, and orchestrated end-to-end runs with Airflow, cutting manual reporting prep by 6 hours per week.
Held warehouse compute to about $25 per month with an X-Small warehouse and 60-second auto-suspend, and clustered the largest mart table on created date to cut scan time by 35%.
Tech: AWS Lambda, Amazon S3, Snowflake, Snowpipe, dbt, Airflow, SQL, Python
