# Récapitulatif — Prototype RAG NYC Taxi

## 1. Objectif

Construire un assistant local capable de répondre aux questions techniques et métier sur le projet NYC Taxi à partir de sa documentation Markdown.

## 2. Environnement technique

- Python dans l'environnement Conda `D:\conda_envs\spark_local`
- Sentence Transformers pour transformer les textes en embeddings
- Modèle `paraphrase-multilingual-MiniLM-L12-v2`
- FAISS pour la recherche vectorielle
- Ollama pour exécuter un LLM local
- Qwen 2.5 3B pour générer les réponses
- API locale Ollama : `http://localhost:11434/api/generate`

Le modèle Qwen est stocké sur `D:\Ollama\Models`, afin de limiter l'utilisation de l'espace disque sur C:.

## 3. Fonctionnement de la recherche documentaire

Les fichiers Markdown du dossier `nyc_taxi/docs` constituent la base documentaire.

Les composants développés comprennent :
- `document_loader.py` : chargement des documents Markdown.
- `text_splitter.py` : découpage des documents en passages.
- `embedding_model.py` : création des embeddings.
- `embedding_index.py` : recherche des passages pertinents avec FAISS.
- `run_rag_search.py` : test de la recherche documentaire.

Les documents retrouvés comprennent notamment `data_model.md`, `architecture.md`, `powerbi_dashboard.md`, `powerbi_dashboard_rag_ameliore.md` et des fichiers de récapitulation.

## 4. Intégration du LLM

Le fichier `../../scripts` combine désormais la recherche FAISS et la génération de réponses par Qwen.

Le traitement est le suivant :
1. Recevoir une question.
2. Rechercher les cinq passages les plus pertinents.
3. Construire un contexte à partir de ces passages.
4. Envoyer la question et le contexte à Ollama.
5. Afficher la réponse générée.

La fonction `generate_answer()` utilise `requests` pour appeler l'API locale. La fonction `answer_question()` orchestre la recherche et la génération.

## 5. Tests effectués

Quatre types de questions ont été testés :
- Comptage SQL avec `COUNT(*)`.
- Comptage des lignes de `gold_fact_trips`.
- Nombre de courses dans Power BI avec `COUNTROWS`.
- Volume d'activité sur une période sélectionnée.

Les réponses SQL et DAX sont globalement correctes sur les exemples simples. La question sur une période révèle cependant des hallucinations : Qwen a inventé des tables, des colonnes et des dates non documentées.

## 6. État actuel

Le pipeline de base fonctionne : recherche vectorielle, assemblage du contexte, appel du modèle local et génération de texte.

Le prototype n'est pas encore suffisamment fiable pour être considéré comme finalisé. La priorité est de réduire les réponses non fondées, d'améliorer les tests et de vérifier la traçabilité des réponses vers les documents sources.


----


# Récapitulatif RAG — NYC Taxi (Session 4)

## 1. Objectif de la session

Faire fonctionner le pipeline RAG de bout en bout pour répondre à des questions sur le projet NYC Taxi à partir de sa documentation.

Le système doit :
1. recevoir une question en langage naturel ;
2. rechercher les passages pertinents dans les documents Markdown ;
3. transmettre les passages retrouvés au modèle Qwen ;
4. générer une réponse fondée sur le contexte documentaire.

## 2. Environnement utilisé

- **Projet :** `D:\data-ai-engineer-roadmap`
- **Environnement Python :** `D:\conda_envs\spark_local`
- **Script testé :** `../../scripts`
- **Modèle d'embeddings :** Sentence Transformers
- **Index vectoriel :** FAISS
- **LLM :** Qwen 2.5 3B via Ollama
- **Documents :** fichiers Markdown du dossier `nyc_taxi/docs`

Commande exécutée :

```powershell
python .\nyc_taxi\test_rag_answer.py
```

## 3. Résultat du test de bout en bout

**Le pipeline RAG fonctionne sur les quatre questions testées.**

Le système a retrouvé cinq passages pour chaque question, puis a transmis le contexte à Qwen pour produire une réponse.

### Question 1 — Compter les trajets avec SQL

**Question :** Quelle formule SQL utilise `COUNT(*)` pour compter les trajets ?

Réponse obtenue :

```sql
COUNT(*)
```

Sources retrouvées :
- `data_model.md` — score de similarité : 0.799
- `rag_learning_recap3.md` — score : 0.793

La réponse correspond à la documentation : `COUNT(*)` compte les lignes d'un résultat SQL.

### Question 2 — Compter les lignes de `gold_fact_trips`

**Question :** Comment compter les lignes de `gold_fact_trips` en SQL ?

