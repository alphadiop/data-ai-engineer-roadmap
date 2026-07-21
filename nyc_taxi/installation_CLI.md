

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