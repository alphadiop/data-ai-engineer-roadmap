
#### Déploiement d'une plateforme Data Lakehouse Databricks avec Asset Bundles et orchestration de pipelines Spark."
✅ Databricks Asset Bundles  
✅ Delta Lake  
✅ Unity Catalog  
✅ Bronze / Silver / Gold  
✅ Jobs  
✅ Paramètres (--periode, --taxi_type)  
✅ Audit  
✅ Maintenance VACUUM  
✅ CI/CD possible avec GitHub Actions  

---
### Installation CLI
- [ ] ouvrir PowerShell en mode admin
- [ ] winget install Databricks.DatabricksCLI
- [ ] databricks -v
- [ ] databricks version


### configure CLI
- [ ] databricks auth logout --profile alphadiop
- [ ] databricks auth login --profile alphadiop --host https://dbc-8c847397-3c66.cloud.databricks.com
- [ ] databricks auth profiles
- [ ] databricks workspace list /
- [ ] databricks configure --profile alphadiop
---


### comment Databricks vérifie ton identité avant de t'autoriser à accéder à un workspace, un cluster, un job ou une API ?
- [ ] Pour chaque commande la CLI contacte l'API Databricks
- [ ] Databricks doit répondre à deux questions : Qui es-tu ? → Authentification et As-tu le droit de faire cela ? → Autorisation
- [ ] Exemple : Utilisateur -> alphadiop@gmail.com  Action -> lire le workspace


