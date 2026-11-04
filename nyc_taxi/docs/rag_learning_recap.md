# Récapitulatif — Apprentissage et développement du RAG NYC Taxi

# Récapitulatif — Apprentissage du RAG dans le projet NYC Taxi

## 1. Objectif

L'objectif est de construire un système RAG (*Retrieval-Augmented Generation*) capable de répondre à des questions sur le projet NYC Taxi en s'appuyant sur sa documentation technique.

Exemples de questions :
- Quelle formule SQL permet de calculer le chiffre d'affaires ?
- Comment calcule-t-on le nombre de trajets ?
- À quoi servent les couches Bronze, Silver et Gold ?

Le projet utilise actuellement la partie **Retrieval**, c'est-à-dire la recherche des passages documentaires les plus pertinents. La génération de réponses par un LLM sera ajoutée ultérieurement.

## 2. Architecture du RAG

Le fonctionnement actuel suit ces étapes :

1. Charger les documents Markdown.
2. Découper les documents en chunks.
3. Transformer les chunks en embeddings.
4. Construire un index FAISS.
5. Transformer la question en embedding.
6. Rechercher les chunks les plus similaires à la question.
7. Retourner les passages pertinents avec leur source et leur score.

## 3. Chargement des documents — `document_loader.py`

La fonction `load_markdown_documents()` charge les fichiers `.md` du dossier documentaire.

Pour chaque document, elle retourne :
- `source` : le nom du fichier ;
- `content` : le contenu textuel.

Les fichiers `rag_assistant_roadmap.md` et `rag_learning_recap.md` sont exclus de la recherche afin de ne pas mélanger la documentation du projet avec les notes de suivi de l'apprentissage.

## 4. Découpage du texte — `text_splitter.py`

La fonction `split_text()` découpe un document en plusieurs morceaux appelés **chunks**.

Paramètres utilisés par défaut :
- `chunk_size = 1000` caractères ;
- `overlap = 150` caractères.

Le découpage tient compte des titres Markdown (`#`, `##`, `###`, etc.) pour préserver autant que possible le contexte des sections.

Lorsqu'une section est trop longue, elle est découpée en privilégiant les paragraphes. Un chevauchement peut être conservé entre les chunks pour limiter la perte de contexte.

**Pourquoi découper les documents ?**

Un document complet peut être trop long ou contenir plusieurs sujets. Des chunks plus ciblés permettent de retrouver plus facilement le passage utile pour répondre à une question.

## 5. Création des embeddings — `embedding_model.py`

Un embedding est une représentation numérique d'un texte sous la forme d'un vecteur.

Le modèle utilisé est :

`paraphrase-multilingual-MiniLM-L12-v2`

Il permet de représenter des textes en plusieurs langues, notamment en français.

Les embeddings des documents et de la question sont produits par le même modèle.

La normalisation est activée avec :

`normalize_embeddings=True`

Les vecteurs obtenus ont 384 dimensions.

**Pourquoi utiliser des embeddings ?**

Ils permettent de comparer le sens des textes plutôt que de rechercher uniquement des mots identiques.

Par exemple, une question sur les « revenus des courses » peut retrouver un passage qui parle du « chiffre d'affaires ».

## 6. Indexation et recherche — `embedding_index.py`

### Construction des embeddings

La fonction `build_embeddings()` :
1. charge les documents ;
2. découpe leur contenu en chunks ;
3. associe chaque chunk à son fichier source ;
4. transforme les chunks en embeddings ;
5. retourne les chunks et les vecteurs numériques.

Chaque chunk conserve son nom de fichier afin de pouvoir identifier l'origine d'un résultat.

### Construction de l'index FAISS

La fonction `build_faiss_index()` utilise :

`faiss.IndexFlatIP(embeddings.shape[1])`

FAISS est une bibliothèque de recherche de similarité vectorielle.

`IndexFlatIP` utilise le produit scalaire. Comme les embeddings sont normalisés, ce produit scalaire correspond à la similarité cosinus.

