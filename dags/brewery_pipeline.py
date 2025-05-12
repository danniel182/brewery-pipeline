from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
} #possibillida politica de retry e alerta caso necessario

with DAG(
    dag_id="etl_brewery",
    start_date=datetime(2023,1,1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
) as dag:
    extract = BashOperator(
        task_id="extract_breweries",
        bash_command="python3 /opt/airflow/scripts/extract_breweries.py"
        #sla=timedelta(minutes=10),                         - possível adicao de sla para cada uma das tarefas
        #on_failure_callback=notificar_falha                - e notificação de falha
    )

    transform = BashOperator(
        task_id="transform_breweries",
        bash_command="python3 /opt/airflow/scripts/transform_breweries.py"
    )

    aggregate = BashOperator(
        task_id="aggregate_breweries",
        bash_command="python3 /opt/airflow/scripts/aggregate_breweries.py"
    )

    extract >> transform >> aggregate