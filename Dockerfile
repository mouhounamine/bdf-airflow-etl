FROM quay.io/astronomer/astro-runtime:12.6.0

USER root

# Installer pour faire tourner les jobs Spark
# Install OpenJDK-17
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jdk ant && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/
RUN export JAVA_HOME