Réponse obtenue :

```sql
SELECT COUNT(*)
FROM gold_fact_trips;
```

Le modèle a répondu directement avec `COUNT(*)`. La requête complète ci-dessus explicite la réponse sous forme de SQL exécutable.

Source principale : `data_model.md`, score de similarité de 0.815.

### Question 3 — Compter les courses dans Power BI

**Question :** Comment connaître le nombre de courses dans le tableau de bord Power BI ?

Réponse obtenue :

```dax
Nombre_Trajets =
COUNTROWS(gold_fact_trips)
```

Cette mesure DAX compte les lignes de la table `gold_fact_trips`.

La mesure dépend du contexte de filtre du rapport Power BI : les filtres de période et les autres filtres applicables influencent le résultat.

Sources principales :
- `architecture.md`
- `data_model.md`
- `powerbi_dashboard_rag_ameliore.md`

### Question 4 — Volume d'activité sur une période

**Question :** Quel est le volume d'activité sur la période sélectionnée ?

Réponse obtenue : utiliser la mesure `Nombre_Trajets`, fondée sur `COUNTROWS`, dont le résultat dépend notamment du filtre de période.

Cette réponse est cohérente avec le fonctionnement attendu du tableau de bord.

Pour rendre la réponse encore plus précise, on pourra documenter explicitement le nom de la mesure, la table utilisée et le rôle des filtres Power BI.

## 4. Comprendre les scores de similarité

Exemple de résultats :

| Document | Score |
|---|---:|
| `data_model.md` | 0.799 |
| `rag_learning_recap3.md` | 0.793 |
| `data_model.md` | 0.674 |

Le moteur vectoriel FAISS classe les passages selon leur proximité avec la question dans l'espace des embeddings.

Un score élevé indique ici une proximité sémantique plus importante. Il ne garantit toutefois pas que le passage soit exact ni que la réponse finale soit correcte.

Le modèle reçoit les passages sélectionnés et les utilise pour générer sa réponse.

## 5. Rôle des composants du RAG

| Composant | Rôle |
|---|---|
| Documents Markdown | Base de connaissances du projet |
| Document loader | Charge les fichiers de documentation |
| Text splitter | Découpe les documents en passages |
| Sentence Transformers | Transforme les passages et les questions en vecteurs |
| FAISS | Recherche les passages les plus proches de la question |
| Ollama | Exécute le modèle de langage localement |
| Qwen 2.5 3B | Génère la réponse à partir de la question et du contexte |

Le pipeline complet est donc :

```text
Question utilisateur
        |
        v
Création de l'embedding de la question
        |
        v
Recherche vectorielle FAISS
        |
        v
Sélection des 5 passages pertinents
        |
        v
Construction du contexte documentaire
        |
        v
Envoi à Qwen via Ollama
        |
        v
Réponse en langage naturel
```

## 6. Avertissement Hugging Face

Le terminal affiche :

```text
Warning: You are sending unauthenticated requests to the HF Hub.
```

Ce message indique que les requêtes vers Hugging Face sont effectuées sans jeton d'authentification.

Le chargement du modèle s'est néanmoins terminé correctement :

```text
199/199
```

L'avertissement n'a donc pas empêché l'exécution du test. Un jeton Hugging Face peut être utile pour bénéficier de limites de téléchargement plus élevées, mais il n'est pas nécessaire de corriger ce point pour valider le fonctionnement actuel.

## 7. Bilan de la session

Les quatre questions ont obtenu une réponse et le pipeline a exécuté les deux étapes essentielles :

- **RAG — Retrieval :** recherche de passages pertinents dans la documentation.
- **RAG — Generation :** production d'une réponse par Qwen à partir du contexte retrouvé.

Le projet sait maintenant répondre à des questions sur les formules SQL, le modèle de données et les mesures Power BI de NYC Taxi.

## 8. Prochaines améliorations

1. Ajouter des questions sur l'architecture Bronze, Silver et Gold.
2. Tester des questions dont la réponse est absente de la documentation, afin de vérifier que le modèle ne l'invente pas.
3. Améliorer les réponses en demandant à Qwen de citer le document utilisé.
4. Comparer les réponses générées avec les passages retrouvés.
5. Ajouter des tests automatisés sur la recherche documentaire et la génération.
6. Mesurer la qualité de la recherche : pertinence des cinq passages, qualité des réponses et temps d'exécution.

**Conclusion :** le RAG NYC Taxi fonctionne de bout en bout sur les quatre questions testées. La prochaine étape consiste à renforcer la fiabilité des réponses et à vérifier le comportement du système lorsque la documentation ne contient pas l'information demandée.
