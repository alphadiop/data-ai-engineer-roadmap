# Power BI Dashboard – NYC Taxi

## 1. Objectif

Le dashboard Power BI permet d'exploiter les données préparées dans la couche Gold du projet NYC Taxi.

L'objectif est de fournir une vue synthétique et interactive permettant d'analyser :

* l'activité des taxis ;
* le chiffre d'affaires ;
* le volume de trajets ;
* les distances parcourues ;
* les performances temporelles ;
* les zones de départ et d'arrivée ;
* les principaux indicateurs opérationnels.

Le dashboard est alimenté à partir des tables analytiques Databricks.

---

# 2. Architecture BI

```text
                    Databricks
                        |
                        v
              +-------------------+
              |    Gold Layer     |
              +-------------------+
                 |             |
                 v             v
        gold_fact_trips   gold_kpi_daily
                 |             |
                 +------+------+
                        |
                        v
                 Power BI Model
                        |
             +----------+----------+
             |                     |
             v                     v
         dim_date            dim_location
             |                     |
             +----------+----------+
                        |
                        v
                  Power BI Report
```

---

# 3. Sources de données

Le modèle Power BI utilise principalement les tables suivantes :

```text
nyc_taxi.gold.gold_fact_trips
nyc_taxi.gold.gold_kpi_daily
nyc_taxi.ref.dim_date
nyc_taxi.ref.dim_location
```

## gold_fact_trips

Table de faits principale.

Elle contient les informations détaillées des trajets.

Granularité :

```text
1 ligne = 1 trajet
```

---

## gold_kpi_daily

Table d'agrégation journalière.

Granularité :

```text
1 ligne = 1 journée
```

Elle permet notamment d'optimiser les visualisations basées sur les indicateurs quotidiens.

---

## dim_date

Dimension temporelle utilisée pour les analyses :

* année ;
* mois ;
* jour ;
* trimestre ;
* semaine ;
* jour de la semaine.

---

## dim_location

Dimension géographique permettant d'analyser :

* les zones de départ ;
* les zones d'arrivée ;
* les Borough ;
* les zones de service.

---

# 4. Modèle en étoile

Le modèle Power BI suit une architecture en étoile.

```text
                    dim_date
                       |
                       |
                       v
dim_location ---> gold_fact_trips
                       |
                       |
                       v
                gold_kpi_daily
```

La table `gold_fact_trips` constitue le cœur du modèle analytique.

---

# 5. Relations

## Relation Date

```text
dim_date[date_key]
        |
        | 1
        |
        | *
        v
gold_fact_trips[date_key]
```

Cardinalité :

```text
1 → *
```

---

## Relation Localisation Pickup

```text
dim_location[LocationID]
        |
        | 1
        |
        | *
        v
gold_fact_trips[PULocationID]
```

Cette relation permet d'analyser les zones de prise en charge.

---

## Relation Localisation Dropoff

Pour les zones d'arrivée, le modèle utilise également `DOLocationID`.

Selon la configuration Power BI retenue, cette relation peut être implémentée avec :

* une deuxième copie logique de la dimension ;
* ou une relation inactive activée dans les mesures DAX.

Exemple conceptuel :

```text
dim_location_pickup
        |
        v
PULocationID

dim_location_dropoff
        |
        v
DOLocationID
```

Cette approche permet de conserver des relations simples et d'éviter les ambiguïtés dans le modèle.

---

# 6. Mesures DAX

Les mesures suivantes constituent une base pour le dashboard.

## Chiffre d'affaires

```DAX
Chiffre_Affaires =
SUM(gold_fact_trips[total_amount])
```

---

## Nombre de trajets

```DAX
Nombre_Trajets =
COUNTROWS(gold_fact_trips)
```

---

## Distance moyenne

```DAX
Distance_Moyenne =
AVERAGE(gold_fact_trips[trip_distance])
```

---

## Durée moyenne

```DAX
Duree_Moyenne =
AVERAGE(gold_fact_trips[trip_duration_minute])
```

---

## Pourboire moyen

```DAX
Pourboire_Moyen =
AVERAGE(gold_fact_trips[tip_percent])
```

---

## Tarif moyen

```DAX
Tarif_Moyen =
AVERAGE(gold_fact_trips[fare_amount])
```

---

# 7. Page 1 – Executive Overview

## Objectif

Cette page fournit une vision globale de l'activité.

### KPI Cards

Les cartes recommandées sont :

```text
+------------------+------------------+
| Chiffre          | Nombre de        |
| d'affaires       | trajets          |
+------------------+------------------+
| Distance         | Durée            |
| moyenne          | moyenne          |
+------------------+------------------+
```

### Visuels

Prévoir notamment :

* évolution du chiffre d'affaires dans le temps ;
* évolution du nombre de trajets ;
* répartition des trajets par jour ;
* principaux indicateurs.

### Filtres

Filtres recommandés :

* année ;
* mois ;
* période ;
* Borough ;
* zone ;
* date.

---

# 8. Page 2 – Revenue & Trips

## Objectif

Analyser l'évolution de l'activité et du chiffre d'affaires.

### Indicateurs

* Chiffre d'affaires ;
* Nombre de trajets ;
* Tarif moyen ;
* Pourboire moyen.

### Visualisations

#### Chiffre d'affaires dans le temps

Graphique en ligne :

```text
Axe X : Date
Axe Y : Chiffre d'affaires
```

#### Nombre de trajets

Graphique en ligne ou en colonnes :

```text
Axe X : Date
Axe Y : Nombre de trajets
```

---

# 9. Page 3 – Geographic Analysis

## Objectif

Analyser la répartition géographique des trajets.

