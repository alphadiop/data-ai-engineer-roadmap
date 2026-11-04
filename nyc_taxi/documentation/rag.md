# Assistant RAG du projet NYC Taxi

## 1. Objectif

Le prototype RAG permet de poser des questions sur la documentation du projet NYC Taxi. Il combine une recherche de passages documentaires et un modèle de langage local chargé de formuler une réponse à partir des passages récupérés.

Le RAG n'interroge pas automatiquement les tables Databricks et ne vérifie pas l'exécution d'une requête SQL. Il répond à partir des documents indexés et du contexte qui lui est transmis.

## 2. Chaîne de traitement

```text
Fichiers Markdown de référence
          |
          v
Chargement des documents
          |
          v
Découpage en passages (chunks)
          |
          v
Embeddings vectoriels
          |
          v
Index FAISS
          |
Question -> embedding de la question
          |
          v
Recherche des passages similaires
          |
          v
Assemblage du contexte
          |
          v
Ollama / Qwen2.5 3B
          |
          v
Réponse générée
```

## 3. Chargement documentaire

Le dossier documentaire prévu pour le RAG est `nyc_taxi/documentation/`. Il contient les documents de référence :
- `README.md`
- `architecture.md`
- `data_model.md`
- `pipeline.md`
- `business_rules.md`
- `powerbi_dashboard.md`
- `rag.md`

Le code du chargeur doit pointer explicitement vers ce dossier. Les anciennes notes, comptes rendus et feuilles de route doivent être exclues de l'index de référence, sauf décision explicite de les rendre consultables. Cela évite que des explications historiques ou des versions concurrentes soient traitées comme des faits courants.

## 4. Découpage et embeddings

Le code du prototype comprend des modules pour charger les documents Markdown, les découper en passages, créer les embeddings et construire l'index. Le modèle d'embeddings utilisé est `paraphrase-multilingual-MiniLM-L12-v2`, qui produit des vecteurs de 384 dimensions.

Les paramètres de découpage — taille, chevauchement et traitement des titres — doivent être documentés à partir de `text_splitter.py`. Ils ne sont pas fixés dans ce document car ils doivent correspondre au code réellement exécuté.

## 5. Recherche vectorielle

FAISS sert à rechercher les passages les plus proches du vecteur de la question. Le script de test utilise actuellement `top_k=5`, donc il récupère jusqu'à cinq passages candidats.

Un score de similarité mesure la proximité selon la méthode d'indexation ; il ne garantit pas que le passage réponde correctement à la question. La pertinence doit être évaluée sur un jeu de questions représentatives. Les doublons, passages redondants et documents obsolètes peuvent dégrader le contexte transmis au modèle.

## 6. Génération de réponse

Le prototype appelle l'API locale Ollama à l'adresse `http://localhost:11434/api/generate` avec le modèle `qwen2.5:3b`.

Le prompt demande au modèle de répondre en français, de s'appuyer sur le contexte, de distinguer SQL et DAX et de signaler les informations manquantes. Ces instructions réduisent certains risques mais ne garantissent pas l'absence d'hallucinations.

Le modèle ne doit pas inventer :
- de tables, colonnes ou clés ;
- de jointures non documentées ;
- de dates ou exemples de résultats présentés comme réels ;
- de règles métier non présentes dans les sources.

Si les documents ne suffisent pas, la réponse attendue doit indiquer clairement que la documentation ne permet pas de répondre précisément. Pour une question sur une période sélectionnée dans Power BI, ne pas proposer une jointure SQL ou une dimension non documentée.

## 7. Scripts de test

Les scripts de test connus comprennent :
- `test_rag_search.py` : teste la recherche de passages et affiche les sources et scores ;
- `test_rag_answer.py` : enchaîne la recherche et la génération par Ollama.

Les questions de test couvrent notamment :
- la formule SQL utilisant `COUNT(*)` ;
- le comptage des lignes de `gold_fact_trips` ;
- le nombre de trajets dans Power BI ;
- l'interprétation du volume d'activité sur une période sélectionnée.

Les tests ont montré que le prototype peut répondre à des questions simples, mais qu'il peut aussi produire des détails non documentés. La fiabilité du contexte et l'abstention lorsque les sources sont insuffisantes restent des axes de travail.

## 8. Procédure de mise à jour documentaire

Quand un document de référence change :
1. vérifier les faits et les formules ;
2. reconstruire ou actualiser les embeddings et l'index selon l'implémentation ;
3. exécuter les tests de recherche ;
4. exécuter les tests de génération ;
5. vérifier que les sources affichées soutiennent effectivement les réponses.

Le mode de persistance de l'index FAISS doit être confirmé dans le code. Si l'index est reconstruit à chaque lancement, documenter le coût de chargement ; s'il est persisté, documenter le chemin et la procédure d'actualisation.

## 9. Critères de validation

Le prototype est prêt pour une démonstration technique lorsque :
- les documents indexés sont les documents de référence ;
- les passages pertinents apparaissent dans les premiers résultats ;
- les réponses distinguent correctement SQL et DAX ;
- les réponses restent dans les limites du contexte ;
- l'assistant reconnaît les informations manquantes ;
- les erreurs Ollama, délais d'attente et résultats de recherche insuffisants sont gérés ;
- les tests sont reproductibles et les sources sont visibles.

## 10. Limites

Ce prototype est un assistant documentaire, pas un agent qui exécute ou valide automatiquement les requêtes dans Databricks. Les scores de recherche et la formulation du modèle ne remplacent ni les tests SQL, ni l'inspection du schéma, ni la validation métier.
