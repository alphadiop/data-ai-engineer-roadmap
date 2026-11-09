# NYC Taxi — Projet Data Engineering et assistant RAG

## 1. Présentation

Ce projet met en œuvre une chaîne de traitement de données NYC Taxi avec Python, PySpark, Delta Lake et Databricks.
Il transforme des fichiers de trajets en tables structurées destinées à l'analyse, puis expose la documentation technique du projet à un prototype d'assistant RAG (Retrieval-Augmented Generation).

Le projet couvre deux volets complémentaires :

- **Data Engineering** : ingestion, nettoyage, transformation, calcul d'indicateurs, audit et orchestration.
- **Assistant RAG** : recherche de passages pertinents dans la documentation Markdown, puis génération d'une réponse à partir du contexte récupéré.

## 2. Objectifs

- Industrialiser un pipeline de données réutilisable par période et type de taxi.
- Structurer les traitements selon l'architecture Medallion : Bronze, Silver et Gold.
- Produire des données analytiques et des indicateurs pour Power BI.
- Tracer les traitements et faciliter le diagnostic des chargements.
- Permettre de poser des questions techniques sur le projet via un assistant RAG local.

## 3. Technologies

| Domaine | Technologies connues |
|---|---|
| Traitement | Python, PySpark, SQL |
| Stockage analytique | Delta Lake |
| Plateforme | Databricks |
| Orchestration | Databricks Jobs/Workflows et Airflow dans l'environnement de projet |
| CI/CD | GitHub Actions, Databricks Asset Bundles |
| Visualisation | Power BI, DAX |
| Assistant documentaire | Python, Sentence Transformers, FAISS, Ollama, modèle Qwen2.5 3B |
| Tests | pytest et scripts de test du RAG |

Les versions précises et les dépendances de chaque environnement doivent être consultées dans les fichiers de configuration du dépôt.

## 4. Architecture logique

1. Des fichiers source NYC Taxi sont ingérés dans la couche Bronze.
2. La couche Silver nettoie et enrichit les données.
3. La couche Gold expose une table de faits et une table d'indicateurs quotidiens.
4. Des tables d'audit permettent de suivre les traitements et les volumes.
5. Power BI exploite les tables analytiques.
6. Le RAG charge les documents Markdown, les découpe en passages, calcule des embeddings, indexe les vecteurs dans FAISS et transmet les passages retrouvés au modèle local pour générer une réponse.

Voir [architecture.md](architecture.md), [pipeline.md](pipeline.md) et [rag.md](rag.md).

## 5. Modèle analytique

Les tables connues dans le catalogue `nyc_taxi` sont notamment :

- `silver.silver_nyc_taxi`
- `gold.gold_fact_trips`
- `gold.gold_kpi_daily`
- `audit.audit_row_count`
- `audit.audit_load`
- `ref.dim_date`
- `ref.dim_location`

Les noms de colonnes, types, clés et relations doivent être vérifiés dans le schéma réellement déployé. Voir [data_model.md](data_model.md).

## 6. Exécution et déploiement
Le dépôt comprend un exécuteur de pipeline Python et une configuration de bundle Databricks.
Le pipeline peut être appelé depuis différents contextes prévus par le projet, dont Databricks et Airflow.
GitHub Actions sert à exécuter les contrôles automatisés et à préparer le déploiement selon la configuration CI/CD.
Les commandes exactes dépendent de l'environnement courant.
Consulter les fichiers de configuration du dépôt et [deployment](deployment.md) dans l'ancienne documentation si ce document reste maintenu.
Ce dossier de documentation n'est pas un substitut aux fichiers exécutables de configuration.


## 7. Documentation
- [Architecture technique](architecture.md)
- [Modèle de données](data_model.md)
- [Pipeline Bronze/Silver/Gold](pipeline.md)
- [Règles métier et KPI](business_rules.md)
- [Tableau de bord Power BI](powerbi_dashboard.md)
- [Assistant RAG](rag.md)


## 8. Limites et principes de fiabilité
Cette documentation distingue les éléments connus du projet des éléments qui doivent être confirmés dans le code ou dans le catalogue Databricks.
Une table, une colonne, une jointure ou une formule ne doit pas être présentée comme existante sans vérification.

Le prototype RAG doit s'abstenir de produire une réponse technique lorsqu'aucun passage pertinent ne documente suffisamment la question.
Les scores de similarité FAISS ne constituent pas, à eux seuls, une preuve de vérité.