### Analyses

* Top zones de départ ;
* Top zones d'arrivée ;
* Borough les plus fréquentés ;
* nombre de trajets par zone ;
* chiffre d'affaires par zone.

### Visuel recommandé

Bar chart :

```text
Zone
  |
  | █████████████
  | █████████
  | ███████
  | █████
  +----------------
       Nombre de trajets
```

---

# 10. Page 4 – Time Analysis

## Objectif

Identifier les tendances temporelles.

### Analyses

* trajets par heure ;
* trajets par jour de semaine ;
* trajets par mois ;
* chiffre d'affaires par mois ;
* durée moyenne par heure.

### Exemple

```text
Heure
00  ███
01  ██
02  █
...
08  █████████
09  ███████████
...
18  █████████████
```

---

# 11. Page 5 – Pickup / Dropoff Analysis

## Objectif

Analyser les flux entre les zones.

### Indicateurs

* zone de départ ;
* zone d'arrivée ;
* nombre de trajets ;
* chiffre d'affaires ;
* distance moyenne.

### Analyse

Identifier les principales combinaisons :

```text
Pickup Zone
     ↓
Dropoff Zone
     ↓
Nombre de trajets
```

Un tableau ou une matrice peut être utilisé :

| Pickup | Dropoff | Trips |
| ------ | ------- | ----- |
| Zone A | Zone B  | ...   |
| Zone B | Zone C  | ...   |
| Zone C | Zone A  | ...   |

---

# 12. Filtres et interactions

Les filtres principaux peuvent être placés dans un panneau latéral.

```text
Filters
-------------------------
Year
Month
Period
Borough
Pickup Zone
Dropoff Zone
-------------------------
```

Les interactions entre les visuels doivent permettre de filtrer dynamiquement les autres graphiques.

---

# 13. Navigation

Une navigation par boutons peut être mise en place :

```text
[Overview]
[Revenue]
[Geography]
[Time Analysis]
[Pickup / Dropoff]
```

Cette navigation facilite l'utilisation du rapport.

---

# 14. Performance

Le modèle doit privilégier les tables Gold plutôt que de charger directement les données Silver ou Bronze.

Principe :

```text
Bronze
  ↓
Silver
  ↓
Gold
  ↓
Power BI
```

Les agrégations journalières présentes dans `gold_kpi_daily` peuvent être utilisées pour les graphiques nécessitant uniquement des données agrégées.

---

# 15. Actualisation des données

Le pipeline Databricks met à jour les tables analytiques.

Le flux cible est :

```text
Nouvelles données
      ↓
Pipeline Databricks
      ↓
Bronze
      ↓
Silver
      ↓
Gold
      ↓
Power BI
      ↓
Refresh
```

Le mécanisme exact d'actualisation Power BI sera documenté une fois la configuration finale mise en place.

---

# 16. Contrôles de cohérence

Avant de publier les indicateurs, les volumes peuvent être contrôlés entre les différentes couches.

Exemple :

```text
Bronze
4 591 845 lignes

        ↓ contrôle qualité

Silver
4 284 519 lignes

        ↓ transformation

Gold Fact
4 284 519 lignes
```

Les volumes d'exécution sont également disponibles dans :

```text
nyc_taxi.audit.audit_row_count
```

---

# 17. Indicateurs principaux

Le dashboard doit permettre de répondre notamment aux questions suivantes :

### Activité

* Combien de trajets ont été réalisés ?
* Quelle est l'évolution du volume de trajets ?

### Revenus

* Quel est le chiffre d'affaires ?
* Quelle est son évolution ?
* Quel est le tarif moyen ?

### Géographie

* Quelles sont les principales zones de départ ?
* Quelles sont les principales zones d'arrivée ?
* Quels Borough concentrent le plus de trajets ?

### Temps

* Quelles sont les heures les plus actives ?
* Quels jours sont les plus actifs ?
* Comment l'activité évolue-t-elle au cours de l'année ?

### Trajets

* Quelle est la distance moyenne ?
* Quelle est la durée moyenne ?
* Quels sont les principaux flux Pickup → Dropoff ?

---

# 18. Architecture cible

```text
                         Databricks
                             |
                 +-----------+-----------+
                 |                       |
                 v                       v
          gold_fact_trips        gold_kpi_daily
                 |                       |
                 +-----------+-----------+
                             |
                 +-----------+-----------+
                 |                       |
                 v                       v
             dim_date             dim_location
                 |                       |
                 +-----------+-----------+
                             |
                             v
                        Power BI
                             |
            +----------------+----------------+
            |                |                |
            v                v                v
         Overview        Geography        Time Analysis
            |
            v
       Revenue Analysis
            |
            v
     Pickup / Dropoff
```

---

# 19. Évolutions possibles

Une fois le dashboard initial terminé, les évolutions pourront inclure :

* comparaison MoM ;
* évolution YoY ;
* KPI dynamiques ;
* drill-through ;
* tooltips personnalisés ;
* bookmarks ;
* navigation avancée ;
* analyse des flux Pickup → Dropoff ;
* cartes géographiques ;
* alertes sur les indicateurs ;
* intégration avec les mécanismes d'actualisation Databricks.

---

# 20. Statut du Dashboard

Cette documentation constitue la **spécification initiale du dashboard Power BI**.

Les éléments suivants seront ajustés après construction :

* noms exacts des colonnes ;
* relations finales du modèle ;
* mesures DAX ;
* nombre de pages ;
* choix des visualisations ;
* filtres ;
* navigation ;
* mécanisme d'actualisation ;
* performances.

Le dashboard final devra rester cohérent avec le modèle de données réellement déployé dans Databricks.
