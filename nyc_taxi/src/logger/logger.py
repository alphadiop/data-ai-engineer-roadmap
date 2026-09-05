import logging
from datetime import datetime
from pathlib import Path

from nyc_taxi.src.utils.config.load_config import load_config


class PipelineLogger:

    def __init__(
            self,
            name,
            env="local",
            periode=None,
            taxi_type=None,
            level=logging.INFO
    ):
        self.name = name
        self.env = env
        self.periode = periode
        self.taxi_type = taxi_type
        self.level = level
        self.path_log = None

        # ----------------------------------------------------------
        # Logger Python
        # ----------------------------------------------------------
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Évite les doublons / remontées vers le root logger
        self.logger.propagate = False

        # ----------------------------------------------------------
        # Configuration
        # ----------------------------------------------------------
        config = load_config(
            "variable_environnement",
            self.logger
        )

        # ==========================================================
        # DATABRICKS
        # ==========================================================
        if self.env == "databricks":

            # ------------------------------------------------------
            # Databricks gère déjà les logs d'exécution.
            # Pas de warehouse_dir
            # Pas de metastore_dir
            # Pas de path_logs obligatoire
            # ------------------------------------------------------

            root_log_dir = None

        # ==========================================================
        # LOCAL / WSL
        # ==========================================================
        else:

            if self.env not in config:
                raise ValueError(
                    f"Environment '{self.env}' not found "
                    f"in variable_environnement configuration."
                )

            if "path_logs" not in config[self.env]:
                raise KeyError(
                    f"'path_logs' is missing for environment "
                    f"'{self.env}' in variable_environnement."
                )

            root_log_dir = config[self.env]["path_logs"]

            self.path_log = self.get_path_logs(
                root_log_dir=root_log_dir,
                periode=periode,
                taxi_type=taxi_type
            )

        # ----------------------------------------------------------
        # Suppression des anciens handlers
        # ----------------------------------------------------------
        self.remove_handlers()

        # ----------------------------------------------------------
        # Formatter
        # ----------------------------------------------------------
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # ----------------------------------------------------------
        # Console
        # ----------------------------------------------------------
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

        self.handlers = [
            console_handler
        ]

        # ==========================================================
        # FILE HANDLER UNIQUEMENT EN LOCAL
        # ==========================================================
        if self.env != "databricks":

            file_handler = logging.FileHandler(
                self.path_log,
                mode="a",
                encoding="utf-8"
            )

            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

            self.handlers.append(file_handler)

        # ----------------------------------------------------------
        # Informations de démarrage
        # ----------------------------------------------------------
        self.info("=" * 120)
        self.info("PIPELINE LOGGER")
        self.info("=" * 120)
        self.info(f"environment      = {env}")
        self.info(f"periode          = {periode}")
        self.info(f"taxi_type        = {taxi_type}")

        if self.env == "databricks":
            self.info("logging_mode     = Databricks console")
        else:
            self.info(f"path_logs        = {root_log_dir}")
            self.info(f"log_file         = {self.path_log}")

        self.info("=" * 120)

    # ==================================================================
    # PATH
    # ==================================================================

    @staticmethod
    def get_path_logs(
            root_log_dir,
            periode=None,
            taxi_type=None
    ):
        """
        Construit le chemin du fichier de log.

        Exemple :

        logs/
        └── yellow/
            └── 2025/
                └── 202501_20260904_121530.log
        """

        if periode is None:

            path_log = Path(root_log_dir) / "pipeline.log"

            path_log.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            return str(path_log)

        # ----------------------------------------------------------
        # Validation
        # ----------------------------------------------------------

        periode = str(periode)

        if len(periode) != 6 or not periode.isdigit():
            raise ValueError(
                f"Invalid periode: {periode}. "
                f"Expected format YYYYMM."
            )

        if not taxi_type:
            raise ValueError(
                "taxi_type is required when periode is specified."
            )

        # ----------------------------------------------------------
        # Année
        # ----------------------------------------------------------

        annee = periode[:4]

        # ----------------------------------------------------------
        # Répertoire
        # ----------------------------------------------------------

        path_log = (
                Path(root_log_dir)
                / taxi_type
                / annee
        )

        path_log.mkdir(
            parents=True,
            exist_ok=True
        )

        # ----------------------------------------------------------
        # Timestamp lancement
        # ----------------------------------------------------------

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        # ----------------------------------------------------------
        # Fichier
        # ----------------------------------------------------------

        return str(
            path_log
            / f"{periode}_{timestamp}.log"
        )

    # ==================================================================
    # HANDLERS
    # ==================================================================

    def remove_handlers(self):
        """
        Supprime proprement tous les handlers existants.
        """

        for handler in self.logger.handlers[:]:

            try:
                handler.flush()
            except Exception:
                pass

            try:
                handler.close()
            except Exception:
                pass

            self.logger.removeHandler(handler)

    def flush(self):
        """
        Force l'écriture des logs en attente.
        """

        for handler in self.logger.handlers:

            try:
                handler.flush()
            except Exception:
                pass

    def close(self):
        """
        Ferme proprement le logger.
        """

        self.flush()
        self.remove_handlers()

    # ==================================================================
    # LOG METHODS
    # ==================================================================

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def exception(self, e):
        """
        Log une exception avec traceback complet.
        """

        self.logger.exception(e)
        self.flush()

    # ==================================================================
    # FINALIZE
    # ==================================================================

    def finalize(self, success: bool):
        """
        Finalise le fichier de log en local.

        En Databricks, aucun fichier n'est renommé :
        les logs restent dans les logs d'exécution Databricks.
        """

        self.flush()

        # ----------------------------------------------------------
        # Databricks
        # ----------------------------------------------------------

        if self.env == "databricks":

            status = "OK" if success else "NOOK"

            self.info("=" * 120)
            self.info(
                f"PIPELINE FINALIZED - STATUS = {status}"
            )
            self.info("=" * 120)

            return

        # ----------------------------------------------------------
        # Local
        # ----------------------------------------------------------

        extension = ".ok" if success else ".nook"

        current_path = Path(self.path_log)

        final_path = current_path.with_suffix(extension)

        # ----------------------------------------------------------
        # Fermer FileHandler
        # ----------------------------------------------------------

        for handler in self.logger.handlers[:]:

            try:
                handler.flush()
            except Exception:
                pass

            if isinstance(handler, logging.FileHandler):

                try:
                    handler.close()
                except Exception:
                    pass

                self.logger.removeHandler(handler)

        # ----------------------------------------------------------
        # Renommage
        # ----------------------------------------------------------

        if current_path.exists():

            current_path.rename(final_path)

            self.path_log = str(final_path)

        else:

            self.logger.warning(
                f"Log file not found: {current_path}"
            )

