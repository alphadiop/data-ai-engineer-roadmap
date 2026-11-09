# Documentation technique — Construction et validation du wheel Python NYC Taxi

**Projet :** `nyc_taxi`
**Version :** `1.0.0`
**Environnement :** Windows / PowerShell / Conda
**Date :** 5 novembre 2026

---

## 1. Objectif de cette étape

L'objectif était de vérifier que le projet `nyc_taxi` pouvait être distribué sous forme de package Python installable.

Jusqu'à présent, le projet était principalement exécuté depuis son répertoire source.

Nous souhaitions vérifier qu'il était également possible de :

- Construire un package Python au format `.whl`.
- Intégrer les modules Python dans ce package.
- Embarquer les ressources nécessaires au fonctionnement des modules : YAML, JSON et SQL.
- Installer le package indépendamment du code source.
- Importer les modules depuis cette installation.
- Utiliser la commande console `nyc-taxi-pipeline`.

Cette démarche permet de se rapprocher des pratiques de distribution et d'industrialisation utilisées dans les projets Data Engineering.

## 2. Comprendre les notions importantes

### 2.1. Le package Python

Un package Python regroupe des modules et des ressources organisés dans une structure de répertoires.

Dans notre projet :

```text
nyc_taxi/
│
├── __init__.py
├── setup.py
├── pyproject.toml
│
├── config/
│   ├── __init__.py
│   └── *.yaml
│
└── src/
    ├── __init__.py
    ├── bronze/
    ├── silver/
    ├── gold/
    ├── jobs/
    ├── spark/
    ├── logger/
    ├── loader/
    ├── sql_operations/
    └── ...
```

Les fichiers `__init__.py` permettent notamment à Python d'identifier les répertoires comme des packages classiques.

### 2.2. Le fichier `setup.py`

C'est le fichier qui décrit à setuptools comment construire le package.

Il précise notamment :

- Le nom du package.
- Sa version.
- Les packages Python à intégrer.
- L'emplacement des packages dans le projet.
- Les ressources non Python à embarquer.
- Les commandes console à générer.

### 2.3. Le fichier `pyproject.toml`

Il définit les informations nécessaires au système de construction.

Notre fichier :

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
```

Ici :

- `setuptools` assure la construction du package.
- `wheel` permet de produire le format `.whl`.
- `build-backend` indique le moteur de construction utilisé.
- La section Black configure le formatage du code.

### 2.4. Le wheel `.whl`

Un wheel est une archive de distribution Python.

Exemple :

```text
nyc_taxi-1.0.0-py3-none-any.whl
```

Signification :

| Élément | Signification |
|---|---|
| `nyc_taxi` | Nom du package |
| `1.0.0` | Version |
| `py3` | Compatible Python 3 |
| `none` | Pas d'ABI spécifique |
| `any` | Pas de plateforme spécifique |

Le wheel contient les fichiers nécessaires à l'installation du package.

Il ne faut pas le confondre avec le dossier source du projet.

---

## 3. Configuration du package dans `setup.py`

Nous avons examiné le mécanisme suivant :

```python
from setuptools import setup, find_packages

src_packages = find_packages("src")

mapped_packages = [
    "nyc_taxi",
    "nyc_taxi.src",
    "nyc_taxi.config",
] + [
    f"nyc_taxi.src.{package}"
    for package in src_packages
]

package_dir = {
    "nyc_taxi": ".",
    "nyc_taxi.src": "src",
    "nyc_taxi.config": "config",
}

for package in src_packages:
    package_dir[
        f"nyc_taxi.src.{package}"
    ] = f"src/{package.replace('.', '/')}"

setup(
    name="nyc_taxi",
    version="1.0.0",
    packages=mapped_packages,
    package_dir=package_dir,
    package_data={
        "nyc_taxi.config": [
            "*.yaml",
        ],
        "nyc_taxi.src.sql_operations": [
            "sql_queries/*.json",
            "sql_queries/sql_files/*.sql",
        ],
    },
    entry_points={
        "console_scripts": [
            "nyc-taxi-pipeline=nyc_taxi.src.jobs.run_pipeline:main"
        ]
    },
)
```

### Comprendre `find_packages("src")`

Cette instruction recherche les packages Python présents dans `src`.

Elle permet de récupérer automatiquement les sous-packages possédant leur fichier `__init__.py`.

### Comprendre `mapped_packages`

Nous devons exposer les packages sous le nom `nyc_taxi.*`, même si les fichiers sources sont organisés différemment dans le dépôt.

Par exemple :

```text
Répertoire source :
src/jobs/

