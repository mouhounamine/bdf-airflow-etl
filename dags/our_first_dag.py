from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args ={
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG (
    dag_id="our_first_dag_v5",
    default_args=default_args,
    start_date=datetime(2021, 9, 29),
    schedule_interval='@daily',
) as dag:
    task1 = BashOperator(
        task_id="first_task",
        bash_command="echo hello this is the first task"
    )
    
    task2 = BashOperator(
        task_id="second_task",
        bash_command="echo hello this is the second task"
    )
    
    task3 = BashOperator(
        task_id="third_task",
        bash_command="echo hello this is the third task and i will be running a the same time as task 2"
    )
    
    # Task dependecies method 1
    #task1.set_downstream(task2) 
    #task1.set_downstream(task3) 
    
    # Task dependecies method 2
    #task1 >> task2 
    #task1 >> task3
    
    # Task dependecies method 3
    task1 >> [task2, task3]
    