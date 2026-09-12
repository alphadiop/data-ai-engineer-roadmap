* power Shell
* wsl
* cd /mnt/d/data-ai-engineer-roadmap
* source ~/spark4_env/bin/activate
* python test_run_pipeline.py


python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles     --env docker     --periode 202501     --taxi_type yellow
python -m nyc_taxi.src.jobs.run_pipeline {'env':'docker', "periode":202501, "taxi_type":"yellow"}
python -m nyc_taxi.src.jobs.run_pipeline {'env':'docker', "periode":202501, "taxi_type":"yellow"}

# Mise en place d'Airflow — Projet NYC Taxi

## 1. Objectif
L'objectif est d'intégrer **Airflow** au projet NYC Taxi afin d'orchestrer l'exécution du pipeline de Data Engineering.

Le pipeline doit pouvoir fonctionner dans plusieurs environnements :

* Local / WSL
* Docker / Airflow
* Databricks

L'objectif est de conserver le même code métier et de faire varier principalement la configuration de l'environnement.

Architecture cible :

```text
Git
 │
 ▼
GitHub
 │
 ▼
Airflow
 │
 ▼
Docker
 │
 ▼
NYC Taxi Pipeline
 │
 ▼
Spark / Delta Lake
```

---
# 2. Comprendre WSL, Docker et Airflow
## 2.1 WSL

WSL signifie :

> Windows Subsystem for Linux

Il permet d'exécuter un environnement Linux directement sous Windows.

Notre projet Windows :

```text
D:\data-ai-engineer-roadmap
```

est accessible depuis WSL avec :

```text
/mnt/d/data-ai-engineer-roadmap
```

Exemple :

| Environnement | Chemin                                 |
| ------------- | -------------------------------------- |
| Windows       | `D:\data-ai-engineer-roadmap\data`     |
| WSL           | `/mnt/d/data-ai-engineer-roadmap/data` |
| Docker        | `/opt/data`                            |
| Databricks    | `/Volumes/nyc_taxi/...`                |

---

# 3. Architecture du projet

Sur Windows :

```text
D:\data-ai-engineer-roadmap
│
├── airflow/                 # orchestration Airflow
│   ├── dags/
│   ├── logs/
│   ├── plugins/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── nyc_taxi/                # code métier du pipeline
│   ├── src/
│   ├── resources/
│   └── ...
│
├── data/                    # données
│
└── config/                  # configuration
```

Dans WSL :

```text
/mnt/d/data-ai-engineer-roadmap
```

---

# 4. Architecture Docker

Docker Desktop exécute les conteneurs nécessaires à Airflow.

```text
                         WINDOWS
                            │
                            ▼
                           WSL
                            │
                            ▼
                    Docker Desktop
                            │
              ┌─────────────┴─────────────┐
              │                           │
         Airflow containers          PostgreSQL
              │
              ├── Scheduler
              ├── API Server
              └── DAG
                    │
                    ▼
             PipelineRunner
                    │
                    ▼
             NYC Taxi / Spark
```

Le fichier :

```text
airflow/docker-compose.yml
```

décrit notamment les services :

```text
postgres
airflow-init
airflow-apiserver
airflow-scheduler
```

---

# 5. Rôle du Dockerfile

Le `Dockerfile` sert à construire l'image Docker utilisée par Airflow.

Il permet notamment d'installer les dépendances nécessaires au projet.

Conceptuellement :

```text
Dockerfile
    │
    ▼
Docker Image
    │
    ▼
Docker Container
```

`docker compose up` permet ensuite de démarrer les services définis dans `docker-compose.yml`.

---

# 6. Les volumes Docker

Docker possède son propre système de fichiers.

Il faut donc explicitement monter les dossiers du projet dans les conteneurs.

Exemple :

```yaml
volumes:
  - ../config:/opt/airflow/config
  - ../data:/opt/data
  - ../nyc_taxi:/opt/airflow/nyc_taxi
```

