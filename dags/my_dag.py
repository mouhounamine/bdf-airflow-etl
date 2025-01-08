from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

@dag(
    schedule=None,
    catchup=False,
    start_date=datetime(2023, 1, 1),  # Ajout d'une start_date requise par Airflow
)
def my_dag():
    # Première tâche : Nettoyage des données (exécution de clean_csv.py)
    clean_data = SparkSubmitOperator(
        task_id="clean_data",  # Tâche pour le nettoyage des données
        application="./include/scripts/clean_csv.py",  # chemin vers votre script de nettoyage
        conn_id="my_spark_conn",  # Connexion Spark à utiliser
        verbose=True,  # pour plus de logs détaillés
    )
    
    # Deuxième tâche : Lecture des données (comme précédemment)
    read_data = SparkSubmitOperator(
        task_id="read_data",  # Tâche pour lire les données traitées
        application="./include/scripts/request_pyspark.py",  # chemin vers votre script d'analyse
        conn_id="my_spark_conn",  # Connexion Spark
        verbose=True,
    )
    
    # Définition de l'ordre des tâches
    clean_data >> read_data  # Nettoyage avant la lecture des données

# Exécution du DAG
my_dag()
