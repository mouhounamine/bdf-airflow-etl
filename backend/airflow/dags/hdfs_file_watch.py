from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hdfs.hooks.hdfs import HDFSHook
from datetime import datetime, timedelta
import logging
from hdfs import InsecureClient

# Définir les arguments par défaut du DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,  # Nombre de réessais automatiques
    'retry_delay': timedelta(seconds=10),  # Intervalle entre les réessais
}

# Fonction pour vérifier les fichiers dans le répertoire HDFS
def check_hdfs_files(**kwargs):
    hook = HDFSHook(hdfs_conn_id='hdfs_default')
    logging.info("Connexion à HDFS établie.")
    
    # Utiliser get_conn() pour obtenir un client hdfs
    hdfs_client = hook.get_conn()

    # Remplacez par l'URL de votre serveur HDFS
    hdfs_url = "http://namenode:9870"  # Changez selon votre URL HDFS

    # Créer un client HDFS pour interagir avec le système de fichiers
    client = InsecureClient(hdfs_url)

    try:
        # Lister les fichiers dans le répertoire /uploads
        files = client.list('/uploads')  # Remplacez '/uploads' par votre chemin réel
        if files:
            logging.info(f"Fichiers trouvés dans /uploads: {files}")
            return True  # Retourner True si des fichiers sont trouvés
        else:
            logging.info("Aucun fichier trouvé dans /uploads. Tentative suivante dans 10 secondes.")
            return False  # Ne pas lever d'exception, juste une tentative infructueuse
    except Exception as e:
        logging.error(f"Erreur lors de la connexion à HDFS ou de la liste des fichiers : {str(e)}")
        raise e  # Relancer l'exception pour réessayer

# Initialiser le DAG
with DAG(
    dag_id='hdfs_file_watcher',
    default_args=default_args,
    description='Surveille un répertoire HDFS et déclenche un traitement',
    schedule_interval='* * * * *',  # Exécuter toutes les minutes pour vérifier le répertoire
    start_date=datetime(2024, 12, 17),
    catchup=False,  # Ne pas exécuter les tâches pour des périodes passées
    max_active_runs=1,  # Éviter l'exécution en parallèle
    is_paused_upon_creation=False  # Le DAG est dépausé par défaut dès sa création
) as dag:

    # Tâche : surveiller l'apparition d'un fichier dans le répertoire HDFS
    wait_for_file = PythonOperator(
        task_id='wait_for_file',
        python_callable=check_hdfs_files,  # Appeler la fonction de vérification
        retries=5,  # Nombre de réessais automatiques
        retry_delay=timedelta(seconds=10),  # Attendre 10 secondes entre chaque réessai
    )

    # Tâche : exécuter un traitement après détection d'un fichier
    process_file = BashOperator(
        task_id='process_file',
        bash_command='echo "Fichier détecté dans HDFS et traitement lancé!"',
    )

    # Définir l'ordre des tâches
    wait_for_file >> process_file
