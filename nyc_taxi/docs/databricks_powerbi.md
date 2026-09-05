
##### You must have Power BI version 2.99.563.0 or above installed.
* acceder via cle token : dapic77bf70405330025cb66255fbcc70a57

* Server hostname : dbc-8c847397-3c66.cloud.databricks.com
* Workspace ID : 7474654582545410
* HTTP path : /sql/1.0/warehouses/f9e12649f3131654
* JDBC URL : jdbc:databricks://dbc-8c847397-3c66.cloud.databricks.com:443/default;transportMode=http;ssl=1;AuthMech=3;httpPath=/sql/1.0/warehouses/f9e12649f3131654;
* OAuth URL : https://dbc-8c847397-3c66.cloud.databricks.com/oidc

* Exposer tes tables Gold dans un workspace Databricks cloud, 
* idéalement avec Unity Catalog + SQL Warehouse


#### gold_fact_trips
* periode
* trip_date
* date
* PULocationID
* DOLocationID
* trip_duration_minute
* trip_distance
* passenger_count
* fare_amount
* tip_amount
* total_amount
* payment_type

PULocationID  = Pickup Location
DOLocationID  = Dropoff Location


`````text
                 Databricks
                     │
          ┌──────────┴──────────┐
          │                     │
     Delta Tables          SQL Warehouse
          │                     │
          └─────────────────────┘
                     │
                     │ Databricks Connector
                     ▼
                 Power BI
                     │
              ┌──────┴──────┐
              │             │
           Power Query   Modèle BI
              │             │
              └──────┬──────┘
                     ▼
                Dashboard
`````


`````text
NYC Taxi Parquet
      ↓
   BRONZE
      ↓
   SILVER
      ↓
    GOLD
      ↓
Databricks SQL Warehouse
      ↓
    Power BI
      ↓
 Modèle en étoile
      ↓
 Mesures DAX
      ↓
 Dashboard NYC Taxi
`````



`````text
                 DATA LAKE
                    │
             NYC Taxi Parquet
                    │
                    ▼
             ┌──────────────┐
             │    BRONZE    │
             │ raw taxi     │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │    SILVER    │
             │ cleaned data │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │     GOLD     │
             │              │
             │ fact_trips   │
             │ dim_date     │
             │ dim_location │
             │ kpi_daily    │
             └──────┬───────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ Databricks SQL        │
        │ Warehouse             │
        └───────────┬───────────┘
                    │
             Azure Databricks
              Power BI connector
                    │
                    ▼
             ┌──────────────┐
             │   Power BI   │
             │ Semantic     │
             │ Model       │
             └──────┬───────┘
                    │
                    ▼
               Dashboard
`````


`````text
`````



`````text
`````


`````text
`````


`````text
`````


`````text
`````


`````text
`````

`````text
`````

`````text
`````