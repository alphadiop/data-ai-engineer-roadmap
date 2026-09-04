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

        # ----------------------------------------------------------
        # Logger Python
        # ----------------------------------------------------------
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Évite que les logs remontent vers le root logger
        self.logger.propagate = False

        # ----------------------------------------------------------
        # Configuration
        # ----------------------------------------------------------
        config = load_config(
            "variable_environnement",
            self.logger
        )

        root_log_dir = config[env]["path_logs"]

        # ----------------------------------------------------------
        # Chemin du fichier de log
        # ----------------------------------------------------------
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

        # ----------------------------------------------------------
        # Fichier
        # ----------------------------------------------------------
        file_handler = logging.FileHandler(
            self.path_log,
            mode="a",
            encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # ----------------------------------------------------------
        # Ajout des handlers
        # ----------------------------------------------------------
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        self.handlers = [
            console_handler,
            file_handler
        ]

        # ----------------------------------------------------------
        # Informations de démarrage
        # ----------------------------------------------------------
        self.info("=" * 120)
        self.info("PIPELINE LOGGER")
        self.info("=" * 120)
        self.info(f"environment      = {env}")
        self.info(f"periode          = {periode}")
        self.info(f"taxi_type        = {taxi_type}")
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

        # ----------------------------------------------------------
        # Aucun contexte de période
        # ----------------------------------------------------------
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


    def finalize(self, success: bool):
        """
        Renomme le fichier de log avec l'extension finale
        .ok ou .nook selon le statut du pipeline.
        """
        self.flush()
        extension = ".ok" if success else ".nook"
        current_path = Path(self.path_log)
        final_path = current_path.with_suffix(extension)

        # Fermer le FileHandler avant de renommer le fichier
        for handler in self.logger.handlers[:]:
            try:
                handler.flush()
            except Exception:
                pass

            if isinstance(handler, logging.FileHandler):
                handler.close()
                self.logger.removeHandler(handler)

        current_path.rename(final_path)
        self.path_log = str(final_path)