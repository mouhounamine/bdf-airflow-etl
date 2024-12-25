#!/bin/bash
set -e  # Arrête le script en cas d'erreur
set -x  # Affiche chaque commande exécutée (mode debug)

echo "Création de la base de données Hive dans PostgreSQL..."
echo "Sur le point de créer!"

# Utilisation de psql pour créer la base de données et l'utilisateur
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
  CREATE DATABASE hive;
  CREATE USER hiveuser WITH PASSWORD 'hivepassword';
  GRANT ALL PRIVILEGES ON DATABASE hive TO hiveuser;
EOSQL

echo "Base de données Hive créée avec succès."