La syntaxe :

```text
SOURCE:DESTINATION
```

signifie :

```text
../config
     │
     ▼
/opt/airflow/config
```

Depuis le projet Airflow :

```text
D:\data-ai-engineer-roadmap\config
```

est donc accessible dans Docker sous :

```text
/opt/airflow/config
```

De même :

```text
D:\data-ai-engineer-roadmap\data
```

est accessible dans Docker sous :

```text
/opt/data
```

et :

```text
D:\data-ai-engineer-roadmap\nyc_taxi
```

est accessible sous :

```text
/opt/airflow/nyc_taxi
```

---

# 7. Vérifier l'environnement WSL

Activer l'environnement Python utilisé pour Spark local :

```bash
source ~/spark4_env/bin/activate
```

Puis se placer à la racine du projet :

```bash
cd /mnt/d/data-ai-engineer-roadmap
```

---

# 8. Démarrer Airflow

Se placer dans le projet Airflow :

```bash
cd /mnt/d/data-ai-engineer-roadmap/airflow
```

Vérifier la structure :

```bash
find . -maxdepth 2 -type f | sort
```

Vérifier la configuration Docker :

```bash
docker compose config
```

Démarrer les services :

```bash
docker compose up -d
```

Vérifier leur état :

```bash
docker compose ps
```

---

# 9. Accéder à un conteneur Airflow

La commande :

```bash
docker compose exec airflow-scheduler bash
```

signifie :

> Exécuter `bash` à l'intérieur du conteneur `airflow-scheduler` déjà démarré.

On peut ensuite utiliser des commandes Linux directement dans le conteneur :

```bash
ls -lah /opt
```

```bash
ls -lah /opt/data
```

```bash
ls -lah /opt/data/ref
```

Pour sortir du conteneur :

```bash
exit
```

---

# 10. Vérifier les volumes Docker

Avant de chercher une erreur dans le code, vérifier que les fichiers sont réellement accessibles depuis Docker.

## Vérifier la configuration du volume

Depuis :

```text
/mnt/d/data-ai-engineer-roadmap/airflow
```

exécuter :

```bash
docker compose config | grep -A5 -B5 "/opt/data"
```

## Vérifier le conteneur

```bash
docker inspect airflow-airflow-apiserver-1 | grep "/opt/data"
```

## Entrer dans le conteneur

```bash
docker exec -it airflow-airflow-apiserver-1 bash
```

ou :

```bash
docker exec -it airflow-airflow-scheduler-1 bash
```

Puis :

```bash
ls -lah /opt/data
```

```bash
ls -lah /opt/data/ref
```

---

# 11. Vérifier les données de référence

Le fichier de référence utilisé par le pipeline est :

```text
taxi_zone_lookup.csv
```

Recherche dans Docker :

```bash
find /opt/data -name "taxi_zone_lookup.csv" 2>/dev/null
```

Vérification plus précise :

```bash
python -c "
from pathlib import Path

p = Path('/opt/data/ref/taxi_zone_lookup.csv')

print('Existe :', p.exists())
print('Fichier :', p.is_file())
print('Taille  :', p.stat().st_size if p.exists() else 'N/A')
"
```

Cette vérification permet de distinguer :

```text
problème de code
```

d'un :

```text
problème de montage Docker
```

---

# 12. Vérifier la configuration du pipeline

La configuration est chargée avec :

```python
load_config(
    "variable_environnement",
    env
)
```

L'environnement Docker doit utiliser :

```text
config["docker"]
```

et non :

```text
config["local"]
```

Pour inspecter la configuration :

```bash
python -c "
from nyc_taxi.src.utils.config.load_config import load_config

config = load_config(
    'variable_environnement',
    'docker'
)

print('TYPE CONFIG :', type(config))

print()
print('CONFIG :')
print(config)

print()
print('DOCKER CONFIG :')
print(config['docker'])

print()
print('REF_PATH :')
print(config['docker']['ref_path'])
"
```

