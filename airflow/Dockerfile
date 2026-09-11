
FROM apache/airflow:3.0.6
USER root

# ==========================================================
# Java 17
# ==========================================================
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# ==========================================================
# Retour utilisateur Airflow
# ==========================================================
USER airflow

# ==========================================================
# PySpark + Delta Lake + YAML
# ==========================================================
RUN pip install --no-cache-dir \
    pyspark==3.5.1 \
    delta-spark==3.2.0 \
    PyYAML

