import os
import sys
import socket
import getpass
import platform
import logging

import pyspark
import delta


class SparkEnvironmentLogger:

    def __init__(
            self,
            spark,
            config,
            env,
            logger=None
    ):
        self.spark = spark
        self.config = config
        self.env = env
        self.logger = logger or logging.getLogger(__name__)

    def log_environment(self):

        self.logger.info("=" * 120)
        self.logger.info("SPARK ENVIRONMENT")
        self.logger.info("=" * 120)

        self.logger.info(f"environment          = {self.env}")
        self.logger.info(f"user                 = {getpass.getuser()}")
        self.logger.info(f"hostname             = {socket.gethostname()}")

        self.logger.info("-" * 120)

        self.logger.info(f"platform             = {platform.platform()}")
        self.logger.info(f"system               = {platform.system()}")
        self.logger.info(f"release              = {platform.release()}")

        self.logger.info("-" * 120)

        self.logger.info(f"python_version       = {platform.python_version()}")
        self.logger.info(f"python_executable    = {sys.executable}")

        self.logger.info("-" * 120)

        self.logger.info(f"pyspark_version      = {pyspark.__version__}")
        self.logger.info(f"spark_version        = {self.spark.version}")
        self.logger.info(f"sparkContext.maste   = {self.spark.sparkContext.master}")


        try:
            self.logger.info(
                f"delta_version        = {delta.__version__}"
            )
        except Exception:
            self.logger.info(
                "delta_version        = unknown"
            )

        self.logger.info("-" * 120)

        self.logger.info(
            f"warehouse_conf       = "
            f"{self.spark.conf.get('spark.sql.warehouse.dir')}"
        )

        self.logger.info(
            f"warehouse_yaml       = "
            f"{self.config['local']['warehouse_dir']}"
        )

        self.logger.info(
            f"metastore_dir        = "
            f"{self.config['local']['metastore_dir']}"
        )

        self.logger.info(
            f"bronze_path          = "
            f"{self.config['local']['bronze_path']}"
        )

        self.logger.info("-" * 120)

        self.logger.info(
            f"catalog              = "
            f"{self.spark.conf.get('spark.sql.catalog.spark_catalog')}"
        )

        self.logger.info(
            f"extensions           = "
            f"{self.spark.conf.get('spark.sql.extensions')}"
        )

        self.logger.info(
            f"current_database     = "
            f"{self.spark.catalog.currentDatabase()}"
        )

        self.logger.info("-" * 120)

        self.logger.info(
            f"driver_memory        = "
            f"{self.spark.conf.get('spark.driver.memory')}"
        )

        self.logger.info(
            f"executor_memory      = "
            f"{self.spark.conf.get('spark.executor.memory')}"
        )

        self.logger.info(
            f"master               = "
            f"{self.spark.sparkContext.master}"
        )

        self.logger.info(
            f"application_id       = "
            f"{self.spark.sparkContext.applicationId}"
        )

        self.logger.info(
            f"default_parallelism  = "
            f"{self.spark.sparkContext.defaultParallelism}"
        )

        self.logger.info("-" * 120)

        self.logger.info(
            f"JAVA_HOME            = "
            f"{os.environ.get('JAVA_HOME')}"
        )

        self.logger.info(
            f"SPARK_HOME           = "
            f"{os.environ.get('SPARK_HOME')}"
        )

        self.logger.info(
            f"PYSPARK_PYTHON       = "
            f"{os.environ.get('PYSPARK_PYTHON')}"
        )

        self.logger.info("=" * 120)