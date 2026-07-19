#### Semaine 1
- [ ] DataFrames
- [ ] Read CSV
- [ ] Write Delta
- [ ] Filter
- [ ] Select
- [ ] GroupBy

#### Semaine 2
- [ ] Catalogs
- [ ] Schemas
- [ ] Tables
- [ ] Volumes
- [ ] SQL

#### Semaine 3
- [ ] Bronze / Silver / Gold
- [ ] Delta Lake
- [ ] Time Travel
- [ ] OPTIMIZE : tous les jours
- [ ] VACUUM : toutes les semaines
- [ ] Time Travel
- [ ] Rollback
- [ ] Historique
- [ ] Tests unitaires
- [ ] Auto Loader
- [ ] Structured Streaming
- [ ] Unity Catalog (permissions)
- [ ] Delta Live Tables (ou Lakeflow)
- [ ] CI/CD Databricks avec Git et Asset Bundles


#### Semaine 4
- [ ] Databricks Workflows (Jobs)
- [ ] Workflows
- [ ] Paramètres
- [ ] Monitoring

#### Semaine 5+
- [ ] Streaming
- [ ] Kafka
- [ ] ML
- [ ] Agents AI

#### Analyse de données de Taxi New York
- [ ] Télecharger les données
- [ ] Crééer une table DELTA


##### Catalog
* 🧱 Catalog → training
* 📁 Schema → training.bronze
* 📁 Schema → training.silver
* 📁 Schema → training.gold
* 📦 Volume → sales_volume
* 📄 Fichier → /Volumes/training/bronze/sales_volume/orders.csv

##### compétences
✅ Catalog  
✅ Schema  
✅ Volume  
✅ Spark DataFrame  
✅ Read CSV  
✅ Write Delta  
✅ Read Delta  
✅ saveAsTable  
✅ Filter  
✅ Select  
✅ GroupBy  
✅ OrderBy  
✅ SQL  
✅ Delta Lake  
✅ Time Travel  
✅ Data Versioning  
✅ OPTIMIZE  
✅ VACUUM  
✅ Jobs  
✅ Bronze / Silver / Gold  

##### Les objects
- [ ] CreateTables
- [ ] DeltaManager
- [ ] AuditManager
- [ ] PipelineRunner


- [ ] construire un chemin dans un volume
- [ ] vérifier si le chemin existe
- [ ] télecharger uniquement s'il est absent
- [ ] lire avec Spark directement depuis le volume
- [ ] Ordre classique : Bronze -> Silver -> Gold -> OPTIMIZE
- [ ] Ordre classique : OPTIMIZE -> VACUUM DRY RUN -> VACUUM
- [ ] toutes les semaines -> VACUUM
- [ ] Pipeline = chargement
- [ ] Maintenance = nettoyage
- [ ] Bronze -> Silver -> Gold -> SUCCESS -> Maintenance -> Audit

- [ ] Définir un schema json des données afin de contrôler le type
- [ ] charger le schema et le transformer structure de creation de table delta
- [ ] Maintenance = nettoyage

### Documentation du projet
#### Télécharger un fichier mensuel
- [ ] choisir une année et un mois donnés
- [ ] vérifier la présence du fichier en local
- [ ] télécharger que si le fichier est absent
- [ ] enregistrer le fichier télécharger en local
- [ ] lire le fichier télécharger avec spark Python
- [ ] ajouter une période afin de suivre les données : {annee}{mois}
- [ ] appliquer des partitions par périodes si necessaires
- [ ] appliquer l'optimisation sur ces partitions 
- [ ] vérifier les partitions avant de lancer l'OPTIMIZE
- [ ] réaliser les traitements nécessaires
- [ ] vérifier que la période concernée n'a pas été chargé
- [ ] charger les données dans Delta
- [ ] charger la table audit -> tracer les chargements
- [ ] analyser avec Power BI

#### Enregistrer le fichier télécharger en local
- [ ] créer un catalogue
- [ ] créer un schema
- [ ] créer un volume
- [ ] 


#### Traitement réalisé
- [ ] 
- [ ] 
- [ ] 
- [ ] 
#### Contrainte pour chager une période
- [ ] 
- [ ] 
- [ ] 
- [ ] 
#### Audit


