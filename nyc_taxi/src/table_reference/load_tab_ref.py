
from pathlib import Path



from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.common.pipeline_step import PipelineStep
from nyc_taxi.src.common.pipeline_context import PipelineContext

class ReferenceDataLoader(PipelineStep):

    def __init__(
            self,
            spark,
            env="local",
            logger=None
    ):
        super().__init__(
            spark,
            self.__class__.__name__
        )

        self.spark = spark
        self.env = env
        self.logger = logger

        self.catalog_manager = CatalogManager(
            spark=spark,
            env=env,
            logger=logger
        )

    def run(self, context:PipelineContext):

        schema_name = "ref"
        table_name = "dim_location"

        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name=schema_name,
                table_name=table_name
            )
        )

        self.logger.info("=" * 80)
        self.logger.info("REFERENCE DATA LOADER")
        self.logger.info("=" * 80)

        self.logger.info(
            f"Table de référence : {full_table_name}"
        )

        # ======================================================
        # VERIFICATION : TABLE DEJA EXISTANTE
        # ======================================================

        if self.spark.catalog.tableExists(full_table_name):

            self.logger.info(
                f"Table {full_table_name} existe déjà."
            )

            self.logger.info(
                "Chargement CSV ignoré."
            )

            return

        # ======================================================
        # CHEMIN CSV
        # ======================================================

        csv_path = Path(
            context.config["ref_path"]
        )

        self.logger.info(
            f"CSV dim_location : {csv_path}"
        )

        if not csv_path.exists():

            raise FileNotFoundError(
                f"Fichier de référence introuvable : "
                f"{csv_path}"
            )

        # ======================================================
        # LECTURE CSV
        # ======================================================

        self.logger.info(
            "Lecture du fichier CSV..."
        )

        df = (
            self.spark.read
            .option("header", "true")
            .option("inferSchema", "true")
            .option("encoding", "UTF-8")
            .csv(str(csv_path))
        )

        self.logger.info(
            f"Colonnes CSV : {df.columns}"
        )

        # ======================================================
        # CONTROLE
        # ======================================================

        row_count = df.count()

        self.logger.info(
            f"Nombre de lignes CSV : {row_count}"
        )

        if row_count == 0:

            raise ValueError(
                f"Le fichier {csv_path} est vide."
            )

        # ======================================================
        # ECRITURE DELTA
        # ======================================================

        self.logger.info(
            f"Création de {full_table_name}"
        )

        (
            df.write
            .format("delta")
            .mode("overwrite")
            .saveAsTable(full_table_name)
        )

        self.logger.info(
            f"Table {full_table_name} créée avec "
            f"{row_count} lignes."
        )

        self.logger.info("=" * 80)
        self.logger.info(
            "REFERENCE DATA LOADER terminé"
        )
        self.logger.info("=" * 80)
