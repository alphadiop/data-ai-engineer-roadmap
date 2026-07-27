import os
import sys
from pyspark.sql import SparkSession

    
from nyc_taxi.src.common.delta_manager import DeltaManager

from nyc_taxi.src.common.catalog_manager import CatalogManager

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nyc_taxi.src.common.logger import PipelineLogger


class MaintenanceJob:
    """ attention :
            vacuum est lancé tous les jours car stockage limité avec l'édition free de databricks
            cela supprime les fichiers historiques de delta de 24h

            optimize periode est lancé tous les jours car stockage limité avec l'édition free de databricks
            cela compacte les fichiers delta pour diminuer la taille des fichiers
    """
    def __init__(self, spark: SparkSession, logger):
        self.spark = spark
        self.logger = logger
        

    def run(self, context):
        if self.logger:
            self.logger.info(
                "MaintenanceJob started"
            )

        catalog_manager = CatalogManager(
            spark = self.spark,
            logger=self.logger,
            env=context.env
        )
        delta_manager = DeltaManager(
            spark=self.spark,
            catalog_manager=catalog_manager,
            logger=self.logger
        )

        ## désactiver la vérification de la durée de conservation des fichiers delta car minimum 168h
        ## alors qu'ici je fais le choix de supprimer les fichiers delta après 24h

        tables = [
            ("silver", "silver_nyc_taxi"),
            ("gold", "gold_fact_trips"),
            ("gold", "gold_dim_date"),
            ("gold", "gold_kpi_daily")
        ]

        for schema_name, table_name in tables:
            try:
                self.logger.info(
                    f"Processing {schema_name}.{table_name}"
                )

                delta_manager.optimize_table(
                    schema_name=schema_name,
                    table_name=table_name
                )

                # VACUUM DRY RUN
                files = delta_manager.vacuum_dry_run(
                    schema_name,
                    table_name
                )

                count = files.count()

                self.logger.info(
                    f"{count} files can be removed"
                )

                # VACUUM réel
                delta_manager.vacuum(
                    schema_name,
                    table_name,
                    retain_hours=168
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
    #
    # def get_liste_tables(self):
    #     return [
    #         "nyc_taxi.silver.silver_nyc_taxi",
    #         "nyc_taxi.gold.gold_fact_trips",
    #         "nyc_taxi.gold.gold_dim_date",
    #         "nyc_taxi.gold.gold_kpi_daily",
    #     ]