Vérifier directement le chemin :

```bash
python -c "
from nyc_taxi.src.utils.config.load_config import load_config
from pathlib import Path

config = load_config(
    'variable_environnement',
    'docker'
)

ref_path = config['docker']['ref_path']

print('ref_path =', ref_path)
print('Existe =', Path(ref_path).exists())
"
```

---

# 13. Gestion des chemins selon l'environnement

Le projet utilise plusieurs environnements.

## Local

Un chemin Windows :

```text
D:/data-ai-engineer-roadmap/...
```

peut être converti en WSL :

```text
/mnt/d/data-ai-engineer-roadmap/...
```

## Docker

Les chemins Docker restent inchangés :

```text
/opt/data
/opt/airflow
```

## Databricks

Les chemins Unity Catalog restent inchangés :

```text
/Volumes/nyc_taxi/...
```

La règle est donc :

```text
local
  D:/...
    ↓
  /mnt/d/...

docker
  /opt/...
    ↓
  /opt/...

databricks
  /Volumes/...
    ↓
  /Volumes/...
```

---

# 14. Paramétrage du pipeline

Pour l'exécution Airflow actuelle :

```python
env = "docker"
taxi_type = "yellow"
periode = 202501
```

Ce qui signifie :

```text
Environnement : Docker
Type de taxi  : Yellow Taxi
Période       : janvier 2025
```

---

# 15. Lancement manuel du PipelineRunner

Avant d'utiliser Airflow, le pipeline peut être lancé directement avec Python.

Depuis :

```text
/mnt/d/data-ai-engineer-roadmap
```

on peut utiliser :

```bash
python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
    --env local \
    --periode 202504 \
    --taxi_type yellow
```

Cette commande lance directement :

```text
PipelineRunner
```

avec :

```text
env       = local
periode   = 202504
taxi_type = yellow
```

---

# 16. Architecture Airflow

Le rôle des fichiers est séparé.

```text
nyc_taxi_airflow.py
        │
        │ orchestration
        ▼
run_pipeline.py
        │
        │ point d'entrée
        ▼
PipelineRunner
        │
        ├── EnvironmentSetup
        ├── ReferenceDataLoader
        ├── UberBronze
        ├── UberSilver
        ├── UberGold
        ├── DataLoader
        └── MaintenanceJob
```

## Responsabilités

### `nyc_taxi_airflow.py`

Responsable de l'orchestration Airflow :

```text
DAG
Task
Schedule
```

### `run_pipeline.py`

Responsable du lancement du pipeline :

```text
Spark
Logger
Steps
PipelineRunner
```

### `PipelineRunner`

Responsable de l'exécution séquentielle des étapes.

### Les Steps

Responsables du traitement métier :

```text
EnvironmentSetup
ReferenceDataLoader
UberBronze
UberSilver
UberGold
DataLoader
MaintenanceJob
```

---

# 17. Vérifier que le DAG est visible par Airflow

Vérifier les fichiers présents :

```bash
docker compose exec airflow-scheduler ls -la /opt/airflow/dags
```

Vérifier la liste des DAG :

```bash
docker compose exec airflow-scheduler airflow dags list
```

Vérifier les erreurs d'import :

```bash
docker compose exec airflow-scheduler airflow dags list-import-errors
```

Si aucune erreur n'est présente, le DAG est correctement importé.

---

# 18. Vérifier le DAG

Afficher la structure du DAG :

```bash
docker compose exec airflow-scheduler airflow dags show nyc_taxi_airflow
```

Cette commande permet de vérifier que :

```text
nyc_taxi_airflow
```

est bien enregistré et contient la task :

```text
run_nyc_taxi_pipeline
```

---

# 19. Premier problème : module `nyc_taxi` introuvable

Erreur rencontrée :

```text
ModuleNotFoundError: No module named 'nyc_taxi'
```

