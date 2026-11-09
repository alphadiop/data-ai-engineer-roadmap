# Modèle de données

## 1. Principes

Le modèle analytique sépare les données nettoyées, les faits destinés à l'analyse, les indicateurs agrégés, les dimensions de référence et les tables d'audit.

Les noms ci-dessous sont ceux connus dans le projet. Les types, contraintes, colonnes complètes et clés doivent être vérifiés dans le schéma Databricks réellement déployé. Ne pas créer une colonne ou une relation simplement parce qu'elle serait courante dans un modèle en étoile.

## 2. Tables connues

| Schéma | Table | Rôle connu | Granularité connue ou attendue |
|---|---|---|---|
| `silver` | `silver_nyc_taxi` | Données nettoyées et enrichies | Une ligne par trajet conservé, à confirmer |
| `gold` | `gold_fact_trips` | Faits analytiques des trajets | Une ligne par trajet selon le modèle courant |
| `gold` | `gold_kpi_daily` | KPI agrégés par jour | Une ligne par jour, à confirmer par clé et schéma |
| `ref` | `dim_date` | Dimension de dates | Une ligne par date, à confirmer |
| `ref` | `dim_location` | Dimension de localisation | Une ligne par localisation, à confirmer |
| `audit` | `audit_row_count` | Suivi de volumes / comptages | Selon le niveau de journalisation |
| `audit` | `audit_load` | Suivi des chargements | Selon le niveau de journalisation |

Le catalogue utilisé dans les exemples est `nyc_taxi`. Les noms complets observés sont par exemple `nyc_taxi.gold.gold_fact_trips` et `nyc_taxi.silver.silver_nyc_taxi`.

## 3. Colonnes de trajet connues

Les colonnes suivantes ont été observées dans le modèle de données du projet :

- `periode`
- `trip_date` ou `date` selon la table ou l'étape — le nom exact de chaque table doit être vérifié
- `PULocationID`
- `DOLocationID`
- `trip_duration_minute`
- `trip_distance`
- `passenger_count`
- `fare_amount`
- `tip_amount`
- `total_amount`
- `payment_type`

D'autres colonnes peuvent exister. Cette liste ne remplace pas le schéma complet. En particulier, ne pas supposer l'existence de `trip_id`, `date_key` ou d'autres clés sans inspection explicite.

## 4. Relations du modèle Power BI

Le modèle utilisé dans Power BI comprend les tables `gold_fact_trips`, `gold_kpi_daily`, `dim_date` et `dim_location`.

Les relations suivantes ont été décrites dans le modèle actuel :
- la dimension de dates filtre les faits selon une relation de type un-à-plusieurs ;
- la dimension de localisation filtre les faits selon une relation de type un-à-plusieurs, notamment par localisation de prise en charge.

Les colonnes exactes de jointure et le sens de filtrage doivent être lus dans le modèle Power BI. Ne pas inventer de clé de relation. Les relations entre `dim_date` et `gold_kpi_daily` doivent également être confirmées dans le modèle effectif.

## 5. Vérification du schéma

Avant de documenter ou d'utiliser une colonne dans une requête SQL :
1. Inspecter le schéma de la table dans Databricks.
2. Vérifier le nom exact, le type et la signification de la colonne.
3. Vérifier la granularité de la table.
4. Vérifier les clés et relations.
5. Mettre à jour cette documentation après validation.

Exemple de requête d'inspection, à exécuter dans l'environnement Databricks approprié :

```sql
DESCRIBE TABLE nyc_taxi.gold.gold_fact_trips;
```

Pour compter les lignes d'une table, si le nom de table est confirmé :

```sql
SELECT COUNT(*) AS nombre_trajets
FROM nyc_taxi.gold.gold_fact_trips;
```

`COUNT(*)` compte les lignes retournées. Il ne compte pas seulement les valeurs non nulles d'une colonne particulière.

## 6. Volumes observés

Des comptages d'exécution ont été observés pour deux périodes :

| Période | Bronze | Silver |
|---|---:|---:|
| `202504` | 3 970 553 | 3 776 318 |
| `202505` | 4 591 845 | 4 284 519 |

Ces chiffres sont des observations d'exécution, pas des constantes du modèle. Ils doivent être accompagnés de la version du pipeline et des règles de filtrage si on les utilise pour analyser les rejets ou la qualité.

## 7. Règle de documentation

Ne documenter comme fait établi que ce qui est confirmé par le code, le schéma de la table, le modèle Power BI ou un test reproductible. Les noms de colonnes incertains doivent être marqués « à vérifier » plutôt que complétés par intuition.
