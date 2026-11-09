# Projet NYC Taxi — Assistant IA hybride RAG + SQL

## 1. Contexte et objectif

Le projet NYC Taxi est un projet portfolio de Data Engineering utilisant Python, PySpark, Databricks et Delta Lake. Il repose sur une architecture médaillon composée des couches Bronze, Silver et Gold.

L'objectif est d'ajouter un assistant IA capable de répondre à des questions en langage naturel sur les données NYC Taxi et sur le fonctionnement technique du pipeline.

L'implémentation commencera en local sous Windows, avec Python, en conservant l'architecture existante et sans perturber le pipeline Databricks ni son CI/CD.

## 2. Objectifs fonctionnels

L'assistant devra progressivement répondre à des questions telles que :

- Comment est calculé le chiffre d'affaires ?
- Comment fonctionne la couche Silver ?
- Quel est le chiffre d'affaires par jour en avril 2025 ?
- Quelles sont les zones de départ les plus fréquentées ?
- Comment évoluent les indicateurs entre deux périodes ?

Les réponses devront être fondées sur la documentation du projet et sur les résultats réels des requêtes SQL.

## 3. Comprendre le RAG

RAG signifie *Retrieval-Augmented Generation*, ou génération augmentée par la recherche d'informations.

Le RAG permet à un modèle de langage (LLM) de répondre à une question en s'appuyant sur des informations récupérées dans une source documentaire.

Son fonctionnement comprend quatre étapes :

1. **Préparation des documents** : charger les fichiers de documentation.
2. **Chunking** : découper les documents en petits morceaux de texte.
3. **Embeddings et indexation** : convertir les morceaux en vecteurs numériques représentant leur sens, puis les indexer.
4. **Retrieval et génération** : retrouver les passages pertinents, les transmettre au LLM avec la question et générer une réponse fondée sur le contexte.

Le RAG n'est pas un modèle à entraîner. C'est une architecture qui associe recherche d'informations et génération de texte.

## 4. Pourquoi combiner RAG et SQL ?

Le RAG seul n'est pas adapté aux calculs exacts sur des données structurées.

L'architecture cible combinera trois mécanismes :

- **RAG** : recherche dans la documentation, les règles de gestion et le dictionnaire de données.
- **SQL** : calcul des indicateurs et interrogation des tables Gold.
- **LLM** : interprétation du contexte et formulation d'une réponse compréhensible.

Exemples :

| Question | Mécanisme principal |
|---|---|
| Que signifie le KPI chiffre d'affaires ? | RAG |
| Comment fonctionne le pipeline ? | RAG |
| Quel est le chiffre d'affaires d'avril 2025 ? | SQL |
| Compare les revenus de deux périodes. | SQL + LLM |
| Explique l'évolution d'un indicateur. | SQL + RAG + LLM |

Les calculs numériques devront être exécutés par SQL, et non estimés par le LLM.

## 5. Architecture cible

Le fonctionnement prévu est le suivant :

1. L'utilisateur pose une question en langage naturel.
2. Un orchestrateur Python analyse la question et sélectionne le mécanisme adapté.
3. Le RAG recherche les passages documentaires pertinents lorsque cela est nécessaire.
4. SQL interroge les données Gold lorsque la question nécessite des chiffres.
5. Le LLM rédige une réponse à partir des informations récupérées.
6. L'assistant retourne la réponse et, lorsque c'est possible, les sources utilisées.

## 6. Technologies envisagées

| Composant | Technologie envisagée |
|---|---|
| Langage | Python |
| Documentation | Markdown et fichiers texte |
| Embeddings | Modèle pré-entraîné |
| Index vectoriel | FAISS ou Chroma |
| LLM local | Ollama, sous réserve de compatibilité |
| Données métier | Tables Gold Delta Lake ou source SQL accessible |
| Orchestration | Python |
| Tests | pytest |
| Industrialisation ultérieure | GitHub Actions et orchestration existante |

Ces choix restent à confirmer en fonction des données disponibles, des ressources de la machine et de la compatibilité des dépendances.

## 7. Environnement de travail

- Projet : `D:\data-ai-engineer-roadmap\nyc_taxi`
- Environnement Python : `D:\conda_envs\spark_local`
- Package existant : `nyc_taxi`
- Tables Gold connues : `gold_fact_trips` et `gold_kpi_daily`

L'emplacement exact des nouveaux modules n'est pas encore défini. Il sera déterminé après inspection de l'arborescence réelle.

## 8. Plan d'implémentation

### Étape 1 — Vérifier l'environnement

- Activer l'environnement Conda existant.
- Vérifier les versions de Python et de pip.
- Examiner l'état Git.
- Inspecter l'arborescence de `nyc_taxi/src`.
- Identifier les fichiers `pyproject.toml`, `setup.py` et `requirements.txt`.

### Étape 2 — Préparer les documents

Rassembler les documents utiles : README, documentation des couches Bronze/Silver/Gold, règles de transformation et définitions des KPI.

### Étape 3 — Construire le RAG documentaire

- Charger les documents.
- Découper les textes en morceaux.
- Générer les embeddings.
- Construire l'index vectoriel.
- Retrouver les passages pertinents pour une question.
- Tester la qualité de la recherche.

### Étape 4 — Connecter les données SQL

- Identifier la source réellement accessible pour les données Gold.
- Définir les requêtes nécessaires aux indicateurs.
- Limiter les requêtes autorisées.
- Vérifier les résultats et les règles de gestion.

### Étape 5 — Construire l'assistant hybride

- Créer un orchestrateur Python.
- Orienter les questions vers le RAG, SQL ou les deux.
- Transmettre les résultats au LLM.
- Retourner des réponses sourcées.

### Étape 6 — Tester et industrialiser

- Tester le retrieval et les réponses.
- Vérifier l'exactitude des calculs SQL.
- Tester les questions sans réponse disponible.
- Ajouter des tests automatisés.
- Préparer l'intégration au CI/CD sans perturber le déploiement Databricks existant.

## 9. Point d'arrêt actuel

**Aucune modification du code n'a encore été effectuée pour le RAG.**

La prochaine action consiste à exécuter les commandes d'inspection dans PowerShell :

```powershell
Set-Location "D:\data-ai-engineer-roadmap\nyc_taxi"

conda activate "D:\conda_envs\spark_local"

python --version
python -m pip --version

git status --short

Get-ChildItem .\nyc_taxi\src -Directory |
    Select-Object -ExpandProperty Name

Get-ChildItem .\nyc_taxi -File |
    Where-Object { $_.Name -in @(
        "pyproject.toml",
        "setup.py",
        "requirements.txt"
    ) } |
    Select-Object -ExpandProperty Name
```

Les résultats devront être examinés avant l'installation de nouvelles bibliothèques ou la création de fichiers.

## 10. Principes de développement

- Conserver l'architecture et le pipeline NYC Taxi existants.
- Ne pas dupliquer les modules déjà présents.
- Avancer étape par étape, avec des explications sur chaque notion et chaque fichier.
- Tester chaque brique avant de passer à la suivante.
- Ne pas modifier les tables Gold ni le déploiement Databricks pour construire le premier prototype.
- Privilégier une première version simple, compréhensible et démontrable en entretien Data Engineer.