Pourtant, le projet était bien présent dans :

```text
/opt/airflow/nyc_taxi
```

Vérification :

```bash
docker compose exec airflow-scheduler bash
```

Puis :

```bash
ls -lah /opt/airflow/nyc_taxi
```

et :

```bash
ls -lah /opt/airflow/nyc_taxi/src
```

---

# 20. Vérifier le `PYTHONPATH`

Dans le conteneur :

```bash
python -c "import sys; print('\n'.join(sys.path))"
```

Le problème était que :

```text
/opt/airflow
```

n'était pas présent dans le chemin Python.

Or notre projet est situé ici :

```text
/opt/airflow/nyc_taxi
```

Python doit donc pouvoir trouver :

```text
/opt/airflow
```

pour importer :

```python
import nyc_taxi
```

---

# 21. Correction du PYTHONPATH

Dans `docker-compose.yml` :

```yaml
environment:
  PYTHONPATH: /opt/airflow
```

Après modification :

```bash
docker compose up -d
```

Puis vérifier :

```bash
docker compose exec airflow-scheduler bash
```

```bash
echo $PYTHONPATH
```

Test d'import :

```bash
python -c "
from nyc_taxi.src.jobs.pipeline_runner_jobs_bundles import PipelineRunner
print('IMPORT OK')
"
```

Résultat attendu :

```text
IMPORT OK
```

---

# 22. Deuxième problème : `steps = None`

Une fois l'import corrigé, une nouvelle erreur est apparue :

```text
TypeError: 'NoneType' object is not iterable
```

L'erreur se produisait dans :

```python
for step in self.steps:
```

dans :

```text
src/jobs/pipeline_runner_jobs_bundles.py
```

Le problème était dans la construction du :

```python
PipelineRunner
```

Le constructeur contient :

```python
def __init__(
    self,
    spark,
    env,
    taxi_type="yellow",
    periode=None,
    logger=None,
    steps=None
):
```

Donc si aucun `steps` n'est fourni :

```python
self.steps = steps
```

donne :

```python
self.steps = None
```

Puis :

```python
for step in self.steps:
```

provoque :

```text
TypeError: 'NoneType' object is not iterable
```

---

# 23. Identifier la configuration correcte des Steps

La section `if __name__ == "__main__"` du `PipelineRunner` contient déjà la liste correcte :

```python
steps=[
    EnvironmentSetup(...),
    ReferenceDataLoader(...),
    UberBronze(...),
    UberSilver(...),
    UberGold(...),
    DataLoader(...),
    MaintenanceJob(...)
]
```

On peut rechercher les endroits où `steps` est défini :

```bash
cd /mnt/d/data-ai-engineer-roadmap/nyc_taxi

grep -R "steps =" -n src/jobs src | head -30
```

Et rechercher les utilisations de `PipelineRunner` :

```bash
grep -R "PipelineRunner(" -n . \
    --exclude-dir=.git \
    --exclude-dir=__pycache__
```

---

# 24. Correction : créer les Steps dans `run_pipeline.py`

La logique de construction du pipeline a été déplacée dans :

```text
airflow/run_pipeline.py
```

Le fichier construit :

```python
steps = [
    EnvironmentSetup(...),
    ReferenceDataLoader(...),
    UberBronze(...),
    UberSilver(...),
    UberGold(...),
    DataLoader(...),
    MaintenanceJob(...),
]
```

Puis transmet la liste au :

```python
PipelineRunner
```

avec :

```python
runner = PipelineRunner(
    spark=spark,
    env=env,
    taxi_type=taxi_type,
    periode=periode,
    logger=logger,
    steps=steps,
)
```

Ainsi :

```text
run_pipeline.py
       │
       ▼
     steps
       │
       ▼
PipelineRunner
```

---

# 25. Tester `run_pipeline.py`

Après modification :

```bash
docker compose restart airflow-scheduler
```

