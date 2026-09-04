### Spark Manager
```` text
Créer Spark
   ↓
Configurer Delta
   ↓
Configurer warehouse
   ↓
Configurer metastore
   ↓
Retourner spark
````

```` text
CatalogManager
repair_local_metastore()
     ↓
scanner spark-warehouse
     ↓
retrouver audit / silver / gold / ref
     ↓
réenregistrer les tables
````