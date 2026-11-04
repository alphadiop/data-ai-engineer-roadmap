# Transformations Silver — NYC Taxi

## 1. Objectif

La couche Silver transforme les données Bronze en données structurées, typées et contrôlées.

Elle prépare les courses de taxi pour les agrégations de la couche Gold et le calcul des indicateurs métier.

Les transformations comprennent :
- La standardisation des types.
- Le calcul de la durée des courses.
- La création d'une clé de date.
- Le calcul du pourcentage de pourboire.
- Le calcul de la vitesse moyenne.
- L'ajout de caractéristiques calendaires.
- L'application des règles qualité.
- L'application du schéma cible.

## 2. Standardisation des types

Les colonnes sont converties vers des types adaptés aux calculs et à l'analyse.

| Colonne | Type cible | Utilisation |
|---|---|---|
| `tpep_pickup_datetime` | TIMESTAMP | Date et heure de départ |
| `tpep_dropoff_datetime` | TIMESTAMP | Date et heure d'arrivée |
| `passenger_count` | BIGINT | Nombre de passagers |
| `payment_type` | TINYINT | Code du moyen de paiement |
| `trip_distance` | DECIMAL(19,5) | Distance de la course |
| `fare_amount` | DECIMAL(19,5) | Montant de la course hors pourboire |
| `tip_amount` | DECIMAL(19,5) | Montant du pourboire |
| `total_amount` | DECIMAL(19,5) | Montant total de la course |

Les types décimaux permettent de contrôler la précision des montants et des distances.

## 3. Durée de la course

**Colonne :** `trip_duration_minute`

**Formule :**

`trip_duration_minute = (dropoff_timestamp - pickup_timestamp) / 60`

Dans l'implémentation PySpark, la différence est calculée en secondes avec `unix_timestamp`, puis divisée par 60. Le résultat est arrondi à trois décimales.

**Utilité métier :** mesurer la durée de chaque course et détecter les durées nulles, négatives ou anormalement longues.

## 4. Clé de date

**Colonne :** `trip_date`

**Formule :**

`trip_date = year(pickup_datetime) * 10000 + month(pickup_datetime) * 100 + dayofmonth(pickup_datetime)`

Exemple : le 15 avril 2025 devient `20250415`.

**Utilité métier :** disposer d'une clé numérique au format AAAAMMJJ pour faciliter les jointures et les agrégations journalières.

La clé est calculée à partir de la date de prise en charge du client.

## 5. Pourcentage de pourboire

**Colonne :** `tip_percent`

**Formule :**

`tip_percent = (tip_amount / fare_amount) * 100`

Le résultat est arrondi à deux décimales uniquement lorsque `fare_amount > 0`. Sinon, la valeur est NULL.

**Utilité métier :** analyser le poids du pourboire par rapport au tarif de la course.

Ce ratio ne représente pas le pourcentage du montant total, mais celui du tarif `fare_amount`.

## 6. Vitesse moyenne

**Colonne :** `average_speed`

**Formule :**

`average_speed = trip_distance / (trip_duration_minute / 60)`

Le résultat est arrondi à deux décimales lorsque `trip_duration_minute > 0`. Sinon, la valeur est NULL.

**Unité :** miles par heure (mph), si `trip_distance` est exprimée en miles et la durée en minutes.

**Utilité métier :** analyser les vitesses moyennes et repérer des courses potentiellement atypiques.

Cette vitesse est une moyenne calculée sur toute la durée de la course ; elle ne correspond pas à une vitesse instantanée.

## 7. Caractéristiques calendaires
Les caractéristiques suivantes sont dérivées de `tpep_pickup_datetime`.

#### pickup_hour
* Extrait l'heure de la journée, de 0 à 23
* Exemple : 18 h → 18. Utile pour analyser les heures de pointe

#### pickup_day_of_week
* Retourne le jour de la semaine : dimanche = 1, lundi = 2, ..., samedi = 7
* Exemple : jeudi → 5. Utile pour comparer les jours ouvrés et les week-ends

#### pickup_month
* Extrait le mois, de 1 à 12
* Exemple : avril → 4. Utile pour analyser la saisonnalité

#### pickup_year
* Extrait l'année sur quatre chiffres
* Exemple : 2025 → 2025. Utile pour les comparaisons annuelles