Tester l'import :

```bash
docker compose exec airflow-scheduler python -c "
from run_pipeline import run_nyc_taxi_pipeline
print('run_pipeline import OK')
"
```

Résultat attendu :

```text
run_pipeline import OK
```

---

# 26. Tester le DAG

Vérifier d'abord que le DAG est visible :

```bash
docker compose exec airflow-scheduler \
    airflow dags show nyc_taxi_airflow
```

Puis exécuter un test :

```bash
docker compose exec airflow-scheduler \
    airflow dags test nyc_taxi_airflow 2026-09-11
```

---

# 27. Comprendre la commande `airflow dags test`

Commande complète :

```bash
docker compose exec airflow-scheduler \
    airflow dags test nyc_taxi_airflow 2026-09-11
```

Elle se lit de gauche à droite.

## `docker compose`

Utilise le fichier :

```text
docker-compose.yml
```

pour gérer les services Docker du projet.

---

## `exec`

Demande à Docker :

> Exécute une commande dans un conteneur déjà démarré.

Il ne crée pas un nouveau conteneur.

---

## `airflow-scheduler`

C'est le service dans lequel la commande sera exécutée.

```text
docker compose
       │
       └── exec
             │
             └── airflow-scheduler
```

---

## `airflow dags test`

C'est une commande de la CLI Airflow.

Elle demande à Airflow de tester l'exécution d'un DAG.

---

## `nyc_taxi_airflow`

C'est le :

```text
dag_id
```

défini dans :

```python
with DAG(
    dag_id="nyc_taxi_airflow",
```

---

## `2026-09-11`

C'est la date logique utilisée pour cette exécution de test.

La commande signifie donc :

> Dans le conteneur `airflow-scheduler`, demande à Airflow d'exécuter le DAG `nyc_taxi_airflow` en mode test avec la date logique du 11 septembre 2026.

---

# 28. Différence entre `dags show` et `dags test`

## `dags show`

```bash
docker compose exec airflow-scheduler \
    airflow dags show nyc_taxi_airflow
```

Répond principalement à :

> Est-ce que mon DAG est correctement chargé ?

---

## `dags test`

```bash
docker compose exec airflow-scheduler \
    airflow dags test nyc_taxi_airflow 2026-09-11
```

Répond à :

> Est-ce que mon DAG arrive réellement à exécuter la task et le pipeline ?

---

# 29. Conserver les logs d'un test

Pour conserver la sortie du test :

```bash
docker compose exec airflow-scheduler \
    airflow dags test nyc_taxi_airflow 2026-09-11 \
    2>&1 | tee /tmp/airflow_test.log
```

Explication :

```text
2>&1
```

redirige les erreurs vers la sortie standard.

```text
tee
```

affiche la sortie à l'écran tout en l'enregistrant dans :

```text
/tmp/airflow_test.log
```

On peut ensuite rechercher une erreur :

```bash
grep -n -B 15 -A 5 \
    "TypeError: 'NoneType' object is not iterable" \
    /tmp/airflow_test.log
```

---

# 30. Vérifier les logs du Scheduler

Après un problème ou une modification :

```bash
docker compose logs airflow-scheduler --since=5m
```

Cette commande affiche les logs du Scheduler des cinq dernières minutes.

On peut également redémarrer le Scheduler :

```bash
docker compose restart airflow-scheduler
```

---

# 31. Résultat final du test

Le test final a produit :

```text
PIPELINE FINALIZED - STATUS = OK
```

Puis :

```text
Task instance state updated new_state=success
```

Et enfin :

```text
DagRun Finished:
dag_id=nyc_taxi_airflow
state=success
```

Le pipeline a donc été exécuté avec succès par Airflow.

Le fichier de log généré était :

```text
/opt/airflow/nyc_taxi/logs/yellow/2025/202501_20260911_204135.ok
```

Le suffixe :

```text
.ok
```

