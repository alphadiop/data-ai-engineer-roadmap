
##### You must have Power BI version 2.99.563.0 or above installed.
* acceder via cle token : dapic77bf70405330025cb66255fbcc70a57

* Server hostname : dbc-8c847397-3c66.cloud.databricks.com
* Workspace ID : 7474654582545410
* HTTP path : /sql/1.0/warehouses/f9e12649f3131654
* JDBC URL : jdbc:databricks://dbc-8c847397-3c66.cloud.databricks.com:443/default;transportMode=http;ssl=1;AuthMech=3;httpPath=/sql/1.0/warehouses/f9e12649f3131654;
* OAuth URL : https://dbc-8c847397-3c66.cloud.databricks.com/oidc


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