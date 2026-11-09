# Architecture technique

## 1. Vue d'ensemble

Le projet NYC Taxi suit une architecture Medallion sur Databricks, avec des traitements Python/PySpark, des tables Delta Lake, des mécanismes d'audit et des consommateurs analytiques. Un assistant RAG distinct permet d'interroger la documentation du projet.

## 2. Flux de données

```text
Fichiers NYC Taxi
      |
      v
Bronze : données brutes
      |
      v
Silver : données nettoyées et enrichies
      |
      v
Gold : faits et indicateurs analytiques
      |
      +------> Audit et suivi des volumes
      |
      v
Power BI
```

Le flux de déploiement est distinct du flux de données :

```text
Dépôt GitHub
    |
    v
GitHub Actions : tests et contrôles
    |
    v
Databricks Asset Bundles : validation / déploiement
    |
    v
Databricks Job / Workflow
    |
    v
PipelineRunner
```

Airflow est également utilisé dans l'environnement du projet pour orchestrer le lancement du `PipelineRunner`. Le rôle exact de chaque orchestrateur doit rester explicite dans la configuration : éviter de présenter deux orchestrateurs comme maîtres d'un même déclenchement sans l'avoir configuré ainsi.

## 3. Architecture Medallion

### Bronze

La couche Bronze conserve les données ingérées au plus près des fichiers sources. Le chemin de stockage connu dans l'environnement Databricks est :

`/Volumes/nyc_taxi/bronze/raw_files/`

Le format, les conventions de nommage et la stratégie de conservation doivent être confirmés dans le code d'ingestion et la configuration du catalogue.

### Silver

La table de référence connue est `nyc_taxi.silver.silver_nyc_taxi`. Cette couche contient les données nettoyées et enrichies destinées aux traitements analytiques. Les règles exactes de validation, de déduplication, de typage et de rejet sont définies par le code du pipeline et doivent être documentées à partir de celui-ci.

### Gold

Les principales tables connues sont :

- `nyc_taxi.gold.gold_fact_trips` : table analytique au niveau du trajet, selon le modèle actuel.
- `nyc_taxi.gold.gold_kpi_daily` : agrégats d'indicateurs quotidiens.

La granularité exacte, les colonnes et les clés doivent être vérifiées dans le schéma déployé.

### Audit

Les tables d'audit connues incluent `nyc_taxi.audit.audit_row_count` et `nyc_taxi.audit.audit_load`. Elles servent au suivi des volumes et des chargements. Le détail des colonnes, statuts et règles de réconciliation doit être vérifié dans le code.

## 4. Composants Python

Le projet utilise un exécuteur central de pipeline, `PipelineRunner`, qui coordonne les principales étapes. Le point d'entrée historique identifié est `src/jobs/pipeline_runner_jobs_bundles.py`.

Les responsabilités mentionnées dans l'implémentation comprennent l'initialisation de l'environnement, le chargement des données de référence, les traitements Bronze/Silver/Gold, le chargement des sorties et la maintenance. Les noms exacts des classes et l'ordre effectif doivent être contrôlés dans la version courante du code avant toute modification de cette documentation.

Le pipeline reçoit notamment des paramètres comme l'environnement, le type de taxi et la période. Le type de taxi observé dans la configuration de bundle est `yellow`; un exemple de période est `202504`.

## 5. Orchestration et industrialisation

- **Databricks Jobs/Workflows** : exécution des traitements sur Databricks.
- **Databricks Asset Bundles** : définition et déploiement des ressources Databricks à partir du dépôt.
- **GitHub Actions** : automatisation des tests et contrôles CI/CD.
- **Airflow** : orchestration du pipeline dans l'environnement local du projet.

Les étapes réellement actives doivent être vérifiées dans les fichiers de workflow et de configuration. Une possibilité future ou une recommandation d'architecture ne doit pas être confondue avec une fonctionnalité déployée.

## 6. Assistant RAG

Le RAG est un composant documentaire séparé du pipeline de données. Il charge des fichiers Markdown, segmente leur contenu, calcule des embeddings, indexe les vecteurs avec FAISS, récupère les passages les plus similaires à une question et transmet ce contexte à Ollama/Qwen pour générer une réponse.

La source documentaire prévue est `nyc_taxi/documentation/`. Le chemin effectivement utilisé doit être configuré explicitement dans le code de chargement afin que les anciennes notes ne soient pas indexées par accident.

## 7. Points de vérification

Avant de modifier l'architecture, vérifier dans le dépôt :
- les chemins et noms de ressources Databricks réels ;
- le catalogue et les schémas utilisés par chaque environnement ;
- l'ordre des étapes de `PipelineRunner` ;
- les orchestrateurs activement utilisés ;
- les mécanismes de déploiement et de contrôle qualité réellement présents.