confirme également que le mécanisme de logging du pipeline considère l'exécution comme réussie.

---

# 32. Architecture finale

L'architecture obtenue est maintenant :

```text
                    Airflow
                       │
                       ▼
             nyc_taxi_airflow.py
                       │
                       │ déclenche
                       ▼
                run_pipeline.py
                       │
                       ▼
                PipelineRunner
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Environment    Reference       UberBronze
     Setup          Data              │
                                      ▼
                                 UberSilver
                                      │
                                      ▼
                                  UberGold
                                      │
                                      ▼
                                  DataLoader
                                      │
                                      ▼
                                Maintenance
```

---

# 33. Pourquoi cette séparation est importante

Le DAG ne contient pas toute la logique métier.

Il se contente d'orchestrer :

```text
DAG
 ↓
Task
 ↓
run_pipeline()
```

Le fichier :

```text
run_pipeline.py
```

contient le point d'entrée du pipeline.

Le :

```text
PipelineRunner
```

reste indépendant d'Airflow.

Cela permet d'utiliser le même moteur depuis :

```text
CLI
 │
 ├── Local
 │
 ├── Docker
 │
 ├── Airflow
 │
 └── Databricks
```

---

# 34. Prochaines étapes d'industrialisation

Une fois le fonctionnement de base validé, les améliorations pourront être faites progressivement.

## Étape 1 — DAG fonctionnel

```text
[x] Airflow installé
[x] Docker fonctionnel
[x] DAG créé
[x] PipelineRunner exécuté
[x] Logs vérifiés
[x] Exécution SUCCESS
```

## Étape 2 — Paramétrage

```text
[ ] Période dynamique
[ ] Taxi type dynamique
[ ] Paramètres Airflow
```

## Étape 3 — Scheduling

```text
[ ] Scheduling quotidien
[ ] Gestion de la date d'exécution
[ ] Catchup
```

## Étape 4 — Robustesse

```text
[ ] Retries
[ ] Gestion des erreurs
[ ] Timeout
[ ] Alertes
```

## Étape 5 — Monitoring

```text
[ ] Logs Airflow
[ ] Logs pipeline
[ ] Suivi des exécutions
[ ] Contrôle des volumes
```

## Étape 6 — Découpage Airflow

À terme, le pipeline pourrait être représenté par plusieurs tasks :

```text
EnvironmentSetup
       │
       ▼
ReferenceData
       │
       ▼
Bronze
       │
       ▼
Silver
       │
       ▼
Gold
       │
       ▼
Quality
       │
       ▼
Maintenance
```

Mais ce découpage doit être réalisé **après avoir validé le fonctionnement du pipeline monolithique dans Airflow**.

---

# 35. Commandes essentielles à retenir

## Démarrer Airflow

```bash
cd /mnt/d/data-ai-engineer-roadmap/airflow

docker compose up -d
```

## Vérifier les conteneurs

```bash
docker compose ps
```

## Entrer dans le Scheduler

```bash
docker compose exec airflow-scheduler bash
```

## Vérifier les DAGs

```bash
docker compose exec airflow-scheduler airflow dags list
```

## Vérifier les erreurs d'import

```bash
docker compose exec airflow-scheduler airflow dags list-import-errors
```

## Afficher un DAG

```bash
docker compose exec airflow-scheduler \
    airflow dags show nyc_taxi_airflow
```

## Tester un DAG

```bash
docker compose exec airflow-scheduler \
    airflow dags test nyc_taxi_airflow 2026-09-11
```

## Voir les logs du Scheduler

```bash
docker compose logs airflow-scheduler --since=5m
```

## Redémarrer le Scheduler

```bash
docker compose restart airflow-scheduler
```

## Tester un import Python

```bash
docker compose exec airflow-scheduler python -c "
from nyc_taxi.src.jobs.pipeline_runner_jobs_bundles import PipelineRunner
print('IMPORT OK')
"
```

