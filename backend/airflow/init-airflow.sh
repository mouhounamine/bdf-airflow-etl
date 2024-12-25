#!/bin/bash

set -e 
set -x 

echo "Vérification que le serveur Airflow est prêt..."
while ! curl -s http://etl-airflow-webserver-1:8080/health | grep '"status": "healthy"'; do
  echo "Le serveur Airflow n'est pas prêt. Nouvelle tentative dans 5 secondes..."
  sleep 5
done

echo "Création des connexions HDFS, HIVE & PostgreSQL dans Airflow..."

# Nécessaire pour intéragir avec HDFS
airflow connections add 'hdfs_default' --conn-type 'HDFS' --conn-host 'namenode' --conn-port '8020' --conn-schema 'webhdfs' --conn-login 'dr.who' --conn-password ''

# Nécessaire pour intéragir avec Hive
airflow connections add 'hive_default' --conn-type 'HiveServer2' --conn-host 'hive-server2' --conn-port '10000' --conn-schema 'default' --conn-login 'hiveuser' --conn-password 'hivepassword'

# Nécessaire pour intéragir avec la bd PostgreSQL afin de créer la table Hive
airflow connections add 'postgres_default' --conn-type 'postgres' --conn-host 'postgres' --conn-login 'airflow' --conn-password 'airflow' --conn-schema 'postgres'

echo "Connexions HDFS, HIVE, PostgreSQL ajoutées avec succès à Airflow"