Package installé :
nyc_taxi.src.jobs/
```

`mapped_packages` définit les noms des packages dans la distribution.

### Comprendre `package_dir`

Ce dictionnaire établit la correspondance entre le nom du package et son emplacement physique.

Exemple :

```python
"nyc_taxi.src": "src"
```

Cela signifie que les fichiers du package `nyc_taxi.src` se trouvent dans le répertoire `src` de `setup.py`.

### Une erreur corrigée : le package racine

Lors de notre premier test d'installation, nous avons constaté que le wheel ne contenait pas :

```text
nyc_taxi/__init__.py
```

La déclaration initiale ne mentionnait pas explicitement le package racine.

Nous avons donc ajouté :

```python
"nyc_taxi"
```

dans `mapped_packages`, ainsi que :

```python
"nyc_taxi": "."
```

dans `package_dir`.

Après reconstruction, le wheel contenait bien :

```text
nyc_taxi/
├── __init__.py
├── setup.py
├── config/
└── src/
```

Cette correction a permis de résoudre le problème d'importation du package installé.

---

## 4. Intégration des ressources SQL et JSON

Le module `sql_operations` utilise des fichiers externes.

Structure :

```text
src/
└── sql_operations/
    ├── __init__.py
    ├── sql_operations.py
    └── sql_queries/
        ├── sql_operations.json
        └── sql_files/
            ├── load_df.sql
            ├── select_table.sql
            ├── create_table.sql
            ├── delete_rows.sql
            └── ...
```

Ces fichiers sont indispensables : le code Python les utilise pour charger des configurations et des modèles de requêtes SQL.

Or, les fichiers `.sql` et `.json` ne sont pas automatiquement intégrés au wheel comme les fichiers `.py`.

Nous avons donc configuré `package_data` :

```python
package_data={
    "nyc_taxi.config": [
        "*.yaml",
    ],
    "nyc_taxi.src.sql_operations": [
        "sql_queries/*.json",
        "sql_queries/sql_files/*.sql",
    ],
},
```

Cette configuration demande à setuptools d'intégrer :

- Les fichiers YAML du package de configuration.
- Les fichiers JSON directement dans `sql_queries`.
- Les fichiers SQL dans `sql_queries/sql_files`.

---

## 5. Construction du wheel

Nous avons utilisé :

```powershell
New-Item -ItemType Directory -Force "nyc_taxi/verification_wheel/build_output"

Push-Location "nyc_taxi"

python -m pip wheel . `
    --no-deps `
    --no-build-isolation `
    --wheel-dir "verification_wheel/build_output"

Pop-Location
```

### Comprendre la commande

| Élément | Rôle |
|---|---|
| `python -m pip wheel` | Demande à pip de construire un wheel |
| `.` | Utilise le projet situé dans le répertoire courant |
| `--no-deps` | Ne construit pas les wheels des dépendances |
| `--no-build-isolation` | Utilise l'environnement Python actuel |
| `--wheel-dir` | Définit le répertoire de sortie |

Résultat obtenu :

```text
nyc_taxi-1.0.0-py3-none-any.whl
Taille : 108 514 octets
```

### Différence entre `build`, `dist` et `verification_wheel`

- `build/` : fichiers intermédiaires générés pendant la construction.
- `dist/` : répertoire conventionnel pour les distributions finales.
- `verification_wheel/` : répertoire que nous avons choisi pour isoler les artefacts et les tests de validation.

Ces répertoires ne sont pas des packages Python.

Ils ne remplacent pas le code source.

---

## 6. Vérification du contenu du wheel

Un wheel est une archive ZIP.

Nous avons donc utilisé Python et `zipfile.ZipFile` pour examiner son contenu sans l'extraire.

Résultats :

| Type de fichier | Nombre |
|---|---:|
| Python | 92 |
| SQL | 57 |
| JSON | 1 |
| YAML | 2 |

Le fichier JSON était bien présent :

```text
nyc_taxi/src/sql_operations/sql_queries/sql_operations.json
```

Les fichiers SQL étaient également présents :

```text
nyc_taxi/src/sql_operations/sql_queries/sql_files/
```