## Tester `run_pipeline.py`

```bash
docker compose exec airflow-scheduler python -c "
from run_pipeline import run_nyc_taxi_pipeline
print('run_pipeline import OK')
"
```

---

# 36. Résumé à retenir

Le point essentiel de cette intégration est :

```text
Windows
   │
   ▼
WSL
   │
   ▼
Docker
   │
   ▼
Airflow
   │
   ▼
DAG
   │
   ▼
run_pipeline.py
   │
   ▼
PipelineRunner
   │
   ▼
Spark
   │
   ├── Bronze
   ├── Silver
   └── Gold
```

Airflow est donc utilisé comme **orchestrateur**, tandis que le code métier reste dans le projet `nyc_taxi`.

Le test final :

```bash
docker compose exec airflow-scheduler \
    airflow dags test nyc_taxi_airflow 2026-09-11
```

a confirmé :

```text
PIPELINE FINALIZED - STATUS = OK
Task = SUCCESS
DagRun = SUCCESS
```

L'intégration **Airflow → PipelineRunner → NYC Taxi** est donc fonctionnelle.



docker compose exec airflow-scheduler python -c "
from nyc_taxi.src.jobs.run_pipeline import run_nyc_taxi_pipeline
print('run_pipeline import OK')
"


#### Etape
✅ DAG avec 1 tâche  
✅ run_pipeline.py séparé  
✅ Exécution depuis Airflow  
✅ Logs Airflow  

⬜ Paramètres Airflow (periode, taxi_type)  
⬜ Variables Airflow  
⬜ Connections Airflow  
⬜ DAG Bronze/Silver/Gold séparés  
⬜ Retries  
⬜ Notifications  
⬜ Monitoring  
⬜ Déploiement Databricks  


### Actions à faire
* [ ] Ajouter un formulaire Airflow avec params pour saisir periode, taxi_type et env directement depuis l'interface, puis de les récupérer dans run_pipeline.py
* [ ] C'est exactement comme cela que les équipes Data Engineering déclenchent des rechargements ciblés en production


### Vérifier que le DAG est rechargé
* [ ] cd /mnt/d/data-ai-engineer-roadmap/airflow
* [ ] docker compose restart airflow-scheduler
* [ ] docker compose exec airflow-scheduler airflow dags show nyc_taxi_airflow
* [ ] docker compose exec airflow-scheduler airflow dags list | grep nyc_taxi
* [ ] docker compose exec airflow-scheduler airflow dags show nyc_taxi_airflow
* [ ] docker compose exec airflow-scheduler cat /opt/airflow/dags/nyc_taxi_airflow.py
* [ ] docker compose exec airflow-scheduler find /opt/airflow/dags -maxdepth 2 -type f -print
* [ ] docker compose exec airflow-scheduler grep -R "env = \"docker\"" /opt/airflow/dags
* [ ] docker compose exec airflow-scheduler grep -R 'dag_id="nyc_taxi_airflow"' /opt/airflow/dags
* [ ] docker compose exec airflow-scheduler grep -n "Param\|params\|periode\|taxi_type\|env" /opt/airflow/dags/nyc_taxi_airflow.py
* [ ] docker compose restart airflow-apiserver
* [ ] sleep 5

