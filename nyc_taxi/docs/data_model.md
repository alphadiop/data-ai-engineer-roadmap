# Modèle de Données – NYC Taxi

## Objectif

Le modèle de données a été conçu pour faciliter :

* l'analyse des trajets de taxis ;
* le suivi des indicateurs métier ;
* la création de tableaux de bord Power BI ;
* l'optimisation des performances analytiques.

Le modèle repose sur une architecture en étoile (Star Schema), couramment utilisée dans les plateformes décisionnelles modernes.

---

# Vue d'Ensemble

```text
                    +------------------+
                    |    dim_date      |
                    +------------------+
                             |
                             |
                             |
+------------------+         |         +------------------+
|   dim_location   |---------+---------| gold_fact_trips  |
+------------------+                   +------------------+
                                                 |
                                                 |
                                                 |
                                         +------------------+
                                         | gold_kpi_daily   |
                                         +------------------+
```

---

# Tables de Référence

## ref.dim_date

### Description

Dimension temporelle utilisée pour toutes les analyses calendaires.

### Clé primaire

```text
date_key
```

### Colonnes principales

| Colonne     | Description                    |
| ----------- | ------------------------------ |
| date_key    | Clé de date au format YYYYMMDD |
| trip_date   | Date complète                  |
| year        | Année                          |
| month       | Mois                           |
| day         | Jour                           |
| day_name    | Nom du jour                    |
| week_number | Numéro de semaine              |
| quarter     | Trimestre                      |

### Exemple

| date_key | trip_date  |
| -------- | ---------- |
| 20250401 | 2025-04-01 |
| 20250402 | 2025-04-02 |

---

## ref.dim_location

### Description

Dimension géographique issue du fichier Taxi Zone Lookup.

### Clé primaire

```text
LocationID
```

### Colonnes principales

| Colonne      | Description         |
| ------------ | ------------------- |
| LocationID   | Identifiant de zone |
| Borough      | Arrondissement      |
| Zone         | Nom de la zone      |
| service_zone | Zone de service     |

### Exemple

| LocationID | Borough   | Zone                  |
| ---------- | --------- | --------------------- |
| 236        | Manhattan | Upper East Side North |
| 161        | Manhattan | Midtown Center        |

---

# Table de Faits

## gold.gold_fact_trips

### Description

Table principale contenant les trajets enrichis.

Chaque ligne représente un trajet de taxi.

### Granularité

```text
1 ligne = 1 trajet
```

### Clé métier

Combinaison :

```text
VendorID
tpep_pickup_datetime
tpep_dropoff_datetime
PULocationID
DOLocationID
```

### Colonnes principales

| Colonne               | Description             |
| --------------------- | ----------------------- |
| VendorID              | Fournisseur du trajet   |
| tpep_pickup_datetime  | Date de prise en charge |
| tpep_dropoff_datetime | Date de dépose          |
| passenger_count       | Nombre de passagers     |
| trip_distance         | Distance parcourue      |
| fare_amount           | Tarif                   |
| tip_amount            | Pourboire               |
| total_amount          | Montant total           |
| PULocationID          | Zone de départ          |
| DOLocationID          | Zone d'arrivée          |
| periode               | Période YYYYMM          |

---

## Colonnes Calculées

### trip_duration_minute

Durée du trajet en minutes.

```text
dropoff - pickup
```

---

### tip_percent

Pourcentage de pourboire.

```text
tip_amount / fare_amount
```

---

### average_speed

Vitesse moyenne.

```text
trip_distance / durée
```

---

### pickup_hour

Heure de départ.

Exemple :

```text
14
```

---

### pickup_day_of_week

Jour de la semaine.

Exemple :

```text
Monday
Tuesday
Wednesday
```

---

# Table de KPI

## gold.gold_kpi_daily

### Description

Table agrégée contenant les indicateurs journaliers.

### Granularité

```text
1 ligne = 1 jour
```

### Colonnes principales

| Colonne         | Description        |
| --------------- | ------------------ |
| trip_date       | Date               |
| nb_trips        | Nombre de trajets  |
| revenue         | Chiffre d'affaires |
| avg_distance    | Distance moyenne   |
| avg_duration    | Durée moyenne      |
| avg_tip_percent | Pourboire moyen    |
| periode         | Période YYYYMM     |

---

# Relations Power BI

## Relation Date

```text
dim_date.date_key
        |
        |
        v
gold_fact_trips.date_key
```

Cardinalité :

```text
1 → *
```

---

## Relation Localisation Pickup

```text
dim_location.LocationID
        |
        |
        v
gold_fact_trips.PULocationID
```

Cardinalité :

```text
1 → *
```

---

## Relation Localisation Dropoff

```text
dim_location.LocationID
        |
        |
        v
gold_fact_trips.DOLocationID
```

Cardinalité :

```text
1 → *
```

---

# Partitionnement Delta

Les tables volumineuses sont partitionnées par :

```text
periode
```

Exemple :

```text
202501
202502
202503
202504
202505
```

Avantages :

* réduction du volume lu ;
* meilleures performances Spark ;
* rechargement incrémental.

---

# Volumétrie Observée

Exemple de chargements réalisés.

| Période | Bronze    | Silver    |
| ------- | --------- | --------- |
| 202504  | 3 970 553 | 3 776 318 |
| 202505  | 4 591 845 | 4 284 519 |

Les écarts correspondent aux contrôles qualité appliqués dans la couche Silver.

---

# Cas d'Usage Métier

Le modèle permet notamment :

### Analyse du chiffre d'affaires

```sql
SUM(total_amount)
```

---

### Nombre de trajets

```sql
COUNT(*)
```

---

### Distance moyenne

```sql
AVG(trip_distance)
```

---

### Pourboire moyen

```sql
AVG(tip_percent)
```

---

### Analyse géographique

* Top zones de départ
* Top zones d'arrivée
* Répartition par Borough

---

### Analyse temporelle

* Tendances journalières
* Tendances mensuelles
* Analyse par heure de la journée

---

# Consommation dans Power BI

Les tables recommandées pour Power BI sont :

```text
gold_fact_trips
dim_date
dim_location
gold_kpi_daily
```

Cette structure permet de construire un modèle décisionnel performant, évolutif et conforme aux bonnes pratiques de la modélisation analytique.
