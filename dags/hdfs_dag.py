from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os
import pandas as pd
from hdfs import InsecureClient

# Définir les paramètres du DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    dag_id='process_csv_on_hdfs_with_spark',
    default_args=default_args,
    description='Un DAG pour traiter un fichier CSV depuis HDFS avec Spark',
    schedule_interval=None,  # Peut être ajusté selon la fréquence des traitements
    catchup=False,
)

# Fonction pour vérifier si le fichier existe sur HDFS avec InsecureClient
def check_file_on_hdfs():
    client = InsecureClient('http://namenode:9870')  
    file_path = '/uploads/vgchartz-2024.csv'
    
    # Vérifier si le fichier existe sur HDFS
    if client.status(file_path, strict=False):
        print(f"Le fichier {file_path} existe sur HDFS.")
    else:
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas sur HDFS.")

# Étape 1: Vérifier si le fichier CSV existe sur HDFS
check_hdfs_file = PythonOperator(
    task_id='check_hdfs_file',
    python_callable=check_file_on_hdfs,
    dag=dag,
)

# Étape 2: Soumettre un job Spark pour traiter le fichier CSV
spark_processing = SparkSubmitOperator(
    task_id='spark_processing',
    conn_id='my_spark_conn',  # Utilisez votre connexion Spark
    application='./include/scripts/script_spark.py',  # Le script Spark que vous allez soumettre
    name='spark_csv_processing',
    application_args=[
        'hdfs://namenode:9000/uploads/vgchartz-2024.csv',  # Chemin du fichier CSV sur HDFS
        'hdfs://namenode:9000/processed/processed_vgchartz-2024.csv',  # Chemin de sortie sur HDFS
    ],
    dag=dag,
)

# Définir l'ordre des tâches
check_hdfs_file >> spark_processing
