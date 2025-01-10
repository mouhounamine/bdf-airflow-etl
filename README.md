# ETL with Airflow, HDFS, Spark

Ce projet configure un environnement complet pour traiter, analyser et visualiser des données à l'aide des technologies suivantes :

- **Apache Spark** pour le traitement distribué des données
- **Hadoop HDFS** pour le stockage distribué
- **Flask** pour l'API backend
- **React** pour l'interface utilisateur

## Structure des services

### 1. Spark Master

- **Image** : `bitnami/spark:latest`
- **Rôle** : Nœud maître Spark pour coordonner les tâches.
- **Ports** :
  - `8082` : Interface utilisateur Spark Master
  - `7077` : Port RPC Spark Master
- **Volumes** :
  - `spark-data` : Stockage persistant des données Spark
  - `./include` : Dossiers pour inclure des fichiers Airflow
  - `./apps` : Emplacement des applications Spark
  - `./data` : Répertoire des données Spark

### 2. Spark Worker

- **Image** : `bitnami/spark:latest`
- **Rôle** : Exécute les tâches distribuées attribuées par Spark Master.
- **Volumes** : Identiques à Spark Master
- **Dépendance** : Démarre après Spark Master

### 3. Hadoop Namenode

- **Image** : `apache/hadoop:3.3.5`
- **Rôle** : Gère le stockage des métadonnées du HDFS.
- **Ports** :
  - `9870` : Interface utilisateur Hadoop Namenode
- **Volumes** :
  - `./backend/hdfs/namenode/hadoop_namenode` : Données du Namenode
  - `./backend/hdfs/hadoop_config` : Configuration Hadoop
  - `./backend/hdfs/namenode/start-hdfs.sh` : Script de démarrage du HDFS

### 4. Hadoop Datanode

- **Image** : `apache/hadoop:3.3.5`
- **Rôle** : Gère le stockage physique des données dans le HDFS.
- **Volumes** :
  - `./backend/hdfs/datanode/hadoop_datanode` : Données du Datanode
  - `./backend/hdfs/hadoop_config` : Configuration Hadoop
  - `./backend/hdfs/datanode/init-datanode.sh` : Script d'initialisation du Datanode
- **Dépendance** : Démarre après le Namenode

### 5. Flask App (API Backend)

- **Build** : Context `./backend/api/`
- **Rôle** : Fournit une API pour interagir avec le backend.
- **Ports** :
  - `5000` : API Flask
- **Volumes** :
  - `./backend/airflow/uploads` : Stockage des fichiers téléchargés
- **Dépendance** : Démarre après le Namenode

### 6. Frontend (React)

- **Build** : Context `./front`
- **Rôle** : Fournit une interface utilisateur pour visualiser et interagir avec les données.
- **Ports** :
  - `3000` : Interface React
- **Volumes** :
  - `/app/.next` : Fichiers générés pour l'application React

## Réseau

Tous les services sont connectés au réseau Docker nommé `airflow` pour permettre une communication entre eux.

## Volumes

- **spark-data** : Stockage persistant pour Spark
- **Dossiers locaux** : Plusieurs volumes locaux pour Spark, Hadoop et les applications

## Prérequis

1. **Docker** : Assurez-vous que Docker est installé sur votre machine.
2. **Docker Compose** : Version 3.1 ou supérieure est nécessaire.
3. **Espace disque** : Garantissez suffisamment d'espace pour les volumes de données.

## Instructions

### 1. Cloner le projet

```bash
git clone URL-du-repository
cd bigdata-airflow-etl
```

## 2. Construire et lancer les conteneurs

```bash
docker-compose up --build `
```

## 3. Accéder aux services

- **Airflow UI** : http://localhost:8080
- **Spark Master UI** : http://localhost:8082
- **Hadoop Namenode UI** : http://localhost:9870
- **API Flask** : http://localhost:5000
- **Frontend React** : http://localhost:3000
