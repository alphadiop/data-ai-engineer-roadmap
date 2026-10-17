# -*- coding: utf-8 -*-
"""
 get de la class SQL_Alchemy
"""

from typing import TYPE_CHECKING

from nyc_taxi.src.sql_operations.sql_operations import SQLOperations
from nyc_taxi.src.logger.logger import PipelineLogger





def get_sql_operations(
    env: str,
    server_name: str = "dw_prod",
    odbc_driver: str = None,
    connect_args: dict = None,
    options: dict = None,
    logger: 'PipelineLogger' = None
) -> 'SQLOperations':

    if connect_args is None:
        connect_args = {'autocommit': True}

    return SQLOperations(
        env=env,
        server_name=server_name,
        odbc_driver=odbc_driver,
        connect_args=connect_args,
        options=options,
        logger=logger
    )

if __name__ == '__main__':
    odbc_driver = "ODBC Driver 17 for SQL Server"
    env = "local"
    periode = 202411
    taxi_type = "yellow"

    logger = PipelineLogger(
        name="pipeline_runner",
        env=env,
        periode=periode,
        taxi_type=taxi_type
    )
    sql_ops = get_sql_operations(
        env=env,
        server_name="dw_prod",
        odbc_driver=odbc_driver,
        logger=logger,
    )
    rows = sql_ops.fetch_all("SELECT TOP 10 * FROM Sales.SalesOrderHeader")
    logger.info(rows)

