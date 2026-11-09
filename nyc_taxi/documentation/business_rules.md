# Règles métier et indicateurs

## 1. Principes

Les indicateurs sont calculés à partir des tables Gold et consommés notamment dans Power BI. La formule doit être choisie selon la granularité de la table et la définition métier de l'indicateur.

Les exemples ci-dessous sont fondés sur les tables et colonnes connues du projet. Avant de publier un indicateur, vérifier que la colonne existe dans la table concernée et que les filtres correspondent au besoin métier.

## 2. Indicateurs connus

| Indicateur | Définition de travail | Formule SQL |
|---|---|---|
| Nombre de trajets | Nombre de lignes de la table de faits, si une ligne représente un trajet | `COUNT(*)` |
| Chiffre d'affaires | Somme de `total_amount`, sous réserve de la définition métier retenue | `SUM(total_amount)` |
| Distance moyenne | Moyenne de `trip_distance` | `AVG(trip_distance)` |
| Durée moyenne | Moyenne de `trip_duration_minute` | `AVG(trip_duration_minute)` |
| Pourboire moyen | Moyenne de `tip_amount` | `AVG(tip_amount)` |
| Tarif moyen | Moyenne de `fare_amount` | `AVG(fare_amount)` |

Le projet a également utilisé une colonne `tip_percent` dans les mesures Power BI. Sa formule de calcul et sa disponibilité dans la table Gold doivent être vérifiées dans le code et le schéma avant d'en donner une définition métier précise.

## 3. Exemples SQL

### Nombre de lignes / trajets

Si `gold_fact_trips` contient une ligne par trajet :

```sql
SELECT COUNT(*) AS nombre_trajets
FROM nyc_taxi.gold.gold_fact_trips;
```

`COUNT(*)` compte toutes les lignes retournées, même si certaines colonnes de ces lignes contiennent `NULL`.

### Chiffre d'affaires

```sql
SELECT SUM(total_amount) AS chiffre_affaires
FROM nyc_taxi.gold.gold_fact_trips;
```

Cette formule additionne les valeurs non nulles de `total_amount`. Elle ne définit pas à elle seule les règles d'exclusion des remboursements, montants négatifs ou enregistrements invalides.

### Distance moyenne

```sql
SELECT AVG(trip_distance) AS distance_moyenne
FROM nyc_taxi.gold.gold_fact_trips;
```

`AVG` ignore les valeurs `NULL`. Les unités et règles de filtrage doivent être documentées avec la donnée source.

### Durée moyenne

```sql
SELECT AVG(trip_duration_minute) AS duree_moyenne_minute
FROM nyc_taxi.gold.gold_fact_trips;
```

Cette requête suppose que `trip_duration_minute` existe dans la table Gold et représente une durée en minutes. Vérifier le schéma et la logique de calcul avant de considérer l'exemple comme contractuel.

## 4. Indicateurs dans le temps

Pour analyser les indicateurs par jour ou par période, utiliser les champs temporels et relations réellement présents dans le modèle. Le modèle Power BI comprend une dimension `dim_date`, mais le nom exact de la clé de date ne doit pas être deviné.

Ne pas inventer de table de calendrier, de colonne de date, de relation ou de filtre. Pour répondre à une question sur « la période sélectionnée », préciser si l'on parle d'une mesure Power BI affectée par un segment de dates ou d'une requête SQL filtrée par une période explicite.

## 5. SQL et DAX : ne pas confondre

- SQL : `COUNT(*)` compte les lignes d'un résultat SQL.
- DAX : `COUNTROWS(gold_fact_trips)` compte les lignes de la table dans le contexte de filtre DAX.

Ces expressions sont proches dans leur intention, mais appartiennent à deux langages et à deux contextes d'exécution différents.

## 6. Règles métier à confirmer

Les éléments suivants ne doivent pas être déduits uniquement du nom des colonnes :
- définition officielle du chiffre d'affaires ;
- traitement des montants nuls ou négatifs ;
- définition d'un trajet valide ;
- filtres sur la distance ou la durée ;
- traitement des doublons ;
- définition et calcul de `tip_percent` ;
- règles de comparaison entre périodes.

Ils doivent être renseignés à partir du code de transformation, des exigences métier du projet et des mesures utilisées dans Power BI.