Enfin, nous avons vérifié la déclaration du point d'entrée :

```ini
[console_scripts]
nyc-taxi-pipeline = nyc_taxi.src.jobs.run_pipeline:main
```

À ce stade, nous avions validé le contenu de l'archive.

---

## 7. Installation isolée du wheel

Il ne suffisait pas de constater que le wheel contenait les fichiers.

Nous devions également vérifier qu'il pouvait être installé.

Nous avons utilisé :

```powershell
python -m pip install `
    --no-deps `
    --target "nyc_taxi/verification_wheel/install_test" `
    "nyc_taxi/verification_wheel/build_output/nyc_taxi-1.0.0-py3-none-any.whl"
```

Résultat :

```text
Successfully installed nyc-taxi-1.0.0
```

### Pourquoi `--target` ?

Normalement, pip installe un package dans l'environnement Python actif.

Avec `--target`, nous choisissons un répertoire d'installation particulier.

Cela permet de tester le wheel sans remplacer les packages de l'environnement Conda.

Nous avons donc obtenu :

```text
verification_wheel/
├── build_output/
│   └── nyc_taxi-1.0.0-py3-none-any.whl
│
└── install_test/
    ├── nyc_taxi/
    └── ...
```

Les deux répertoires ont des rôles différents :

- `build_output` contient le fichier distribué.
- `install_test` contient le résultat de son installation.

---

## 8. Problème rencontré lors du test d'importation

Lors du premier test, Python affichait :

```text
D:\data-ai-engineer-roadmap\nyc_taxi\__init__.py
```

Nous pensions utiliser le package installé, mais Python chargeait encore le package source.

La raison : le répertoire courant et les chemins de recherche de Python peuvent faire passer le code source avant le répertoire d'installation.

Nous avons donc effectué un diagnostic depuis `%TEMP%`.

Ce diagnostic a révélé que le package installé ne contenait pas son propre `__init__.py` racine.

Après correction de `setup.py`, nous avons reconstruit et réinstallé le wheel.

Le nouveau test a donné :

```text
D:\data-ai-engineer-roadmap\nyc_taxi\verification_wheel\install_test\nyc_taxi\__init__.py
```

Cette fois, l'import provenait bien de l'installation isolée.

**C'est une distinction fondamentale : tester un import depuis le code source ne prouve pas que le package distribué fonctionne.**

---

## 9. Vérification des ressources depuis le package installé

Nous avons utilisé le module standard `importlib.resources`.

Exemple :

```python
from importlib.resources import files

package = files("nyc_taxi.src.sql_operations")

json_file = package.joinpath(
    "sql_queries",
    "sql_operations.json"
)

sql_file = package.joinpath(
    "sql_queries",
    "sql_files",
    "select_table.sql"
)
```

Puis :

```python
print(json_file.is_file())
print(sql_file.is_file())
```

Résultat :

```text
JSON accessible : True
SQL accessible : True
```

Cela démontre que les ressources peuvent être retrouvées depuis le package installé.

`importlib.resources` est particulièrement utile pour accéder aux ressources embarquées dans les packages Python sans dépendre directement du répertoire de développement.

---

## 10. Vérification du point d'entrée console

Dans `setup.py`, nous avons :

```python
entry_points={
    "console_scripts": [
        "nyc-taxi-pipeline=nyc_taxi.src.jobs.run_pipeline:main"
    ]
}
```

Cette déclaration demande à setuptools de générer une commande exécutable lors de l'installation.

Elle signifie :

1. Créer une commande `nyc-taxi-pipeline`.
2. Importer le module `nyc_taxi.src.jobs.run_pipeline`.
3. Appeler sa fonction `main()`.

Dans notre module :

```python
def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--env",
        choices=["local", "docker", "databricks"],
        default="local"
    )

    parser.add_argument(
        "--taxi_type",
        default="yellow"
    )

    parser.add_argument(
        "--periode",
        type=int,
        default=None
    )

    args = parser.parse_args()

    return run_pipeline(
        env=args.env,
        taxi_type=args.taxi_type,
        periode=args.periode
    )
```

Nous avons retrouvé le lanceur généré :

```text
verification_wheel/install_test/bin/nyc-taxi-pipeline.exe
```

Puis nous avons exécuté :

```powershell
& "$installPath/bin/nyc-taxi-pipeline.exe" --help
```

Résultat :

```text
usage: nyc-taxi-pipeline [-h]
                         [--env {local,docker,databricks}]
                         [--taxi_type TAXI_TYPE]
                         [--periode PERIODE]