Un score plus élevé indique une plus grande similarité entre les vecteurs. Il ne représente toutefois pas une probabilité que la réponse soit correcte.

### Recherche des passages

La fonction `search_documents()` :
1. vérifie que `top_k` est positif ;
2. charge le modèle d'embeddings une seule fois ;
3. utilise ce modèle pour vectoriser les documents ;
4. construit l'index FAISS ;
5. vectorise la question ;
6. recherche les `top_k` chunks les plus similaires ;
7. retourne la source, le contenu et le score de chaque résultat.

Le paramètre `top_k=3` demande les trois passages les plus pertinents, ou moins si le nombre de chunks disponibles est inférieur à trois.

## 7. Optimisation du chargement du modèle

Initialement, le modèle était chargé deux fois pendant une recherche :
- une première fois dans `build_embeddings()` pour vectoriser les documents ;
- une seconde fois dans `search_documents()` pour vectoriser la question.

Le code a été amélioré pour charger le modèle une seule fois, puis transmettre la même instance à `build_embeddings()`.

La fonction accepte désormais un paramètre optionnel :

`def build_embeddings(docs_dir: str, model=None):`

Si aucun modèle n'est fourni, la fonction en crée un. Si une instance existe déjà, elle la réutilise.

Cette modification évite un chargement inutile sans changer le principe de la recherche.

## 8. Test de recherche

Le script `nyc_taxi/test_rag_search.py` teste la question suivante :

« Quelle formule SQL permet de calculer les revenus des courses ? »

Commande exécutée depuis la racine du dépôt :

```powershell
python .\nyc_taxi\test_rag_search.py
```

Résultats obtenus :

| Rang | Source | Score |
|---|---|---:|
| 1 | `data_model.md` | 0.683 |
| 2 | `data_model.md` | 0.504 |
| 3 | `powerbi_dashboard.md` | 0.494 |

Le premier résultat contient la section « Analyse du chiffre d'affaires » et la formule :

```sql
SUM(total_amount)
```

Le passage précise que la colonne `total_amount` représente le montant total associé à une course dans la table `gold.gold_fact_trips`.

Le score du premier résultat était auparavant de 0.374 et le passage correct n'était pas classé en première position. Après l'amélioration du découpage, le score est passé à 0.683 et le passage correct est remonté en première position.

Cette amélioration concerne ce test précis : d'autres questions doivent être testées pour évaluer la qualité globale de la recherche.

## 9. Avertissement Hugging Face

Un avertissement peut apparaître :

`Warning: You are sending unauthenticated requests to the HF Hub.`

Il indique que les requêtes vers Hugging Face sont effectuées sans jeton d'authentification.

Dans le contexte actuel, le modèle est déjà téléchargé et la recherche fonctionne. Cet avertissement n'empêche donc pas le test de s'exécuter.

## 10. État actuel et prochaines étapes

### Fonctionnalités opérationnelles

- Chargement des documents Markdown.
- Exclusion des fichiers de suivi de l'apprentissage.
- Découpage en chunks tenant compte des titres.
- Création des embeddings.
- Indexation vectorielle avec FAISS.
- Recherche sémantique des passages pertinents.
- Retour des sources, contenus et scores.
- Réutilisation du modèle pour limiter les chargements.

### Prochaines étapes

1. Tester plusieurs formulations de questions.
2. Vérifier la pertinence des résultats pour les KPI, les distances et l'architecture Bronze/Silver/Gold.
3. Ajuster si nécessaire le découpage et le nombre de résultats `top_k`.
4. Étudier l'intégration d'un LLM pour générer une réponse à partir des passages retrouvés.
5. Ajouter des tests automatisés pour vérifier la qualité de la recherche.

## 11. Vocabulaire essentiel

