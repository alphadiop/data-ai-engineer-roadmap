import os
import sys
from pyspark.sql import SparkSession

PROJECT_ROOT = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/nyc_taxi/srcc"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    
from common.delta_manager import DeltaManager
from common.logger import PipelineLogger

class MaintenanceJob:
    """ attention :
            vacuum est lancé tous les jours car stockage limité avec l'édition free de databricks
            cela supprime les fichiers historiques de delta de 24h

            optimize periode est lancé tous les jours car stockage limité avec l'édition free de databricks
            cela compacte les fichiers delta pour diminuer la taille des fichiers
    """
    def __init__(self, spark: SparkSession, logger: PipelineLogger):
        self.spark = spark
        self.logger = logger
        

    def run(self):

        if self.logger:
            self.logger.info(
                "MaintenanceJob started"
            )

        delta_manager = DeltaManager(
            spark=self.spark,
            logger=self.logger
        )

        ## désactiver la vérification de la durée de conservation des fichiers delta car minimum 168h
        ## alors qu'ici je fais le choix de supprimer les fichiers delta après 24h

        for table_name in self.get_liste_tables():
            try:
                self.logger.info(
                    f"Processing {table_name}"
                )

                delta_manager.optimize_table(
                    table_name=table_name
                )
                    
                delta_manager.vacuum_dry_run(
                    table_name=table_name
                ).show(truncate=False)
                    
                delta_manager.vacuum(
                    table_name = table_name,
                    retain_hours = 24
                )
                
                self.logger.info(
                    f"Maintenance completed "
                    f"for {table_name}"
                )

            except Exception as e:
                self.logger.error(
                    f"Maintenance failed for "
                    f"{table_name}: {e}"
                )
        
        self.logger.info(
            "MaintenanceJob finished"
        )
 
        # "nyc_taxi.audit.audit_load",
        # "nyc_taxi.audit.audit_row_count"
        
    def get_liste_tables(self):
        return [
            "nyc_taxi.silver.silver_nyc_taxi", 
            "nyc_taxi.gold.gold_fact_trips",
            "nyc_taxi.gold.gold_dim_date", 
            "nyc_taxi.gold.gold_kpi_daily",
        ]