options:
  -h, --help
  --env {local,docker,databricks}
  --taxi_type TAXI_TYPE
  --periode PERIODE

Code de retour : 0
```

Le lanceur fonctionne.

Nous n'avons pas exécuté le pipeline complet : `--help` permet de vérifier l'interface de la commande sans démarrer Spark ou Databricks.

---

## 11. Architecture de vérification obtenue

Nous avons organisé les tests autour de cette structure :

```text
nyc_taxi/
│
├── setup.py
├── pyproject.toml
├── src/
├── config/
│
└── verification_wheel/
    │
    ├── build_output/
    │   └── nyc_taxi-1.0.0-py3-none-any.whl
    │
    └── install_test/
        ├── nyc_taxi/
        ├── bin/
        └── nyc_taxi-1.0.0.dist-info/
```

Attention : cette arborescence représente les éléments principaux. Le répertoire d'installation contient également d'autres métadonnées et fichiers générés par pip.

---

## 12. Bilan des validations

| Vérification | Résultat |
|---|---|
| Construction du wheel | Réussie |
| Package racine | Présent |
| Modules Python | 92 présents |
| Ressources SQL | 57 présentes |
| Ressource JSON | Présente |
| Ressources YAML | 2 présentes |
| Installation isolée | Réussie |
| Import depuis l'installation | Réussi |
| Lecture du JSON installé | Réussie |
| Lecture du SQL installé | Réussie |
| Génération du lanceur console | Réussie |
| Exécution de `--help` | Réussie |

**Conclusion :** la construction, le contenu, l'installation isolée et le point d'entrée console du wheel `nyc_taxi-1.0.0` ont été validés.

Cela ne signifie pas encore que toutes les fonctionnalités métier sont validées dans un environnement propre.

---

## 13. Ce qui reste à faire

Les prochaines étapes envisagées sont :

1. Examiner et déclarer correctement les dépendances du package.
2. Vérifier que les fichiers nécessaires sont suivis par Git.
3. Tester l'installation dans un environnement Python réellement propre, avec les dépendances nécessaires.
4. Tester l'exécution du pipeline après installation.
5. Intégrer la construction et la validation du wheel dans GitHub Actions.

Nous devrons également examiner le fait que `setup.py` est actuellement embarqué dans le wheel, afin de décider si nous souhaitons l'exclure.

**Important :** les modifications locales non commitées, notamment le module `sql_operations` et ses ressources SQL/JSON, doivent être préservées. La validation locale ne signifie pas que ces fichiers ont été ajoutés à Git ou publiés sur GitHub.

---

## 14. Les notions à retenir pour un entretien Data Engineer

- **Package Python :** ensemble organisé de modules et de ressources réutilisables.
- **setuptools :** outil permettant de configurer et construire une distribution Python.
- **wheel :** format de distribution binaire prêt à installer.
- **package_dir :** correspondance entre les noms des packages et leurs emplacements physiques.
- **package_data :** déclaration des ressources non Python à embarquer.
- **entry_points :** mécanisme permettant de créer des commandes exécutables après installation.
- **pip wheel :** commande permettant de construire un wheel.
- **pip install --target :** installation dans un répertoire choisi.
- **importlib.resources :** accès aux ressources intégrées dans un package.
- **CI/CD :** automatisation des contrôles, de la construction et de la distribution.

### Exemple de présentation orale

« Sur mon projet NYC Taxi, j'ai travaillé sur la distribution du code Python sous forme de wheel. J'ai configuré setuptools pour intégrer les différents modules du projet ainsi que les ressources externes, notamment les fichiers SQL, JSON et YAML.

J'ai ensuite construit le wheel, contrôlé son contenu, installé le package dans un répertoire isolé et vérifié que les imports et les ressources fonctionnaient depuis cette installation.

J'ai également configuré et testé un point d'entrée console permettant de lancer le pipeline avec différents paramètres d'environnement, de type de taxi et de période.

Cette démarche m'a permis de vérifier que le projet pouvait être distribué indépendamment de son répertoire de développement. »

---

**État final :** wheel `nyc_taxi-1.0.0` construit et validé sur les contrôles réalisés le 5 novembre 2026.
