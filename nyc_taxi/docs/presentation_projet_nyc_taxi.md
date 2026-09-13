
J'ai construit un modèle en étoile dans Power BI connecté à Databricks, 
avec une table de faits gold_fact_trips et des dimensions Date, Pickup Location et Dropoff Location. 
Les dimensions fournissent le contexte de filtrage et mes mesures DAX calculent dynamiquement les KPI 
comme le CA, le nombre de courses, la distance moyenne et la croissance selon le contexte de filtre