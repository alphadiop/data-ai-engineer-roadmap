# Tableau de bord Power BI

## 1. Objectif

Le modèle Power BI exploite les tables analytiques Gold et les dimensions de référence afin de suivre l'activité NYC Taxi selon les filtres et périodes sélectionnés.

Les visuels précis, leurs titres, la mise en page et les interactions doivent être décrits à partir du fichier Power BI réel. Ce document formalise les tables et mesures connues sans supposer de visuel qui n'a pas été vérifié.

## 2. Sources du modèle

Tables connues dans le modèle :
- `gold_fact_trips` : faits au niveau du trajet ;
- `gold_kpi_daily` : indicateurs agrégés par jour ;
- `dim_date` : dimension de dates ;
- `dim_location` : dimension de localisation.

Dans l'environnement décrit, les tables sont exposées sous le catalogue `nyc_taxi`, avec les schémas `gold` et `ref`. Vérifier les sources réellement configurées dans le modèle sémantique Power BI.

## 3. Relations

Le modèle comprend des relations de type un-à-plusieurs entre les dimensions et les faits :
- `dim_date` vers les faits par une clé de date ;
- `dim_location` vers les faits par la localisation de prise en charge.

Les noms exacts des colonnes de jointure, le sens du filtre et la relation éventuelle avec `gold_kpi_daily` doivent être vérifiés dans le modèle Power BI. Ne pas inventer une colonne `date_key` ou une autre clé si elle n'est pas présente.

## 4. Mesures DAX connues

Les mesures suivantes ont été utilisées ou décrites dans le projet. Les noms de mesures peuvent être adaptés à ceux du fichier Power BI.

### Nombre de trajets

```dax
Nombre_Trajets =
COUNTROWS(gold_fact_trips)
```

Cette mesure compte les lignes de `gold_fact_trips` dans le contexte de filtre courant. Elle représente le nombre de trajets si la granularité de la table est bien une ligne par trajet.

### Chiffre d'affaires

```dax
Chiffre_Affaires =
SUM(gold_fact_trips[total_amount])
```

Cette mesure additionne `total_amount` dans le contexte de filtre courant.

### Distance moyenne

```dax
Distance_Moyenne =
AVERAGE(gold_fact_trips[trip_distance])
```

### Durée moyenne

```dax
Duree_Moyenne_Minute =
AVERAGE(gold_fact_trips[trip_duration_minute])
```

### Pourboire moyen

```dax
Pourboire_Moyen =
AVERAGE(gold_fact_trips[tip_amount])
```

### Tarif moyen

```dax
Tarif_Moyen =
AVERAGE(gold_fact_trips[fare_amount])
```

Une mesure utilisant `tip_percent` a également été évoquée. Sa définition et sa présence dans la table doivent être vérifiées avant de documenter une formule DAX définitive.

## 5. Filtres et période sélectionnée

Une mesure telle que `Nombre_Trajets` est évaluée dans le contexte de filtre du rapport. Si un segment de dates est correctement relié à `gold_fact_trips`, la mesure peut refléter la période sélectionnée.

Ce comportement dépend du modèle et des relations effectives. La documentation ne doit pas inventer les noms de segments, les colonnes de calendrier ou les relations. Si la question concerne une période donnée, vérifier :
1. quelle colonne alimente le segment de dates ;
2. quelle relation propage le filtre vers les faits ;
3. si la mesure est affectée par le filtre ou le neutralise explicitement ;
4. si les données de la période sont présentes dans le modèle.

## 6. SQL et DAX

La formule SQL :

```sql
SELECT COUNT(*)
FROM nyc_taxi.gold.gold_fact_trips;
```

s'exécute sur la table dans le moteur SQL. La formule DAX `COUNTROWS(gold_fact_trips)` s'évalue dans le modèle Power BI et tient compte du contexte de filtre du rapport. Il ne faut pas présenter une expression DAX comme une requête SQL ni l'inverse.

## 7. Vérifications avant publication

- Confirmer le nom exact de chaque mesure dans le rapport.
- Confirmer le nom des colonnes et les types.
- Vérifier les relations et leur cardinalité.
- Tester les filtres de dates et de localisation.
- Comparer les valeurs du rapport avec des requêtes SQL de contrôle.
- Documenter les visuels et leur interprétation à partir du rapport réel.