### Comprendre l'authentification
- [ ] PAT Token (Personal Access Token) : Tu crées un token puis la CLI l'utilise
- [ ] OAuth (recommandé aujourd'hui) : Aujourd'hui Databricks pousse OAuth.
- [ ] Azure CLI (si Azure Databricks)


### Créer un Token Databricks
- [ ] Avatar (en haut à droite)
- [ ] Settings
- [ ] Developer
- [ ] Access tokens
- [ ] Generate new token


#### OAuth (recommandé)
- [ ] databricks auth login
- [ ] La CLI ouvre un navigateur
    - [ ] Connexion Microsoft
    - [ ] Connexion Google
    - [ ] Connexion Databricks
- [ ] Une fois connecté, Databricks fournit un jeton OAuth : La CLI stocke ce jeton localement


* Principal (Pour les pipelines automatiques) : On ne veut pas utiliser un compte humain
* On crée alors : Service Principal qui agit comme un utilisateur technique


#### Exemple de pipelines automatiques
- [ ] GitHub Actions
- [ ] Azure DevOps
- [ ] Databricks Job
- [ ] 


#### Comment fonctionne un token ?
- [ ] Imagine un badge d'entreprise
- [ ] Au lieu de montrer ton passeport à chaque porte : Passeport -> vérification -> badge
- [ ] Ensuite : Badge -> ouverture de la porte
- [ ] Le token est ce badge


#### Où la CLI stocke les informations ?
- [ ] Sous Windows : C:\Users\<utilisateur>\.databrickscfg
- [ ] notepad $HOME\.databrickscfg


#### Les profils Databricks
- [ ] quand tu executes databricks auth profiles
- [ ] Chaque profil contient :
- [ ] host
- [ ] token ou OAuth
- [ ] databricks auth profiles


#### Variables d'environnement
- [ ] Tu peux aussi fournir les informations directement.
- [ ] Host : $env:DATABRICKS_HOST="https://xxx.cloud.databricks.com"
- [ ] Token : $env:DATABRICKS_TOKEN="dapi..."
- [ ] La CLI utilisera ces valeurs sans lire le fichier .databrickscfg


#### Pour diagnostiquer
- [ ] echo $env:DATABRICKS_HOST
- [ ] echo $env:DATABRICKS_TOKEN
- [ ] echo $env:DATABRICKS_CONFIG_PROFILE
- [ ] databricks auth env --profile alphadiop
- [ ] databricks workspace list /
- [ ] databricks workspace list /Workspace/Users
- [ ] databricks workspace list "/Workspace/Users/alphadiop@gmail.com"
- [ ] databricks workspace get-status "/Workspace/Users/alphadiop@gmail.com/Learning workspace"
- [ ] databricks workspace list "/Workspace/Users/alphadiop@gmail.com/Learning workspace"

| Commande                    | Rôle                                              |
| --------------------------- | ------------------------------------------------- |
| `workspace list PATH`       | Voir le contenu d'un dossier                      |
| `workspace get-status PATH` | Voir les informations du dossier/fichier lui-même |
| `workspace mkdirs PATH`     | Créer un dossier                                  |
| `workspace delete PATH`     | Supprimer un objet                                |
| `workspace import PATH`     | Importer un notebook/fichier                      |

* C'est un Databricks Repo, c'est-à-dire un dépôt Git connecté à GitHub, GitLab ou Azure DevOps.


### Résumé
- [ ] list → montre le contenu d'un dossier.
- [ ] get-status → montre les propriétés d'un objet.
- [ ] Ton objet "Learning workspace" est un REPO Git.
- [ ] Son identifiant Databricks est 4463873554004726.
- [ ] C'est probablement l'emplacement de ton projet NYC Taxi et de tes futurs Databricks Asset Bundles.
- [ ] databricks repos get 4463873554004726

### que fait cette commande : databricks auth login --profile dev --host https://dbc-8c847397-3c66.cloud.databricks.com
- [ ] Crée (ou met à jour) un profil nommé dev
- [ ] Lance une authentification OAuth
- [ ] Stocke le token de manière sécurisée
- [ ] Permet d'utiliser ce profil


### Test connexion
- [ ] databricks auth profiles
- [ ] databricks current-user me
- [ ] databricks workspace list /


#### Configurer la CLI
- [ ] affiche la valeur de la variable d'environnement DATABRICKS_CONFIG_PROFILE: echo $env:DATABRICKS_CONFIG_PROFILE
- [ ] databricks auth login --profile dev --host https://dbc-8c847397-3c66.cloud.databricks.com
- [ ] databricks auth login --profile alphadiop --host https://dbc-8c847397-3c66.cloud.databricks.com
- [ ] databricks auth describe -p dev
- [ ] databricks auth describe -p alphadiop
- [ ] Get-Content $HOME\.databrickscfg
- [ ] notepad $HOME\.databrickscfg
- [ ] diagnostiquer : Get-Content $HOME\.databrickscfg
- [ ] diagnostiquer : databricks auth profiles
- [ ] commande : databricks configure
- [ ] La CLI demande : 
    - [ ] Databricks Host : Tu mets l'URL de ton workspace
    - [ ] Token:cle token
- [ ] La CLI crée un fichier : C:\Users\<ton_user>\.databrickscfg
- [ ] accès à ce fichier : notepad $env:USERPROFILE\.databrickscfg
- [ ] databricks auth login --host https://dbc-8c847397-3c66.cloud.databricks.com
- [ ] Vérifier l'authentification alphadiop : databricks auth describe --profile alphadiop
- [ ] databricks auth profiles
- [ ] Supprime l'ancien profil : databricks auth logout --profile alphadiop
- [ ] Puis reconnecte : databricks auth login --profile alphadiop --host https://dbc-8c847397-3c66.cloud.databricks.com
- [ ] 

### Tester la connexion
- [ ] databricks workspace list /
- [ ] Importer un notebook : databricks workspace import `/Workspace/Users/alphadiop@gmail.com/test.py ` --file test.py
- [ ] Exporter un notebook : databricks workspace export `/Workspace/Users/alphadiop@gmail.com/test.py
- [ ] Voir les clusters : databricks clusters list
- [ ] Voir les jobs : databricks jobs list
- [ ] Lancer un job : databricks jobs run-now --job-id 123
- [ ] utiliser dev : databricks jobs list --profile dev
- [ ] databricks auth profiles
- [ ] 
- [ ] 
- [ ] 


### Déploiement avec la CLI
- [ ] Ton PC
- [ ] Databricks CLI
- [ ] Databricks Workspace
- [ ] Jobs Databricks
- [ ] Exemple : databricks workspace import-dir ./src /Workspace/Users/alphadiop@gmail.com/nyc_taxi/src
* Ton code local est envoyé dans Databricks.


``` text
nyc_taxi_bundle
│
├── databricks.yml
│
├── resources
│    └── jobs.yml
│
└── src
     ├── bronze.py
     ├── silver.py
     └── gold.py
```

### La CLI et Databricks Asset Bundles
- [ ] La CLI permet de créer un bundle 
- [ ] Valider : databricks bundle validate
- [ ] Déployer : databricks bundle deploy
- [ ] Lancer : databricks bundle run nyc_pipeline
- [ ] 


### Résumé du rôle de chaque outil
| Outil                | Rôle                                         |
| -------------------- | -------------------------------------------- |
| Databricks Workspace | Interface Web pour travailler                |
| Notebook             | Code interactif                              |
| Databricks CLI       | Piloter Databricks depuis terminal           |
| Asset Bundle         | Déployer une application Databricks complète |
| Job                  | Exécuter automatiquement un pipeline         |
| Git                  | Versionner le code                           |



### progression logique
1. Installer CLI ✅
2. Configurer connexion ✅
3. Tester workspace
4. Créer un bundle
5. Définir un Job Bronze/Silver/Gold
6. Déployer avec bundle
7. Automatiser avec CI/CD
---



#### commande
- [ ] notepad $env:USERPROFILE\.databrickscfg
- [ ] databricks jobs list --profile alphadiop
- [ ] databricks workspace list / --profile alphadiop
- [ ] databricks clusters list -> Erreur
- [ ] [System.Environment]::SetEnvironmentVariable("DATABRICKS_CONFIG_PROFILE","alphadiop","User")
- [ ] databricks auth logout --profile alphadiop
- [ ] databricks auth login --profile alphadiop --host https://dbc-8c847397-3c66.cloud.databricks.com
- [ ] databricks workspace list /



✓ GitHub  
✓ Databricks CLI  

→ Créer un premier Job Databricks  
→ Paramétrer la période  
→ Exécuter le pipeline via le Job  
→ Découvrir les Workflows  

Puis :  
→ Databricks Asset Bundles  
→ GitHub Actions (plus tard)  
→ CI/CD  

### Databricks CLI (Command Line Interface)
- [ ] piloter Databricks depuis un terminal (Windows PowerShell, Linux, Mac).
- [ ] automatiser les opérations que tu fais normalement dans l'interface Web Databricks.
- [ ] déployer du code avec Databricks Asset Bundles
- [ ] créer et lancer des Jobs
- [ ] gérer les notebooks
- [ ] gérer les fichiers Workspace
- [ ] appeler des API Databricks
- [ ] automatiser les déploiements CI/CD (GitHub Actions, Azure DevOps...)


### Installation CLI
- [ ] ouvrir PowerShell en mode admin
- [ ] winget install Databricks.DatabricksCLI
- [ ] databricks -v
- [ ] databricks version

#### Créer un Personal Access Token (PAT)
* dans databricks
- [ ] Clique sur ton profil (en haut à droite)
- [ ] Settings
- [ ] Developer
- [ ] Access Tokens
- [ ] Generate New Token
- [ ] Copie immédiatement le token

#### récuperer l'URL de databricks
- [ ] se connecter à databricks
- [ ] voir url dans barre url : https://dbc-8c847397-3c66.cloud.databricks.com/browse/folders/1161129702718992?o=7474654582545410
- [ ] sinon : dans notebooks, taper : spark.conf.get("spark.databricks.workspaceUrl")
- [ ] Get-ChildItem Env:DATABRICKS*
- [ ] 'dbc-8c847397-3c66.cloud.databricks.com'
- [ ] Remove-Item Env:DATABRICKS_TOKEN
- [ ] Remove-Item Env:DATABRICKS_HOST
- [ ] notepad $env:USERPROFILE\.databrickscfg
- [ ] databricks auth logout --profile alphadiop
- [ ] databricks auth logout --profile alphadiop
- [ ] databricks current-user me --profile alphadiop
- [ ] databricks current-user me --profile alphadiop
- [ ] databricks configure --profile alphadiop
- [ ] notepad $env:USERPROFILE\.databrickscfg
- [ ] databricks current-user me --profile alphadiop
- [ ] databricks auth profiles




#### Configurer la CLI
- [ ] databricks configure
- [ ] databricks bundle --help
** 463ef382f43a7576467fbd54d4042c469f528555b940dff977acfad45de16b6b
*** 463ef382f43a7576467fbd54d4042c469f528555b940dff977acfad45de16b6b