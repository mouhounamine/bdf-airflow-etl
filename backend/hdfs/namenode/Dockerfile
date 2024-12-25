# Utilisation de l'image de base Hadoop
FROM apache/hadoop:3.3.5

# Définir l'utilisateur et les variables d'environnement
USER root
ENV HADOOP_HOME=/opt/hadoop

# Copier les fichiers nécessaires pour le Namenode
COPY ./start-hdfs.sh /start-hdfs.sh

# Définir le répertoire de travail
WORKDIR /opt/hadoop

# Exécuter le script de démarrage du Namenode
CMD ["/bin/bash", "/start-hdfs.sh"]
