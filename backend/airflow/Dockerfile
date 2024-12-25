FROM apache/airflow:2.0.1

# Passer en mode root pour installer des dépendances système
USER root

# Mettre à jour les paquets et installer les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y \
    krb5-user \
    libkrb5-dev \
    build-essential \
    libffi-dev \
    libssl-dev \
    && apt-get clean

# Installer les dépendances Python nécessaires pour Airflow, Hive, Spark et HDFS
RUN pip install apache-airflow-providers-apache-hdfs apache-airflow-providers-apache-hive apache-airflow-providers-apache-spark pyspark

# Copier le script d'initialisation dans l'image Docker
COPY init-airflow.sh /init-airflow.sh

# Donner les droits d'exécution au script
RUN chmod +x /init-airflow.sh

# Exécuter le script d'initialisation
RUN /bin/bash /init-airflow.sh

# Revenir à l'utilisateur airflow pour éviter d'exécuter d'autres commandes en tant que root
USER airflow
