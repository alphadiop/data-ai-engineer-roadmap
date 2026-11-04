
import builtins

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.column import Column
from pyspark.sql import functions as F

from nyc_taxi.src.common.pipeline_step import PipelineStep
from nyc_taxi.src.logger.logger import PipelineLogger
from nyc_taxi.src.common.decorators import log_execution
from nyc_taxi.src.common.schema_manager import SchemaManager
from nyc_taxi.src.common.path_manager import PathManager
from nyc_taxi.src.utils.load_json import load_json
from nyc_taxi.src.common.pipeline_context import PipelineContext

class UberSilver(PipelineStep):
    """Transformation Silver et contrôles qualité des courses NYC Taxi."""

    def __init__(
        self,
        spark: SparkSession,
        logger: PipelineLogger,
    ):
        super().__init__(spark, self.__class__.__name__)

        self.spark: SparkSession = spark
        self.logger: PipelineLogger = logger
        self._accepted_rows: int = 0

        self.spark.conf.set(
            "spark.sql.legacy.timeParserPolicy",
            "LEGACY",
        )

    @log_execution
    def cast_columns(self, df: DataFrame) -> DataFrame:
        """ Standardise les types des colonnes """

        types = {
            "tpep_pickup_datetime": "timestamp",
            "tpep_dropoff_datetime": "timestamp",
            "passenger_count": "bigint",
            "payment_type": "tinyint",
            "trip_distance": "decimal(19,5)",
            "fare_amount": "decimal(19,5)",
            "tip_amount": "decimal(19,5)",
            "total_amount": "decimal(19,5)",
        }

        return df.select(
            *[
                F.col(name).cast(types[name]).alias(name)
                if name in types
                else F.col(name)
                for name in df.columns
            ]
        )


    def add_trip_features(self, df: DataFrame) -> DataFrame:
        """Calcule les caractéristiques temporelles des courses."""

        expressions = {
            "trip_duration_minute": F.expr("""
                ROUND(
                    (
                        UNIX_TIMESTAMP(tpep_dropoff_datetime)
                        - UNIX_TIMESTAMP(tpep_pickup_datetime)
                    ) / 60.0,
                    3
                )
            """),

            "trip_date": F.expr("""
                YEAR(tpep_pickup_datetime) * 10000
                + MONTH(tpep_pickup_datetime) * 100
                + DAYOFMONTH(tpep_pickup_datetime)
            """),

            "tip_percent": F.expr("""
                ROUND(
                    CASE
                        WHEN fare_amount > 0
                        THEN tip_amount / fare_amount * 100
                        ELSE NULL
                    END,
                    2
                )
            """),

            "pickup_hour": F.expr(
                "HOUR(tpep_pickup_datetime)"
            ),

            "pickup_day_of_week": F.expr(
                "DAYOFWEEK(tpep_pickup_datetime)"
            ),

            "pickup_month": F.expr(
                "MONTH(tpep_pickup_datetime)"
            ),

            "pickup_year": F.expr(
                "YEAR(tpep_pickup_datetime)"
            ),
        }

        return df.withColumns(expressions)



    @log_execution
    def add_derived_metrics(self, df: DataFrame) -> DataFrame:
        """Calcule les indicateurs dérivés."""

        expressions = {
            "average_speed": F.round(
                F.expr("""
                    CASE
                        WHEN trip_duration_minute > 0
                        THEN trip_distance / (trip_duration_minute / 60.0)
                        ELSE NULL
                    END
                """),
                2,
            ),
        }
        return df.withColumns(expressions)


    def build_quality_rules(
            self,
            date_debut: Column,
            date_fin: Column,
    ) -> dict[str, Column]:
        """Définit les règles de rejet par ordre de priorité."""

        date_debut_sql = date_debut
        date_fin_sql = date_fin

        return {
            "date_pickup_absente": F.expr(
                "tpep_pickup_datetime IS NULL"
            ),
            "date_anterieure": (
                    F.col("tpep_pickup_datetime") < date_debut_sql
            ),
            "date_posterieur": (
                    F.col("tpep_pickup_datetime") >= date_fin_sql
            ),
            "date_dropoff_absente": F.expr(
                "tpep_dropoff_datetime IS NULL"
            ),
            "date_incoherente": F.expr(
                "tpep_dropoff_datetime < tpep_pickup_datetime"
            ),
            "duree_invalide": F.expr(
                """
                trip_duration_minute IS NULL
                OR trip_duration_minute <= 0
                OR trip_duration_minute >= 1400
                """
            ),
            "distance_invalide": F.expr(
                """
                trip_distance IS NULL
                OR trip_distance <= 0
                """
            ),
            "ca_absent": F.expr(
                "total_amount IS NULL"
            ),
            "ca_negatif": F.expr(
                "total_amount < 0"
            ),
            "ca_nul": F.expr(
                "total_amount = 0"
            ),
        }




    @log_execution
    def add_rejection_status(
        self,
        df: DataFrame,
        periode_a_charger: str,
    ) -> DataFrame:
        """Ajoute la période et le statut de rejet."""

        if (
            len(periode_a_charger) != 6
            or not periode_a_charger.isdigit()
            or int(periode_a_charger[:4]) < 1
            or not 1 <= int(periode_a_charger[4:]) <= 12
        ):
            raise ValueError(
                "La période doit être au format YYYYMM, "
                "par exemple 202505."
            )

        date_debut = F.to_timestamp(
            F.lit(
                f"{periode_a_charger[:4]}-"
                f"{periode_a_charger[4:]}-01 00:00:00"
            )
        )

        date_fin = F.add_months(date_debut, 1)

        rules = self.build_quality_rules(
            date_debut,
            date_fin,
        )

        status_expression: Column | None = None

        for status, condition in rules.items():
            if status_expression is None:
                status_expression = F.when(
                    condition,
                    F.lit(status),
                )
            else:
                status_expression = status_expression.when(
                    condition,
                    F.lit(status),
                )

        if status_expression is None:
            raise RuntimeError(
                "Aucune règle de qualité n'a été définie."
            )

        return df.withColumns({
            "statut_rejet": status_expression.otherwise(
                F.lit("valid")
            ),
        })



    @log_execution
    def apply_quality_rules(
            self,
            df: DataFrame,
            periode_a_charger: str,
    ) -> dict[str, DataFrame]:
        """ Retourne les DataFrames valides et rejetés après contrôle qualité """

        self.logger.subsection("SILVER QUALITY CONTROLS")

        # Ajouter le statut de rejet selon les règles de qualité.
        df_controle = self.add_rejection_status(
            df,
            periode_a_charger,
        )

        # Une seule agrégation pour compter les lignes par statut.
        df_status = (
            df_controle
            .groupBy("statut_rejet")
            .count()
            .orderBy("statut_rejet")
        )

        status_counts = {
            row["statut_rejet"]: row["count"]
            for row in df_status.collect()
        }

        # Calculer les volumes.
        total = builtins.sum(status_counts.values())
        accepted = status_counts.get("valid", 0)
        rejected = total - accepted

        # Conserver le nombre de lignes acceptées pour run().
        self._accepted_rows = accepted

        # Séparer les lignes valides et rejetées.
        df_valid = df_controle.filter(
            F.col("statut_rejet") == "valid"
        )

        df_rejete = df_controle.filter(
            F.col("statut_rejet") != "valid"
        )

        # Afficher la répartition des statuts dans les logs.
        repartition = "\n".join(
            f"  {status}: {count:,}".replace(",", " ")
            for status, count in sorted(status_counts.items())
        )

        self.logger.info(
            f"Répartition des statuts de qualité :\n{repartition}"
        )

        # Produire le rapport de qualité.
        self.logger.separator("SILVER QUALITY REPORT")

        self.logger.metric(
            "Input rows",
            f"{total:,}".replace(",", " "),
        )
        self.logger.metric(
            "Accepted rows",
            f"{accepted:,}".replace(",", " "),
        )
        self.logger.metric(
            "Rejected rows",
            f"{rejected:,}".replace(",", " "),
        )

        if total > 0:
            self.logger.metric(
                "Rejection rate",
                f"{rejected / total * 100:.2f}%",
            )

        self.logger.success("Silver quality controls completed")

        return {
            "df_valid": df_valid,
            "df_rejete": df_rejete,
        }


    @log_execution
    def run(self, context:PipelineContext) -> DataFrame:
        """Exécute les transformations Silver."""

        self.logger.subsection("SILVER TRANSFORMATION")

        if context.df_bronze is None:
            raise ValueError(
                "Le DataFrame Bronze est absent du contexte."
            )

        if context.taxi_type is None:
            raise ValueError(
                "Le type de taxi est absent du contexte."
            )

        if context.periode is None:
            raise ValueError(
                "La période est absente du contexte."
            )

        df_bronze: DataFrame = context.df_bronze

        # 1. Standardisation des types.
        df_silver: DataFrame = self.cast_columns(df_bronze)

        # 2. Calcul des caractéristiques des courses.
        df_silver: DataFrame = self.add_trip_features(df_silver)

        # 3. Calcul des indicateurs dérivés.
        df_silver: DataFrame = self.add_derived_metrics(df_silver)

        # 4. Application des règles qualité.
        quality_result: dict[str, DataFrame] = self.apply_quality_rules(
            df_silver,
            str(context.periode),
        )

        df_silver:DataFrame = quality_result["df_valid"]
        df_rejete:DataFrame= quality_result["df_rejete"]

        df_rejete = (
            df_rejete
            .select(
                *df_bronze.columns,
                "statut_rejet",
            )
        )

        df_silver = df_silver.drop("statut_rejet")

        # 5. Application du schéma cible Silver.
        path_manager = PathManager(context=context)

        schema_file = path_manager.schema_path(
            taxi_type=context.taxi_type,
            table_name="silver_nyc_taxi",
        )

        schema_json = load_json(schema_file)

        schema_manager = SchemaManager(
            spark=self.spark,
            logger=self.logger
        )

        df_silver = schema_manager.apply_schema(
            df=df_silver,
            schema_json=schema_json
        )

        # 6. Mise à jour du contexte.
        context.df_silver = df_silver

        context.df_rejete = df_rejete

        context.row_count["silver"] = self._accepted_rows

        self.logger.metric(
            "Final Silver rows",
            f"{self._accepted_rows:,}".replace(",", " "),
        )

        self.logger.success("Silver transformation completed")
        return df_silver
