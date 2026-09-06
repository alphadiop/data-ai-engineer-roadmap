### BI
* [ ] SQL (requêtes, jointures, agrégations, fenêtres)
* [ ] Modélisation décisionnelle (étoile, flocon)
* [ ] Power BI (DAX, Power Query, rafraîchissement)
* [ ] Cas métier et KPI
* [ ] Performance et bonnes pratiques
````sql
````
### fenêtres : Structure générale
* [ ] fonction() OVER(PARTITION BY ... ORDER BY ...)
* [ ] PARTITION BY ... découpe les données en groupes
* [ ] ORDER BY ... définit l'ordre dans chaque groupe

* Les fonctions de fenêtrage permettent d'effectuer des calculs analytiques 
* sur un ensemble de lignes liées sans agréger les données comme le ferait un GROUP BY. 
* Je les utilise notamment pour les classements (ROW_NUMBER, RANK), les cumuls (SUM OVER), 
* les moyennes mobiles, ainsi que pour comparer une ligne avec la précédente 
* ou la suivante grâce à LAG et LEAD. 
* Dans mon projet NYC Taxi, elles servent par exemple à calculer les revenus cumulés, 
* identifier les trajets les plus rentables par jour et produire des KPI temporels destinés à Power BI.



### Point essentiel : 
* [ ] les dimensions servent à filtrer et analyser, la table de faits sert à mesurer
* [ ] Les dimensions décrivent qui / où / quand.
* [ ] une mesure DAX est recalculée automatiquement selon le contexte de filtre  
* [ ] Les faits décrivent combien / combien de fois / quelle distance


````sql
````

J'ai construit un modèle en étoile dans Power BI connecté à Databricks, 
avec une table de faits gold_fact_trips et des dimensions Date, Pickup Location et Dropoff Location. 
Les dimensions fournissent le contexte de filtrage et mes mesures DAX calculent dynamiquement 
les KPI comme le CA, le nombre de courses, la distance moyenne et la croissance 
selon le contexte de filtre. »

