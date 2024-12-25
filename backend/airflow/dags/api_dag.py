from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'amine',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id="api_dag",
    default_args=default_args,
    start_date=datetime(2021, 9, 29),
    schedule_interval=None,  # Pas de planification automatique
    catchup=False,  
) as dag:

    task1 = BashOperator(
        task_id="first_task",
        bash_command="echo Amine"
    )
    
    task2 = BashOperator(
        task_id="second_task",
        bash_command="echo MOUHOUN"
    )
    
    task3 = BashOperator(
        task_id="third_task",
        bash_command="echo AMINE MOUHOUN"
    )
    
    task1 >> [task2, task3]
