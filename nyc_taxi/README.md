

# NYC Taxi Data Engineering Project

## Overview

This project demonstrates the design and implementation of a modern Data Engineering pipeline using:

* Python
* PySpark
* Delta Lake
* Databricks
* Databricks Asset Bundles
* GitHub Actions
* Apache Airflow
* Docker
* Medallion Architecture (Bronze / Silver / Gold)

The pipeline processes NYC Yellow Taxi trip data and transforms raw datasets into curated analytical tables ready for reporting and business intelligence.

---

## Architecture

```text
NYC Taxi Dataset
        |
        v
+------------------+
| Bronze Layer     |
| Raw Parquet Data |
+------------------+
        |
        v
+------------------+
| Silver Layer     |
| Data Cleaning    |
| Quality Rules    |
| Enrichments      |
+------------------+
        |
        v
+------------------+
| Gold Layer       |
| Fact Tables      |
| KPI Tables       |
| Dimensions       |
+------------------+
        |
        v
Power BI / Analytics
```

---

## Technologies

| Category         | Technologies             |
| ---------------- | ------------------------ |
| Language         | Python                   |
| Big Data         | Spark / PySpark          |
| Storage          | Delta Lake               |
| Cloud Platform   | Databricks               |
| Orchestration    | Airflow                  |
| CI/CD            | GitHub Actions           |
| Deployment       | Databricks Asset Bundles |
| Containerization | Docker                   |
| Version Control  | Git                      |

---

## Project Structure

```text
nyc_taxi/
│
├── src/
│   ├── audit/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── jobs/
│   ├── common/
│   └── quality/
│
├── config/
│
├── schema/
│
├── tests/
│
├── logs/
│
├── airflow/
│
├── databricks.yml
│
└── requirements.txt
```

---

## Data Model

### Silver

| Table           |
| --------------- |
| silver_nyc_taxi |

### Reference

| Table        |
| ------------ |
| dim_date     |
| dim_location |

### Gold

| Table           |
| --------------- |
| gold_fact_trips |
| gold_kpi_daily  |

### Audit

| Table           |
| --------------- |
| audit_load      |
| audit_row_count |

---

## Pipeline Features

### Bronze Layer

* Read NYC Taxi parquet files
* Automatic file management
* Incremental processing by period

### Silver Layer

* Data quality checks
* Data type standardization
* Derived business columns
* Trip duration calculation
* Average speed calculation
* Tip percentage calculation

### Gold Layer

* Fact table generation
* Daily KPI generation
* Date dimension generation

### Audit Layer

* Pipeline execution tracking
* Success and failure monitoring
* Row count monitoring
* Processing duration tracking

---

## Running Locally

```bash
wsl
cd /mnt/d/data-ai-engineer-roadmap/nyc_taxi
source ~/spark4_env/bin/activate
python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles --env local --periode 202504 --taxi_type yellow
python -m nyc_taxi.src.jobs.run_pipeline --env local --taxi_type yellow --periode 202505
python -m nyc_taxi.src.jobs.run_pipeline \
  --env local \
  --taxi_type yellow \
  --periode 202505
  
```

---

```PowerShell
powershell
conda activate spark_local
cd D:\data-ai-engineer-roadmap
python -m nyc_taxi.src.jobs.run_pipeline --env local --taxi_type yellow --periode 202505
```


## Running with Airflow

```bash
docker compose up -d
```

Open:

```text
http://localhost:8080
```

Run DAG:

```text
nyc_taxi_airflow
```

---

## Databricks Deployment

Validate bundle:

```bash
databricks bundle validate
```

Deploy bundle:

```bash
databricks bundle deploy
```

Run job:

```bash
databricks bundle run nyc_taxi_job \
  --params taxi_type=yellow,periode=202505
```

---

## CI/CD

GitHub Actions automatically:

* installs dependencies
* executes unit tests
* validates Docker configuration
* validates Databricks bundles
* deploys Databricks assets

---

## Data Quality Controls

Implemented controls:

* Null checks
* Business rule validation
* Schema validation
* Duplicate detection
* Audit monitoring

---

## Example KPIs

* Number of trips
* Revenue
* Average fare
* Average trip distance
* Average trip duration
* Tip percentage
* Daily trends

---

## Future Improvements

* Streaming ingestion with Auto Loader
* Delta Live Tables
* Unity Catalog governance
* Data Quality Expectations
* MLflow integration
* RAG and GenAI analytics assistant

---

## Author

**Alpha Oumar DIOP**

Data Engineer | Databricks | Spark | Delta Lake

GitHub Portfolio Project developed to demonstrate end-to-end Data Engineering skills using modern cloud and big data technologies.
