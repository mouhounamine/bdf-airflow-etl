from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'amine',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def greet(name):
    print ('Hello World ! My name: %s' % name)

with DAG(
    dag_id="our_first_dag_with_python_operator_v01",
    default_args=default_args,
    start_date=datetime(2021, 9, 29),
    schedule_interval='@daily',
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'name': 'Tom'}
    )
    
    