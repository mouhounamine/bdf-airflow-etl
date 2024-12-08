from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta
import boto3
import logging
import os

# Configurer S3 en utilisant les variables d'environnement
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

S3_BUCKET = 'bigdata-bdml2-project-bucket'  

def upload_to_s3(**kwargs):
    file_name = kwargs['dag_run'].conf.get('file_name')  # Récupérer le nom du fichier depuis 'conf'
    
    if not file_name:
        raise ValueError("File name not provided in conf")
    
    file_path = f"/app/uploads/{file_name}"  
    try:
        # Ouvrir le fichier et le charger sur S3
        with open(file_path, 'rb') as data:
            s3_client.upload_fileobj(data, S3_BUCKET, file_name)
            
        logging.info(f"File {file_name} uploaded to S3 bucket {S3_BUCKET}")
    except Exception as e:
        logging.error(f"Error uploading file {file_name} to S3: {str(e)}")
        raise

default_args = {
    'owner': 'amine',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Définir le DAG
with DAG(
    'user_upload_handler',
    default_args=default_args,
    description='DAG pour uploader un fichier CSV vers S3',
    schedule_interval=None,  # Le DAG ne s'exécute pas automatiquement, il est déclenché manuellement
    start_date=datetime(2024, 12, 7),
    catchup=False,  
) as dag:

    # Tâche pour lister les fichiers dans le répertoire partagé
    task1 = BashOperator(
        task_id="list_directory",
        bash_command="ls /app/uploads"  # Lister les fichiers dans le répertoire partagé
    )

    # Définir la tâche d'upload
    upload_task = PythonOperator(
        task_id='upload_csv_to_s3',
        python_callable=upload_to_s3,
        provide_context=True,  # Permet de passer le contexte au callable
    )

    # Définir l'ordre des tâches dans le DAG
    task1 >> upload_task  # Task3 doit être exécutée avant upload_task
