"""Airflow DAG skeleton for the NYC 311 ELT pipeline (example only).

Schedule: daily. Tasks: ingest -> stage -> mart.
This is a skeleton showing the DAG structure; it is NOT a live cloud
deployment and its task functions only log their step (they do not
call Lambda, S3, Snowflake or Snowpipe).

Airflow imports are guarded so this file compiles and imports even
where Airflow is not installed.
"""

from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator

    _AIRFLOW_AVAILABLE = True
except ImportError:  # pragma: no cover - allows local compile/import without Airflow
    _AIRFLOW_AVAILABLE = False

    class DAG:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    class PythonOperator:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs):
            self.task_id = kwargs.get("task_id", "task")

        def __rshift__(self, other):
            return other


def ingest(**_kwargs):
    """Placeholder for the Lambda/S3 ingest step (see src/ingest.py locally)."""
    print("ingest: read CSV, validate, de-duplicate, write clean data")


def stage(**_kwargs):
    """Placeholder for the staging step (see sql/stg_311.sql)."""
    print("stage: build STG_311 from raw data")


def mart(**_kwargs):
    """Placeholder for the mart step (see sql/mart_311_by_borough.sql)."""
    print("mart: build MART_311_BY_BOROUGH, clustered by created_month")


default_args = {
    "owner": "sathwik",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2026, 1, 1),
}

with DAG(
    dag_id="nyc_311_elt_daily",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:
    ingest_task = PythonOperator(task_id="ingest", python_callable=ingest)
    stage_task = PythonOperator(task_id="stage", python_callable=stage)
    mart_task = PythonOperator(task_id="mart", python_callable=mart)

    ingest_task >> stage_task >> mart_task

if __name__ == "__main__":
    print(f"Airflow available: {_AIRFLOW_AVAILABLE}")
    print(f"DAG defined: {dag.kwargs.get('dag_id') if hasattr(dag, 'kwargs') else 'nyc_311_elt_daily'}")