- **RAG** : approche qui combine la recherche documentaire et la génération de réponses.
- **Document** : fichier contenant les informations de référence.
- **Chunk** : morceau de document utilisé pour la recherche.
- **Embedding** : représentation numérique d'un texte.
- **Similarité cosinus** : mesure de la proximité entre deux vecteurs normalisés.
- **FAISS** : bibliothèque permettant de rechercher des vecteurs similaires.
- **Top-k** : nombre de résultats retournés.
- **Retrieval** : étape de recherche des passages pertinents.
- **Generation** : étape où un LLM rédige une réponse à partir du contexte retrouvé.
- **LLM** : grand modèle de langage utilisé pour comprendre et générer du texte.

**À retenir :** le système actuel sait retrouver les passages documentaires les plus proches d'une question. Il ne génère pas encore de réponse rédigée par un LLM. C'est la prochaine évolution du projet.
---


----
## 1. Objectif du projet

L'objectif est d'intégrer un système de recherche documentaire (RAG, *Retrieval-Augmented Generation*) au projet NYC Taxi.

Le système doit permettre de poser des questions en langage naturel sur la documentation technique et métier du projet, puis de retrouver les passages les plus pertinents pour répondre à ces questions.

Exemples de questions :
- Comment est calculé le chiffre d'affaires ?
- Quelle formule SQL permet de calculer les revenus des courses ?
- Quelles sont les tables de la couche Gold ?
- Comment le pipeline Databricks est-il déployé ?

Pour le moment, le projet implémente la **recherche documentaire**. La génération automatique de réponses par un LLM n'est pas encore intégrée.

## 2. Environnement de développement

- Système : Windows
- Environnement Python : Conda
- Répertoire du projet : `D:\data-ai-engineer-roadmap`
- Répertoire NYC Taxi : `D:\data-ai-engineer-roadmap\nyc_taxi`
- Environnement Python : `D:\conda_envs\spark_local`
- Version Python : 3.11.15

Bibliothèques utilisées :
- `sentence-transformers` : transformation des textes en vecteurs numériques (*embeddings*).
- `faiss-cpu` : recherche des vecteurs les plus similaires.
- `numpy` : manipulation des vecteurs numériques.

Le modèle d'embeddings utilisé est :

`paraphrase-multilingual-MiniLM-L12-v2`

Ce modèle prend en charge plusieurs langues, dont le français, et produit des vecteurs de 384 dimensions.

## 3. Organisation du code RAG

Les fichiers principaux se trouvent dans `nyc_taxi/src/rag/`.

### `document_loader.py`

Responsabilité : charger les documents Markdown du répertoire documentaire.

La fonction `load_markdown_documents(docs_dir)` :
1. Vérifie que le répertoire existe.
2. Parcourt les fichiers Markdown.
3. Ignore certains fichiers exclus.
4. Lit leur contenu en UTF-8.
5. Retourne une liste de documents contenant leur nom et leur contenu.

Structure d'un document chargé :

- `source` : nom du fichier Markdown.
- `content` : contenu textuel du fichier.

Le fichier `rag_assistant_roadmap.md` est actuellement exclu du chargement.

Le présent récapitulatif devra également être exclu pour éviter que les notes d'apprentissage et les résultats des tests influencent la recherche documentaire.

### `text_splitter.py`

Responsabilité : découper les documents en petits passages appelés *chunks*.

La fonction utilisée est :

`split_text(text, chunk_size=1000, overlap=150)`

Le découpeur actuel :
1. Sépare le texte sur les doubles retours à la ligne.
2. Ignore les paragraphes vides.
3. Regroupe les paragraphes jusqu'à ce que l'ajout d'un paragraphe dépasse la taille cible.
4. Conserve les paragraphes entiers dans la mesure du possible.
5. Ajoute un chevauchement constitué de paragraphes précédents lorsqu'ils tiennent dans la limite définie.
6. Retourne une liste de chunks.

