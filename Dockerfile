FROM quay.io/astronomer/astro-runtime:12.6.0

USER root

RUN apt-get update && \
    apt-get install -y build-essential krb5-user libkrb5-dev

RUN pip install apache-airflow-providers-apache-hdfs


# Installer pour faire tourner les jobs Spark
# Installer OpenJDK-17
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jdk ant && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Définir JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64/
RUN export JAVA_HOME