| Colonne | Formule | Signification |
|---|---|---|
| `pickup_hour` | `hour(pickup_datetime)` | Heure de prise en charge, de 0 à 23 |
| `pickup_day_of_week` | `dayofweek(pickup_datetime)` | Jour de la semaine, de 1 à 7 |
| `pickup_month` | `month(pickup_datetime)` | Mois, de 1 à 12 |
| `pickup_year` | `year(pickup_datetime)` | Année de prise en charge |

Dans Spark, `dayofweek()` renvoie 1 pour dimanche, 2 pour lundi, et ainsi de suite jusqu'à 7 pour samedi.

**Utilité métier :** faciliter l'analyse des volumes de courses selon l'heure, le jour de la semaine, le mois et l'année.

## 8. Règles qualité

Une course est conservée si toutes les conditions suivantes sont satisfaites :

1. `trip_duration_minute > 0`
2. `trip_duration_minute < 1400`
3. `trip_distance > 0`
4. `total_amount > 0`

La durée doit donc être strictement positive et inférieure à 1 400 minutes, soit 23 heures et 20 minutes.

La distance et le montant total doivent également être strictement positifs.

Les lignes ne satisfaisant pas l'ensemble des conditions sont rejetées de la sortie Silver.

Les valeurs nulles ne satisfont pas ces filtres et sont donc exclues.

**Limite :** ces règles ne contrôlent pas toutes les anomalies possibles. Elles ne valident notamment pas explicitement la cohérence entre les montants détaillés, la distance, les zones de départ et d'arrivée ou les catégories de paiement.

## 9. Rapport qualité

Le pipeline mesure :
- Le nombre de lignes en entrée.
- Le nombre de lignes après les filtres qualité.
- Le nombre de lignes rejetées.
- Le taux de rejet.

**Formules :**

`rejected_rows = rows_before - rows_after`

`rejection_rate = rejected_rows / rows_before * 100`

Le taux de rejet est calculé uniquement lorsque le nombre de lignes en entrée est supérieur à zéro.

Ces indicateurs permettent de suivre l'évolution de la qualité des données entre les exécutions du pipeline.

## 10. Application du schéma cible

Après les transformations et les filtres qualité, `SchemaManager.apply_schema()` applique le schéma défini dans le fichier JSON correspondant à `silver_nyc_taxi`.

Le fichier est localisé avec `PathManager`, selon le type de taxi du contexte.

Le DataFrame final est affecté à `context.df_silver` et le nombre de lignes est enregistré dans `context.row_count["silver"]`.

## 11. Résultat attendu
La couche Silver fournit un jeu de données typé, enrichi de caractéristiques temporelles et d'indicateurs par course, filtré selon les règles qualité définies.
Ces données servent de base aux agrégations de la couche Gold, notamment les analyses de volumes, de chiffre d'affaires, de distance et de fréquentation des zones de taxi.
**Note technique :** les formules décrivent la logique métier du code. Les unités, les types et les conventions doivent être vérifiés avec le schéma réel des données sources.


## Résumé
Ma méthode cast_columns() standardise les types de données à l'entrée de la couche Silver.
Je définis les types cibles dans un dictionnaire, puis je parcours les colonnes du DataFrame.
Si une colonne figure dans le dictionnaire, j'applique un cast ; sinon, je la conserve sans modification explicite.
J'utilise select() avec une compréhension de liste pour réaliser cette transformation de manière dynamique,
sans supprimer les colonnes qui ne nécessitent pas de conversion.
Le point fort de cette approche est qu'elle évite d'écrire un cast distinct pour chaque colonne
tout en conservant les autres champs du jeu de données.

Dans la couche Silver de mon pipeline NYC Taxi, j'enrichis les données Bronze avec des caractéristiques métier et temporelles.
Je calcule la durée des courses à partir des timestamps, je construis une clé de date,
je calcule le pourcentage de pourboire en sécurisant la division par zéro, puis j'extrais les composantes calendaires du départ.
J'utilise withColumns() pour ajouter ces expressions au DataFrame Spark dans une seule transformation logique.
Ces attributs facilitent ensuite les contrôles qualité et les agrégations dans la couche Gold

Je calcule une vitesse moyenne dérivée à partir de la distance et de la durée de chaque course.
Je convertis d'abord la durée en heures, puis je divise la distance par cette durée.
Je protège le calcul avec une condition sur la durée strictement positive et j'arrondis le résultat à deux décimales.
Cette métrique enrichit la couche Silver et peut aussi contribuer à détecter des anomalies de transport.


la vitesse en mph se multiplie par 1.60934 pour obtenir la vitesse en km/h.
Par exemple, 12 mph correspondent à environ 19,31 km/h.