**Limite identifiée :** le découpeur ne tient pas encore compte de la hiérarchie des titres Markdown. Plusieurs sections métier peuvent donc se retrouver dans un même chunk. Un paragraphe très long peut également dépasser la taille cible.

Le découpage par titres Markdown est la prochaine amélioration prévue.

### `embedding_model.py`

Responsabilité : charger le modèle de transformation des textes en vecteurs.

La fonction `create_embedding_model()` charge le modèle :

`paraphrase-multilingual-MiniLM-L12-v2`

Le modèle est utilisé pour encoder les passages documentaires et les questions des utilisateurs.

### `embedding_index.py`

Responsabilité : construire l'index vectoriel et rechercher les passages pertinents.

Trois fonctions principales sont présentes.

#### `build_embeddings(docs_dir)`

Cette fonction :
1. Charge les documents.
2. Découpe chaque document en chunks.
3. Associe chaque chunk à son fichier source.
4. Transforme les chunks en vecteurs.
5. Normalise les vecteurs.
6. Retourne les chunks et les embeddings sous forme de tableau NumPy en `float32`.

Chaque chunk contient :
- `source`
- `content`

#### `build_faiss_index(embeddings)`

Cette fonction construit un index FAISS avec :

`faiss.IndexFlatIP`

Il s'agit d'un index exact fondé sur le produit scalaire. Comme les vecteurs sont normalisés, ce produit scalaire correspond à la similarité cosinus.

L'index permet de retrouver les vecteurs les plus similaires à celui d'une question.

#### `search_documents(question, docs_dir, top_k=3)`

Cette fonction :
1. Construit les embeddings documentaires.
2. Construit l'index FAISS.
3. Transforme la question en vecteur.
4. Recherche les `top_k` chunks les plus similaires.
5. Retourne les résultats classés par score décroissant.

Chaque résultat contient :
- `source` : document d'origine ;
- `content` : contenu du chunk ;
- `score` : score de similarité.

Le paramètre `top_k=3` demande les trois résultats les plus similaires.

## 4. Documentation utilisée

Les documents Markdown du répertoire `nyc_taxi/docs/` comprennent notamment :

- `architecture.md`
- `data_model.md`
- `deployment.md`
- `powerbi_dashboard.md`
- `rag_assistant_roadmap.md`

Le fichier `rag_assistant_roadmap.md` est exclu de la recherche.

Les documents décrivent l'architecture, le modèle de données, le déploiement et le tableau de bord Power BI du projet NYC Taxi.

Un exemple important se trouve dans `data_model.md`, dans la section consacrée au chiffre d'affaires :

```sql
SUM(total_amount)
```

Cette formule correspond à la somme de la colonne `total_amount` des courses analysées. Le résultat dépend notamment des filtres appliqués et de la période sélectionnée.

La table Gold concernée est `gold.gold_fact_trips`.

## 5. Tests réalisés

### Test 1 — Chargement des documents

Le chargement des documents Markdown a été vérifié.

Le système a chargé quatre documents et produit 43 chunks lors d'un test précédent.

Le fichier de roadmap a été exclu.

### Test 2 — Vérification des chunks

Un script `nyc_taxi/check_rag_chunks.py` permet d'examiner les documents et les chunks produits.

Il a notamment permis de vérifier que le passage métier consacré au chiffre d'affaires est bien présent dans `data_model.md`.

Le découpeur conserve désormais les paragraphes entiers, ce qui améliore la cohérence des passages.

### Test 3 — Recherche du chiffre d'affaires

Script de test : `nyc_taxi/test_rag_search.py`

Question initiale :

« Comment est calculé le chiffre d'affaires ? »

Un résultat obtenu précédemment était :

| Document | Score |
|---|---:|
| `data_model.md` | 0,462 |
| `powerbi_dashboard.md` | 0,413 |
| `powerbi_dashboard.md` | 0,347 |

Le premier résultat contenait la formule `SUM(total_amount)` et son explication métier.

Le score de 0,462 indique une similarité vectorielle ; il ne signifie pas que la réponse est correcte à 46,2 %.

