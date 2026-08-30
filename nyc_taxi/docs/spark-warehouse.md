
* metastore_db = catalogue
* spark-warehouse = données

```text
spark-warehouse/
│
├── audit.db/
│   ├── audit_load/
│   └── audit_row_count/
│
├── silver.db/
│   └── silver_nyc_taxi/
│
├── gold.db/
│   ├── gold_fact_trips/
│   ├── gold_dim_date/
│   └── gold_kpi_daily/
│
└── ref.db/
```


