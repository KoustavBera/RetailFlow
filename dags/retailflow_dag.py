"""
Apache Airflow DAG for RetailFlow ETL pipeline.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "retailflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def ingest_task():
    print("Ingesting raw data...")


def transform_task():
    print("Transforming and cleaning raw retail data...")


def quality_check_task():
    print("Running data quality validation checks...")


def load_task():
    print("Loading data into data warehouse...")


with DAG(
    "retailflow_pipeline",
    default_args=default_args,
    description="End-to-end retail data ETL pipeline",
    schedule_interval="0 2 * * *",
    catchup=False,
) as dag:

    t1_ingest = PythonOperator(
        task_id="ingest_to_s3",
        python_callable=ingest_task,
    )

    t2_transform = PythonOperator(
        task_id="clean_and_transform",
        python_callable=transform_task,
    )

    t3_quality = PythonOperator(
        task_id="run_quality_checks",
        python_callable=quality_check_task,
    )

    t4_load = PythonOperator(
        task_id="load_to_warehouse",
        python_callable=load_task,
    )

    t1_ingest >> t2_transform >> t3_quality >> t4_load