### Test 4 — Reformulation de la question

La question a ensuite été remplacée par :

« Quelle formule SQL permet de calculer les revenus des courses ? »

Résultats observés :

| Rang | Document | Score |
|---:|---|---:|
| 1 | `data_model.md` | 0,441 |
| 2 | `architecture.md` | 0,379 |
| 3 | `data_model.md` | 0,374 |

Le troisième résultat contenait bien `SUM(total_amount)` et son explication.

**Conclusion du test :** le système retrouve l'information recherchée malgré une reformulation de la question, mais ne classe pas toujours le passage le plus pertinent en première position.

C'est une limite de la recherche actuelle qui devra être améliorée.

## 6. Points techniques à retenir

### Embeddings

Un embedding est une représentation numérique d'un texte.

Les textes dont les représentations vectorielles sont proches sont considérés comme sémantiquement similaires par le moteur de recherche.

### Similarité cosinus

La similarité cosinus permet de comparer les vecteurs de la question et des chunks.

Les vecteurs étant normalisés, l'index `IndexFlatIP` peut utiliser le produit scalaire pour effectuer cette comparaison.

### `top_k`

`top_k` détermine le nombre de résultats renvoyés par la recherche.

Avec `top_k=3`, le système retourne au maximum trois chunks.

### Limites actuelles

- Les résultats sont classés par similarité, pas par vérification de l'exactitude de la réponse.
- Un passage peut avoir un score élevé sans répondre précisément à la question.
- Les chunks ne suivent pas encore systématiquement les titres Markdown.
- Les embeddings documentaires sont recalculés à chaque appel de `search_documents`.
- Le modèle est actuellement chargé deux fois lors d'une recherche : une fois pour les documents et une fois pour la question.
- Le système ne génère pas encore de réponse à l'aide d'un LLM.

L'avertissement indiquant que les requêtes vers Hugging Face ne sont pas authentifiées n'a pas empêché les tests de fonctionner.

## 7. Prochaines étapes

### Étape 1 — Découpage par titres Markdown

Modifier `text_splitter.py` pour tenir compte de la structure des documents.

L'objectif est de conserver ensemble un titre, son explication et les informations associées.

Par exemple, la section « Analyse du chiffre d'affaires » doit idéalement former un chunk contenant sa définition et la formule `SUM(total_amount)`.

Les sections « Nombre de trajets », « Distance moyenne » et « Pourboire moyen » doivent être traitées séparément lorsque la structure du document le permet.

### Étape 2 — Vérification des nouveaux chunks

Relancer :

```powershell
python .\nyc_taxi\check_rag_chunks.py
```

Vérifier que les titres, les formules et les explications métier restent associés.

### Étape 3 — Nouveaux tests de recherche

Relancer :

```powershell
python .\nyc_taxi\test_rag_search.py
```

Tester plusieurs formulations, comparer les documents retrouvés et vérifier si le passage pertinent apparaît en première position.

### Étape 4 — Optimisation

Après validation de la qualité de la recherche :
- éviter de recharger le modèle deux fois ;
- éviter de recalculer tous les embeddings à chaque question ;
- envisager de sauvegarder l'index FAISS et les métadonnées des chunks.

### Étape 5 — Génération de réponses

Une fois la recherche suffisamment fiable, intégrer un LLM pour produire une réponse à partir des passages retrouvés.

Cette étape permettra de passer d'un moteur de recherche documentaire à un système RAG complet.

## 8. État actuel du projet

Le chargement documentaire, le découpage en chunks, la création des embeddings, l'index FAISS et la recherche vectorielle fonctionnent.
La prochaine priorité est d'améliorer le découpage en tenant compte des titres Markdown, puis de vérifier si cette modification améliore le classement des résultats.
Le projet est donc actuellement à la phase d'amélioration de la qualité de la recherche documentaire, avant l'intégration de la génération de réponses.
