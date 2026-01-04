from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='snowflake_dbt_ml_pipeline',
    start_date=datetime(2026, 1, 1),
    schedule='@daily',
    catchup=False
) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /mnt/d/ECOMMERCE_PROJECT/snowflake_data_project && source venv_wsl/bin/activate && dbt run --full-refresh'
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /mnt/d/ECOMMERCE_PROJECT/snowflake_data_project && source venv_wsl/bin/activate && dbt test'
    )

    train_ml_model = BashOperator(
        task_id='train_ml_model',
        bash_command='cd /mnt/d/ECOMMERCE_PROJECT/snowflake_data_project && source venv_wsl/bin/activate && python ml_scripts/train_churn_model.py'
    )

    dbt_run >> dbt_test >> train_ml_model