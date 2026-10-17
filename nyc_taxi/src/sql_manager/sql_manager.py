
import os
import urllib.parse

import sqlalchemy as sa
from sqlalchemy import text

from nyc_taxi.src.logger.logger import PipelineLogger
from nyc_taxi.src.utils.config.load_config import load_config


class SQLManager:
    """Gère les connexions SQL Server avec SQLAlchemy et pyodbc."""

    def __init__(
        self,
        env: str,
        server_name: str,
        odbc_driver: str | None = None,
        connect_args: dict | None = None,
        logger: PipelineLogger | None = None,
    ):
        self.logger = logger
        self.server_name = server_name
        self.env = env
        self.engine = None
        self.connexion = None

        self.config = load_config(
            file_name="variable_environnement",
            env=self.env,
            logger=self.logger,
        )

        print(self.config)
        # server_name correspond au nom du profil dans le YAML.
        self.db_config = (
            self.config
            .get(self.env, {})
            .get("sql_server", {})
            .get("profiles", {})
            .get(self.server_name)
        )

        if not self.db_config:
            raise ValueError(
                f"Profil SQL Server introuvable : {self.server_name}"
            )

        if self.db_config.get("enabled") is False:
            raise ValueError(
                f"Le profil SQL Server '{self.server_name}' est désactivé."
            )

        # Conserve la possibilité de remplacer le driver depuis le code.
        if odbc_driver:
            self.db_config["odbc_driver"] = odbc_driver

        self.db_config.setdefault(
            "odbc_driver",
            self.db_config.get("driver"),
        )

        if not self.db_config.get("odbc_driver"):
            raise ValueError(
                f"Driver ODBC absent du profil '{self.server_name}'."
            )

        self.engine = self._build_engine(connect_args or {})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and self.logger:
            self.logger.exception(exc_val)

        self.close()
        return False

    def _read_secret(self, name: str) -> str:
        """ Lit un secret dont le nom de variable est indiqué dans le YAML."""
        env_name = self.db_config.get(f"{name}")
        if not env_name:
            raise ValueError(
                f"Le profil '{self.server_name}' doit définir "
                f"'{name}'."
            )

        value = os.getenv(env_name)

        print(f"value : {value}")
        if not value:
            raise RuntimeError(
                f"La variable d'environnement '{env_name}' n'est pas définie."
            )

        return value


    def _build_engine(self, connect_args: dict):
        host = self.db_config.get("host") or self.db_config.get("server")
        database = self.db_config.get("database")

        if not host or not database:
            raise ValueError(
                f"Les champs 'host' et 'database' sont requis "
                f"dans le profil '{self.server_name}'."
            )

        port = self.db_config.get("port")
        server = f"{host},{port}" if port else host

        connection_string = (
            f"DRIVER={{{self.db_config['odbc_driver']}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"Encrypt={self.db_config.get('encrypt', 'yes')};"
            f"TrustServerCertificate="
            f"{self.db_config.get('trust_server_certificate', 'no')};"
        )

        if self.db_config.get("trusted_connection", False):
            connection_string += "Trusted_Connection=yes;"
        else:
            username = self.db_config['username']
            password = self.db_config['password']
            connection_string += (
                f"UID={username};"
                f"PWD={password};"
            )

        if self.logger:
            self.logger.info(
                f"SQL CONNECT → profil={self.server_name}, "
                f"serveur={host}, base={database}"
            )

        odbc = urllib.parse.quote_plus(connection_string)

        return sa.create_engine(
            f"mssql+pyodbc:///?odbc_connect={odbc}",
            connect_args=connect_args,
            pool_pre_ping=True,
            fast_executemany=True,
        )

    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            if self.logger:
                self.logger.info(
                    f"Connexion OK : {self.server_name}"
                )

            return True

        except Exception as e:
            if self.logger:
                self.logger.exception(e)
            return False

    def get_sql_connexion(self):
        if self.connexion is None or self.connexion.closed:
            self.connexion = self.engine.connect()

        return self.connexion

    def transaction(self):
        return self.get_sql_connexion().begin()

    def commit(self, transaction):
        transaction.commit()

    def rollback(self, transaction):
        transaction.rollback()

    def execute_query(self, query: str, params=None):
        with self.engine.begin() as conn:
            conn.execute(text(query), params or {})

    def fetch_all(self, query: str, params=None):
        with self.engine.connect() as conn:
            return conn.execute(
                text(query), params or {}
            ).fetchall()

    def fetch_one(self, query: str, params=None):
        with self.engine.connect() as conn:
            return conn.execute(
                text(query), params or {}
            ).fetchone()

    def scalar(self, query: str, params=None):
        with self.engine.connect() as conn:
            return conn.execute(
                text(query), params or {}
            ).scalar()

    def close(self):
        if self.connexion is not None and not self.connexion.closed:
            self.connexion.close()

        if self.engine is not None:
            self.engine.dispose()


if __name__ == "__main__":
    from nyc_taxi.src.logger.logger import PipelineLogger

    env = "local"
    periode = 202411
    taxi_type = "yellow"

    logger = PipelineLogger(
        name="pipeline_runner",
        env=env,
        periode=periode,
        taxi_type=taxi_type,
    )

    with SQLManager(
        env=env,
        server_name="dw_prod",
        odbc_driver="ODBC Driver 17 for SQL Server",
        logger=logger,
    ) as sql:
        if sql.test_connection():
            rows = sql.fetch_all(
                """
                SELECT TOP 2 *
                FROM Sales.SalesOrderHeader
                """
            )
            logger.info(rows)


