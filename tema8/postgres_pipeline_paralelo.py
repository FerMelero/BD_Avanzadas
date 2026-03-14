from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "cesar",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="postgres_pipeline_paralelo",
    description="Pipeline con ramas paralelas para clase de Airflow",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["postgres", "airflow", "clase", "paralelo"],
) as dag:

    check_connection = BashOperator(
        task_id="check_connection",
        bash_command="python /opt/airflow/dags/scripts/00_check_connection.py",
    )

    create_schema = BashOperator(
        task_id="create_schema",
        bash_command="python /opt/airflow/dags/scripts/01_create_schema.py",
    )

    insert_rows = BashOperator(
        task_id="insert_rows",
        bash_command="python /opt/airflow/dags/scripts/02_insert_rows.py",
    )

    select_rows = BashOperator(
        task_id="select_rows",
        bash_command="python /opt/airflow/dags/scripts/03_select_rows.py",
    )

    update_rows = BashOperator(
        task_id="update_rows",
        bash_command="python /opt/airflow/dags/scripts/04_update_rows.py",
    )

    delete_rows = BashOperator(
        task_id="delete_rows",
        bash_command="python /opt/airflow/dags/scripts/05_delete_rows.py",
    )

    transactions = BashOperator(
        task_id="transactions",
        bash_command="python /opt/airflow/dags/scripts/06_transactions.py",
    )

    pooling = BashOperator(
        task_id="pooling",
        bash_command="python /opt/airflow/dags/scripts/07_pooling.py",
    )

    final_audit = BashOperator(
        task_id="final_audit",
        bash_command="echo 'Pipeline completado y revisado'",
        trigger_rule="none_failed_min_one_success",
    )

    check_connection >> create_schema >> insert_rows

    insert_rows >> select_rows
    insert_rows >> update_rows
    insert_rows >> transactions

    select_rows >> delete_rows
    transactions >> pooling

    [delete_rows, update_rows, pooling] >> final_audit
