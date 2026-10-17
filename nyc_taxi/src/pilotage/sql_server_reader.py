import re

from pyspark.sql import DataFrame, SparkSession


class SqlServerReader:
    """
        Lecteur générique de tables SQL Server via JDBC.
    """

    def __init__(
        self,
        spark: SparkSession,
        server: str,
        database: str,
        user: str,
        password: str,
        port: int = 1433,
    ):
        self.spark = spark
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.port = port

        self.jdbc_url = (
            f"jdbc:sqlserver://{self.server}:{self.port};"
            f"databaseName={self.database};"
            "encrypt=true;"
            "trustServerCertificate=true;"
        )

    @staticmethod
    def _validate_identifier(value: str, name: str) -> str:
        """
        Vérifie qu'un nom de schéma ou de table est un identifiant SQL simple.
        """
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
            raise ValueError(
                f"{name} invalide : '{value}'. "
                "Utilise uniquement lettres, chiffres et underscore."
            )

        return value

    def read_table(
        self,
        table_name: str,
        schema: str = "dbo",
    ) -> DataFrame:
        """
        Lit une table SQL Server et retourne un DataFrame Spark.
        """

        schema = self._validate_identifier(schema, "schema")
        table_name = self._validate_identifier(table_name, "table_name")

        table = f"{schema}.{table_name}"

        return (
            self.spark.read
            .format("jdbc")
            .option("url", self.jdbc_url)
            .option("dbtable", table)
            .option("user", self.user)
            .option("password", self.password)
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
            .load()
        )

    def read_query(self, query: str) -> DataFrame:
        """
        Exécute une requête SQL Server et retourne un DataFrame Spark.
        """

        return (
            self.spark.read
            .format("jdbc")
            .option("url", self.jdbc_url)
            .option("query", query)
            .option("user", self.user)
            .option("password", self.password)
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
            .load()
        )