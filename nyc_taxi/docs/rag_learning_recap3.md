# Récapitulatif — Apprentissage du RAG NYC Taxi

**Date : 20 octobre 2026**

## 1. Objectif

Construire progressivement un assistant RAG pour le projet NYC Taxi afin de répondre à des questions sur :
- l'architecture du projet ;
- le modèle de données ;
- les formules SQL ;
- les indicateurs Power BI ;
- les analyses de trajets et de chiffre d'affaires.

La priorité actuelle est de valider la recherche documentaire avant d'ajouter un LLM chargé de générer les réponses.

## 2. Environnement

- Dépôt : `D:\data-ai-engineer-roadmap`
- Projet : `D:\data-ai-engineer-roadmap\nyc_taxi`
- Environnement Python : `D:\conda_envs\spark_local`
- Documents : `nyc_taxi/docs/`
- Recherche : FAISS
- Embeddings : `sentence-transformers`
- Modèle : `paraphrase-multilingual-MiniLM-L12-v2`
- Dimension des vecteurs : 384

Bibliothèques installées :
- `sentence-transformers`
- `faiss-cpu`

## 3. Fonctionnement actuel

Le pipeline de recherche suit ces étapes :

1. **Chargement documentaire** : `document_loader.py` charge les fichiers Markdown.
2. **Découpage** : `text_splitter.py` divise les documents en chunks, en tenant compte des titres Markdown et des paragraphes.
3. **Vectorisation** : `embedding_model.py` transforme les textes en vecteurs numériques.
4. **Indexation** : `embedding_index.py` construit un index FAISS avec `IndexFlatIP`.
5. **Recherche** : la question est vectorisée, puis comparée aux vecteurs des chunks.
6. **Classement** : les chunks les plus similaires sont retournés avec leur source et leur score.

Les embeddings sont normalisés. L'index `IndexFlatIP` compare donc les vecteurs par produit scalaire, équivalent à la similarité cosinus pour ces vecteurs normalisés.

La fonction principale utilisée pour les tests est `search_documents(question, docs_dir, top_k=3)`.

## 4. Documents utilisés

Le dossier documentaire comprend notamment :
- `architecture.md`
- `data_model.md`
- `deployment.md`
- `powerbi_dashboard.md`
- `powerbi_dashboard_rag_ameliore.md`

Les fichiers `rag_assistant_roadmap.md` et `rag_learning_recap.md` sont exclus du chargement documentaire.

Le document `powerbi_dashboard_rag_ameliore.md` enrichit les explications sur les indicateurs Power BI et les formulations possibles des questions métier.

## 5. Améliorations réalisées

### A. Recherche SQL

Dans `data_model.md`, la section `### Nombre de trajets` a été enrichie avec une explication de `COUNT(*)` et des questions associées.

Exemple :

```sql
COUNT(*)
```

Cette modification améliore la récupération du passage correspondant aux questions sur le nombre de lignes et le nombre de trajets.

### B. Recherche Power BI

Le document `powerbi_dashboard_rag_ameliore.md` précise notamment que la mesure `Nombre_Trajets` utilise `COUNTROWS` et compte les lignes de `gold_fact_trips`.

```DAX
Nombre_Trajets =
COUNTROWS(gold_fact_trips)
```

Une précision a également été ajoutée à la section `### Activité` pour relier le volume d'activité à la période sélectionnée et aux filtres du tableau de bord.

## 6. Derniers résultats des tests

| Question | Document au rang 1 | Score |
|---|---|---:|
| Quelle formule SQL utilise COUNT(*) pour compter les trajets ? | `data_model.md` | 0,799 |
| Comment compter les lignes de gold_fact_trips en SQL ? | `data_model.md` | 0,815 |
| Comment connaître le nombre de courses dans le tableau de bord ? | `powerbi_dashboard_rag_ameliore.md` | 0,613 |
| Quel est le volume d'activité sur la période sélectionnée ? | `powerbi_dashboard_rag_ameliore.md` | 0,654 |

Le dernier test est une amélioration par rapport au score précédent de 0,603. Le passage récupéré au rang 1 mentionne `Nombre_Trajets`, `COUNTROWS`, `gold_fact_trips` et l'effet des filtres de période.

**Attention :** un score de similarité n'est pas un pourcentage de confiance ni une garantie que la réponse générée sera exacte. Il permet de comparer le classement des résultats entre différents tests.

## 7. Limites actuelles

- Le système récupère des passages, mais ne génère pas encore de réponse avec un LLM.
- La recherche repose uniquement sur la similarité vectorielle.
- La qualité des résultats dépend du contenu des documents et du découpage en chunks.
- Certains titres Markdown peuvent être séparés de leur explication par le découpage actuel.
- Le modèle est chargé à chaque appel à `search_documents`, même si les poids sont déjà en cache disque. Le modèle est réutilisé au sein d'une recherche pour encoder les documents et la question.

Le message Hugging Face indiquant que la requête est non authentifiée n'empêche pas les tests actuels.

## 8. Prochaine étape

Continuer à valider la pertinence des résultats, puis passer à la génération de réponses avec un LLM.

Étapes envisagées :

1. Vérifier plusieurs formulations métier différentes.
2. Examiner la qualité et la cohérence des chunks.
3. Évaluer si une recherche hybride, combinant recherche vectorielle et recherche lexicale, est nécessaire.
4. Choisir et intégrer un LLM.
5. Construire une réponse à partir des chunks récupérés, sans inventer d'informations absentes des documents.
6. Tester les réponses avec des questions connues et des cas où la documentation ne permet pas de répondre.

**Point de reprise :** la recherche vectorielle fonctionne sur les questions SQL et Power BI testées. La prochaine grande étape est de préparer la génération de réponses avec un LLM, sans modifier prématurément le pipeline Databricks existant.
