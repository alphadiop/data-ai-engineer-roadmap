# Pipeline de données NYC Taxi

## 1. Objectif

Le pipeline transforme les données source NYC Taxi en tables prêtes pour l'analyse. Il est conçu autour des couches Bronze, Silver et Gold et s'appuie sur un exécuteur central `PipelineRunner`.

## 2. Paramètres

Les paramètres connus de l'exécution comprennent :
- `env` : environnement d'exécution ; la configuration Databricks utilise `databricks` comme valeur.
- `taxi_type` : type de taxi traité ; la configuration observée utilise `yellow`.
- `periode` : période de traitement au format utilisé par le projet, par exemple `202504`.

Les valeurs autorisées, valeurs par défaut et validations doivent être lues dans la configuration et le code courant.

## 3. Étapes fonctionnelles

### 3.1 Initialisation

L'environnement et les paramètres sont préparés. Les ressources et configurations nécessaires sont initialisées avant les traitements.

### 3.2 Chargement des références

Le pipeline prépare ou charge les données de référence utilisées par les traitements. Les sources et règles exactes sont définies par les modules correspondants.

### 3.3 Bronze — ingestion

Les fichiers source sont chargés dans la zone brute. Le chemin Databricks connu est :

`/Volumes/nyc_taxi/bronze/raw_files/`

La couche Bronze sert de point d'entrée traçable pour les données sources. Le détail du format et de la stratégie d'ingestion doit être confirmé dans le code.

### 3.4 Silver — nettoyage et enrichissement

Les données sont standardisées et contrôlées avant d'être exposées aux consommateurs analytiques. Les transformations peuvent inclure la validation des valeurs, le typage, la déduplication et l'enrichissement ; seules les règles réellement implémentées doivent être considérées comme actives.

La table connue est `nyc_taxi.silver.silver_nyc_taxi`.

### 3.5 Gold — données analytiques

La couche Gold prépare les données à usage métier :
- `nyc_taxi.gold.gold_fact_trips` : faits au niveau du trajet ;
- `nyc_taxi.gold.gold_kpi_daily` : agrégats d'indicateurs quotidiens.

La logique exacte des agrégations et la liste des KPI sont détaillées dans [business_rules.md](business_rules.md).

### 3.6 Audit et maintenance

Le projet comprend des tables d'audit, dont `nyc_taxi.audit.audit_row_count` et `nyc_taxi.audit.audit_load`. Elles servent au suivi des volumes et des chargements. Les statuts, compteurs, conditions d'échec et opérations de maintenance doivent être confirmés dans les modules d'audit et de maintenance.

Le mécanisme `ALREADY_LOADED` a été utilisé pour traiter le cas d'une période déjà chargée. Son comportement exact (ignorer, arrêter ou autre) doit être confirmé dans le code courant.

## 4. Orchestration

Le point d'entrée historique du pipeline est `src/jobs/pipeline_runner_jobs_bundles.py`. Le `PipelineRunner` coordonne les étapes fonctionnelles. Le projet dispose également d'un DAG Airflow nommé `nyc_taxi_airflow`, qui déclenche le pipeline dans l'environnement local.

Dans Databricks, le bundle identifié porte le nom `nyc_taxi_pipeline` et définit un job associé. Le déploiement doit être piloté par la configuration versionnée du bundle.

## 5. CI/CD

Le flux de livraison prévu et partiellement mis en place est :

1. Développer et versionner le code dans Git.
2. Exécuter les tests automatisés avec GitHub Actions.
3. Valider le bundle Databricks.
4. Déployer les ressources avec le bundle lorsque cette étape est activée dans le workflow.
5. Exécuter le job Databricks et vérifier les résultats et l'audit.

La présence d'une étape dans cette description ne garantit pas qu'elle est déjà activée dans chaque branche ou workflow. Consulter `.github/workflows/` et `databricks.yml` pour l'état courant.

## 6. Contrôles à documenter

Pour chaque étape, préciser à partir du code :
- les entrées et sorties ;
- les règles de qualité ;
- les volumes lus, écrits, rejetés ou ignorés ;
- le comportement en cas de doublon ou de relance ;
- les logs et informations d'audit ;
- les erreurs bloquantes et non bloquantes ;
- les tests associés.

## 7. Diagnostic des volumes

Des exécutions ont montré les volumes suivants :

| Période | Bronze | Silver |
|---|---:|---:|
| `202504` | 3 970 553 | 3 776 318 |
| `202505` | 4 591 845 | 4 284 519 |

La différence entre Bronze et Silver peut refléter les règles de transformation, de qualité ou de filtrage. Il ne faut pas qualifier automatiquement toute différence de « rejet » sans rapprocher les compteurs et les règles d'exclusion du pipeline.
