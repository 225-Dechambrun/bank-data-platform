from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

with DAG(
    dag_id="bank_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["bank", "data-engineering"],
    template_searchpath=["/opt/airflow/sql"],
) as dag:

    start = EmptyOperator(task_id="start")

    run_warehouse_sql = SQLExecuteQueryOperator(
        task_id="run_warehouse_sql",
        conn_id="bank_db",
        sql="warehouse.sql",
    )

    end = EmptyOperator(task_id="end")

    start >> run_warehouse_sql >> end
