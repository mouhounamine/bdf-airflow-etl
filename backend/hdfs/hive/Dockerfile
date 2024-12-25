FROM postgres:13

# Passer à l'utilisateur root pour installer les packages nécessaires
USER root

# Met à jour le système et installe le client PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copier le script de création de base de données dans le conteneur
COPY create-hive-db.sh /docker-entrypoint-initdb.d/create-hive-db.sh

# Rendre le script exécutable
RUN chmod +x /docker-entrypoint-initdb.d/create-hive-db.sh

# Revenir à l'utilisateur par défaut
USER postgres