* [ ] docker compose restart airflow-apiserver -> forcer une nouvelle session
* [ ] docker compose down -v
* [ ] docker compose up -d
* [ ] docker compose exec airflow-apiserver airflow dags list | grep nyc_taxi
* [ ] docker compose exec airflow-apiserver airflow dags details nyc_taxi_airflow
* [ ] docker compose exec airflow-scheduler airflow config get-value database sql_alchemy_conn
* [ ] grep -n -A15 -B5 "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN" docker-compose.yml
* [ ] grep -n -A10 -B5 "airflow-scheduler:" docker-compose.yml
* [ ] grep -n -A10 -B5 "airflow-apiserver:" docker-compose.yml
* [ ] docker compose exec airflow-scheduler airflow config get-value dag_processor refresh_interval
* [ ] docker compose exec airflow-scheduler airflow config get-value dag_processor min_file_process_interval
* [ ] docker compose exec airflow-scheduler airflow info
* [ ] docker compose exec airflow-scheduler airflow --help
* [ ] docker compose exec airflow-scheduler airflow dag-processor --help
* [ ] docker compose exec airflow-scheduler airflow dag-processor -n 1 -v
* [ ] docker compose exec airflow-scheduler airflow dags list | grep nyc
* [ ] docker compose exec airflow-scheduler airflow dags list | grep nyc
* [ ] docker compose down
* [ ] docker compose up -d
* [ ] docker compose ps

* [ ] docker compose exec airflow-scheduler airflow dags list | grep nyc

enregistrer ton DAG dans la base.
vérifier la configuration Airflow 3 du DAG processor
chargement/parsing des DAGs du Scheduler
fichier est parsé par le DagBag, 
mais que nyc_taxi_airflow n'arrive pas jusqu'à la base utilisée par l'API/UI.
quels conteneurs Airflow sont démarrés (scheduler, apiserver, éventuel dag-processor, etc.)

Ton environnement Docker contient uniquement :
airflow-apiserver
airflow-scheduler
postgres

* Le DAG Processor est le composant chargé de parser les DAGs et de les enregistrer dans la base.

* Avec Airflow 3, la configuration recommandée est généralement :
API Server
Scheduler
DAG Processor
PostgreSQL


```text
PostgreSQL
     │
     ├── airflow-apiserver
     ├── airflow-scheduler
     └── airflow-dag-processor
```


```text
Docker Desktop
      │
      ▼
 ┌─────────────┐
 │ PostgreSQL  │
 └──────┬──────┘
        │
 ┌──────┼───────────────┐
 │      │               │
 ▼      ▼               ▼
API  Scheduler   DAG Processor
Server
 │      │               │
 └──────┴───────┬───────┘
                │
                ▼
        nyc_taxi_airflow
                │
                ▼
        run_pipeline.py
                │
                ▼
         PipelineRunner
```


✅ Le fichier existe dans /opt/airflow/dags  
✅ DagBag manuel arrive à charger nyc_taxi_airflow  
✅ Pas d'erreur de syntaxe  
✅ PostgreSQL fonctionne  
❌ airflow dags list ne voit aucun DAG  
❌ UI ne voit aucun DAG  




docker compose exec airflow-scheduler \
python -c "
from airflow.models import DagBag
bag = DagBag(dag_folder='/opt/airflow/dags', include_examples=False)
dag = bag.get_dag('nyc_taxi_airflow')
print('DAG =', dag.dag_id)
print('PARAMS =', dag.params)
"


docker compose exec airflow-scheduler \
python -c "
from airflow.models import DagBag
bag = DagBag(dag_folder='/opt/airflow/dags', include_examples=False)
dag = bag.get_dag('nyc_taxi_airflow')
print('DAG =', dag.dag_id)
print('PARAMS =', dag.params)
"




* [ ] Tester dans l'interface : http://localhost:8080
* [ ] Puis : DAGs -> nyc_taxi_airflow -> Trigger DAG
* [ ] reponse attendu : periode taxi_type env

### Premier test : 
* [ ] parametres à saisir : {"periode": 202504,"taxi_type": "yellow","env": "docker"}
* [ ] Puis : Trigger

### Vérifier la transmission


## Déclencher le DAG depuis l'interface Airflow
Et ton run_nyc_taxi_pipeline() sait déjà récupérer : params = context["params"]
```text
Airflow
   │
   ▼
nyc_taxi_airflow
   │
   ▼
PythonOperator
   │
   ▼
run_nyc_taxi_pipeline(**context)
   │
   ▼
PipelineRunner
```




docker stats --no-stream