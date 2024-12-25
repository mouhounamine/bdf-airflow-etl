from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import psycopg2
import os

def create_hive_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=os.getenv("POSTGRES_USER", "airflow"),
            password=os.getenv("POSTGRES_PASSWORD", "airflow"),
            host="postgres"
        )
        conn.autocommit = True  

        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE hive;")
        cursor.execute("CREATE USER hiveuser WITH PASSWORD 'hivepassword';")
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE hive TO hiveuser;")
        cursor.close()

        print("Base de données Hive créée avec succès.")
        conn.close()
    except Exception as e:
        print(f"Erreur lors de la création de la base de données Hive : {e}")
        raise

dag = DAG(
    'create_hive_db_dag',  
    description='DAG pour créer la base de données Hive dans PostgreSQL',
    schedule_interval=None, 
    start_date=days_ago(1),  
    catchup=False,
    is_paused_upon_creation=False  
)

create_db_task = PythonOperator(
    task_id='create_hive_db_task',
    python_callable=create_hive_db, 
    dag=dag,
)

create_db_task 
