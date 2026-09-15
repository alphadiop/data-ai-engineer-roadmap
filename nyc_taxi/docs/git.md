# Guide Git – Configuration, diagnostic et workflow

## 1. Pourquoi Git est indispensable

Git permet de :

* sauvegarder l'historique du projet
* revenir à une version précédente
* comparer les modifications
* collaborer avec d'autres développeurs
* synchroniser le code avec GitHub

Dans un projet Data Engineering, Git sert à versionner :

```text
Code Python
DAG Airflow
Databricks Bundles
Fichiers YAML
SQL
Documentation
```

---

# 2. Configuration initiale Git

## Vérifier Git

```bash
git --version
```

Exemple :

```text
git version 2.50.1
```

---

## Configurer son identité

GitHub refuse souvent les commits si l'identité n'est pas configurée correctement.

Configuration globale :

```bash
git config --global user.name "Alpha Oumar Diop"

git config --global user.email "alphadiop@gmail.com"
```

Vérification :

```bash
git config --global --list
```

Exemple :

```text
user.name=Alpha Oumar Diop
user.email=alphadiop@gmail.com
```

---

# 3. Diagnostic de configuration

## Voir toute la configuration

```bash
git config --list
```

---

## Voir uniquement le nom

```bash
git config user.name
```

---

## Voir uniquement l'email

```bash
git config user.email
```

---

## Identifier la provenance d'une configuration

Très utile lorsqu'il existe plusieurs fichiers de configuration.

```bash
git config --show-origin --list
```

Exemple :

```text
file:/home/alpha/.gitconfig
user.name=Alpha Oumar Diop
```

---

# 4. Vérifier que l'on est dans un dépôt Git

```bash
git status
```

Si Git répond :

```text
fatal: not a git repository
```

alors tu n'es pas dans le dossier du projet.

---

# 5. Diagnostic quotidien

## État du projet

Commande la plus utilisée :

```bash
git status
```

Exemple :

```text
modified:
    src/jobs/pipeline_runner_jobs_bundles.py

modified:
    resources/nyc_pipeline.yml
```

Git indique :

* les fichiers modifiés
* les fichiers ajoutés
* les fichiers supprimés
* les fichiers déjà préparés pour le commit

---

## Voir les fichiers modifiés

```bash
git diff --name-only
```

Exemple :

```text
resources/nyc_pipeline.yml
src/audit/audit_manager.py
```

---

## Voir le détail des modifications

```bash
git diff
```

Exemple :

```diff
- default: "202503"
+ default: "202504"
```

---

## Résumé rapide

```bash
git diff --stat
```

Exemple :

```text
resources/nyc_pipeline.yml | 4 ++--
audit_manager.py          | 12 ++++++------
```

---

# 6. Préparer un commit

## Ajouter un fichier

```bash
git add resources/nyc_pipeline.yml
```

---

## Ajouter plusieurs fichiers

```bash
git add fichier1 fichier2
```

---

## Ajouter tout

```bash
git add .
```

Attention :

```text
git add .
```

ajoute tous les fichiers modifiés.

Toujours vérifier avant avec :

```bash
git status
```

---

# 7. Réaliser un commit

## Commit simple

```bash
git commit -m "feat(job): add period parameter"
```

---

## Vérifier l'historique

```bash
git log
```

---

## Historique compact

```bash
git log --oneline
```

Exemple :

```text
f35a8d2 feat(job): add period parameter
c71a921 feat(databricks): initial bundle deployment
```

---

# 8. Diagnostic des derniers commits

## Dernier commit

```bash
git show HEAD
```

---

## Derniers commits

```bash
git log -5 --oneline
```

---

# 9. Connexion à GitHub

## Voir le dépôt distant

```bash
git remote -v
```

Exemple :

```text
origin  git@github.com:alphadiop/nyc_taxi.git
```

---

## Vérifier la branche

```bash
git branch
```

Exemple :

```text
* main
```

---

## Voir toutes les branches

```bash
git branch -a
```

---

# 10. Envoyer les modific
