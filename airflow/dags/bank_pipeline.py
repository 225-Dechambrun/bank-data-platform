from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

with DAG(
    dag_id="bank_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["bank", "data-engineering"]
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    start >> end