````sql
````
## Analyse temporelle
* [ ] LAG( : variation journalière
* [ ] LEAD() : variation mensuelle

````sql
````

````sql
````

````sql
````

### Quelle est la différence entre Power Query, DAX et SQL ?
* [ ] SQL : Extraction des données
* [ ] Power Query : Transformation ETL
* [ ] DAX : Calcul métier et KPI
````sql
````
````sql
````

### Pourquoi utiliser une fonction fenêtre plutôt qu'un GROUP BY ?
Avec un GROUP BY, on agrège les données et on perd le détail des lignes. 
Les fonctions de fenêtre permettent d'effectuer des 
calculs analytiques (classement, cumul, comparaison temporelle, total par groupe) 
tout en conservant les lignes d'origine. 
Elles sont très utiles pour les KPI et les analyses de tendance dans les projets BI.



### Pourquoi Devoteam ?
Devoteam est un acteur majeur du conseil en transformation digitale et data.  
Ce qui m'intéresse particulièrement est la diversité des missions  
et la possibilité d'intervenir sur des projets Data & Analytics à grande échelle.
Mon expérience en SQL, Power BI, Python et Data Engineering me permettrait d'être rapidement opérationnel 
chez vos clients tout en continuant à développer mes compétences.  
````sql
````
````sql
````

### Cas pratique
* Un directeur commercial vous dit : Je veux suivre mes ventes quotidiennes, mensuelles et annuelles.
* comment procedez-vous ?
  * identifier les sources
  * Construire un modèle en étoile
  * Créer une dimension Date
  * Développer les KPI
  * construire les tableaux de bord
````sql
Sales =
SUM(FactSales[Amount])

Sales MTD =
TOTALMTD(
    [Sales],
    DimDate[Date]
)

Sales YTD =
TOTALYTD(
    [Sales],
    DimDate[Date]
)
````
````sql
````



### Différence entre WHERE et HAVING
* [ ] WHERE filtre les lignes avant agrégation
* [ ] HAVING filtre les groupes après agrégation
````sql
SELECT customer_id,
       SUM(amount) AS total_sales
FROM sales
WHERE amount > 0
GROUP BY customer_id
HAVING SUM(amount) > 1000;
````



### INNER JOIN vs LEFT JOIN
* [ ] INNER JOIN uniquement les correspondance
* [ ] LEFT JOIN toutes les lignes de gauche même sans correspondance
````sql
SELECT c.customer_name,
       o.order_id
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;
````



### Trouver le top 3 des clients
````sql
SELECT customer_id,
       SUM(amount) total_sales
FROM sales
GROUP BY customer_id
ORDER BY total_sales DESC
LIMIT 3;
````

````sql
SELECT TOP 3
       customer_id,
       SUM(amount) total_sales
FROM sales
GROUP BY customer_id
ORDER BY total_sales DESC;
````
````sql
````


### ROW_NUMBER()
* [ ] dédoublonnage
* [ ] dernière commande par client

````sql
SELECT *,
       ROW_NUMBER() OVER(
           PARTITION BY customer_id
           ORDER BY order_date DESC
       ) rn
FROM orders;
````

### Différence entre RANK et DENSE_RANK
* [ ] RANK
* [ ] DENSE_RANK
````sql
````
````sql
````


### CTE
````sql
````
````sql
````


### Trouver les doublons
````sql
SELECT customer_id,
       COUNT(*)
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;
````


### Différence entre DELETE, TRUNCATE et DROP
* [ ] DELETE : supprimer les lignes
* [ ] TRUNCATE : vide la table
* [ ] DROP : supprime la table
````sql
````
````sql
````

## Partie Modélisation BI
### Quelle différence entre table de faits et dimensions
* [ ] Table de faits
* [ ] Dimensions
````sql
````

### Schéma en étoile : une table de faits entourée de dimensions
* [ ] plus performant
* [ ] plus simple à comprendre
* [ ] recommandé dans Power BI
````sql
          Dim_Date
              |
Dim_Customer--Fact_Sales--Dim_Product
              |
         Dim_Store
````
````sql
````


## Partie Power BI
### Différence entre mesure et colonne calculée
* [ ] Colonne calculée : calculée ligne par ligne 
  * la colonne est calculé lors du chargement
  * elle est Stockée dans le modèle
  * exemple : Margin = Sales[Revenue] - Sales[Cost]
* [ ] Mesure : 
  * elle est calculée à la demande
  * elle est Plus optimisée 
  * exemple : Total Sales = SUM(Sales[Revenue])
````sql
````



### CALCULATE
* Question très fréquente
* Sales France = CALCULATE(SUM(Sales[Amount]), Customer[Country] = "France")
* Permet de modifier le contexte de filtre.
````sql
````
### Qu'est-ce que le contexte de filtre ?
* Le contexte appliqué par :
  * slicers
  * filtres
  * visuels
  * lignes / colonnes
* exemple : Si je sélectionne 2025 : SUM(Sales[Amount])



### YTD
* Sales YTD = TOTALYTD(SUM(Sales[Amount]), DimDate[Date])
````sql
````


### Différence entre Power Query et DAX
* [ ] Power Query
  * ETL
  * nettoyage
  * transformation
* [ ] DAX
  * calcul métier
  * KPI
  * mesures



### Relations Power BI
* Cardinalité
  * One-to-One
  * One-to-Many
  * Many-to-One
  * Many-to-Many
````sql
````

````sql
````

````sql
````

````sql
````

````sql
````

````sql
````

````sql
````

````sql
````

````sql
````

````sql
````


### Comment optimiser un rapport Power BI lent ?
* [ ] Modèle en étoile
* [ ] Réduire le nombre de colonnes
* [ ] Utiliser des mesures plutôt que des colonnes calculées
* [ ] Eviter les relations many-to-many (reduction de la cardinalité)
* [ ] Agréger les données en amont
* [ ] Utiliser l'Incremental Refresh

#### Pourquoi éviter le Manu-to-Many
* [ ] ambiguïté des calculs 
* [ ] degradation des performances
* [ ] risque d'erreurs DAX


* [ ] ff

### Comment gérer un volume de plusieurs millions de lignes ?
* [ ] Data Warehouse
* [ ] Partitionnement
* [ ] Incremental Refresh
* [ ] Modèle en étoile
* [ ] Agrégations

### Expliquer un projet BI que tu as réalisé
J'ai développé une plateforme Data Engineering en Python, PySpark et Delta Lake.  
Les données NYC Taxi sont chargées dans une architecture Bronze / Silver / Gold.  
Les KPI sont exposés dans Power BI à partir des tables Gold.   
J'ai mis en place l'audit, la qualité des données, le partitionnement par période et l'automatisation des traitements  


### Quelle différence entre Power BI Import et DirectQuery ?
* [ ] Import
  * données chargées dans Power BI
  * très rapide
* [ ] DirectQuery
  * requêtes envoyées à la source
  * données en temps réel
  * moins performant
  * depend de la source

Orders
-------
* OrderID
* CustomerID
* Amount

#### Question : Afficher les clients ayant dépensé plus que la moyenne.
````sql
SELECT customer_id,
       SUM(amount) total_sales
FROM orders
GROUP BY customer_id
HAVING SUM(amount) >
(
    SELECT AVG(total_sales)
    FROM (
        SELECT SUM(amount) total_sales
        FROM orders
        GROUP BY customer_id
    ) t
);
````





