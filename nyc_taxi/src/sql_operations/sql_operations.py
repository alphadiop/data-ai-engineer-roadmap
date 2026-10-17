# -*- coding: utf-8 -*-
"""
 Class de support - Manage les opérations SQL via la lib sqlalchemy
"""
import ast
import csv
import datetime
import glob
import os
import shutil
from typing import TYPE_CHECKING
from typing import Tuple, Dict
from typing import Union, Iterator
import types
from typing import Union, List
from pathlib import Path
import dask.dataframe as dd
import pandas as pd
from sqlalchemy import text
from nyc_taxi.src.utils.load_json import load_json
from nyc_taxi.src.utils.sql_query.read_queries import read_queries
from nyc_taxi.src.utils.sql_query.read_query import read_query


# from copy_file import copy_file

# from make_dirs import make_dirs
# from rmtree import rmtree
# from sqlalchemy import text
# from sql_manager import SQLManager
#
#

# from sql_schema import get_columns_from_schema
# from write import write_csv
# from write_xml import write_xml

from nyc_taxi.src.sql_manager.sql_manager import SQLManager

if TYPE_CHECKING:
    from nyc_taxi.src.logger.logger import PipelineLogger
    from pandas import DataFrame as df_pandas
    from dask.dataframe import DataFrame as df_dask


class SQLOperations(SQLManager):

    def __init__(
            self,
            env: str,
            server_name: str,
            odbc_driver: str,
            connect_args: dict = None,
            options: dict = None,
            logger=None,
    ):
        self.options = options or {}
        SQLManager.__init__(
            self,
            env=env,
            server_name=server_name,
            odbc_driver=odbc_driver,
            connect_args=connect_args,
            logger=logger,
        )

        self.path_script = Path(__file__).parent
        self.path_sql = self.path_script / "sql_queries"
        self.path_file = self.path_script
        self.json_data = self.get_json_data()



    def get_json_data(self):
        path_json = os.path.join(
            self.path_script, r"sql_queries\sql_operations.json"
        )
        return load_json(path_json, logger=self.logger)

    def get_path_sql(self):
        return self.path_sql


    def read_query(self, query: str, format: dict):
        return read_query(
            self.path_sql,
            self.json_data,
            query,
            format=format,
            logger=self.logger
        )

    def read_queries(self, query: str, format: dict):
        return read_queries(
            self.path_sql,
            self.json_data,
            query,
            format=format,
            logger=self.logger
        )


    #
    # def execute_query(self, query: str, path_error: str = None):
    #     if not query:
    #         raise ValueError("Query is empty or None")
    #     try:
    #         with self.engine.begin() as conn:
    #             conn.execute(text(query))
    #         if self.logger:
    #             self.logger.write_sql_query(query)
    #
    #     except Exception as e:
    #         if self.logger:
    #             self.logger.sql_logger.write("\n\n-- Requête exécutée à la levée d'exception:\n")
    #             self.logger.write_sql_query(query)
    #
    #         if path_error:
    #             for src_path in glob.glob(os.path.join(path_error, "*")):
    #                 dst_path = os.path.join(
    #                     os.path.dirname(self.logger.path_log),
    #                     os.path.basename(src_path)
    #                 )
    #                 encodings = None
    #                 if self.options:
    #                     encodings = self.options.get("encodings")
    #
    #                 copy_file(
    #                     src_path,
    #                     dst_path,
    #                     encodings=encodings,
    #                     logger=self.logger)
    #
    #             rmtree(path_error)
    #         if self.logger:
    #             self.logger.exception(e)
    #         raise
    #
    #
    # def execute_query_name(self,query_name: str,format: dict = None,path_error: str = None):
    #     query = self.read_query(query_name,format=format or {})
    #     self.execute_query(query,path_error=path_error)
    #
    #
    #
    # def execute_queries(self, queries: List[str]):
    #     for query in queries:
    #         self.execute_query(query)
    #
    # def execute_query_openquery(self, query: str, dst_table: str, serveur: str):
    #     server = self.config.get_db('dw_prod').get("server")
    #     query = self.read_query(query='execute_openquery', format=dict(DstTable=dst_table, Query=query, Server=server))
    #     self.execute_query(query)
    #
    #
    #
    # def load_df(
    #         self,
    #         query: str,
    #         coerce_float: bool = False,
    #         chunk_size: int = None,
    #         index_col: Union[str, List[str]] = None
    # ) -> Union[pd.DataFrame, types.GeneratorType]:
    #     try:
    #         with self.engine.connect() as conn:
    #             df = pd.read_sql(
    #                 text(query),
    #                 conn,
    #                 index_col=index_col,
    #                 coerce_float=coerce_float,
    #                 chunksize=chunk_size
    #             )
    #         if self.logger is not None:
    #             self.logger.write_sql_query(query)
    #         return df
    #     except Exception as e:
    #         if self.logger is not None:
    #             self.logger.exception(e)
    #         raise
    #
    #
    # def create_table(self, table_name: str, schema: List[Tuple[str, str, str]], drop_table: bool = True) -> None:
    #     """Creation d'une table SQL
    #
    #     :param table_name: nom de la table à créer
    #     :param schema: schema de la table à créer
    #     :param drop_table
    #     :return: None
    #     """
    #     if drop_table:
    #         self.drop_table(table_name)
    #     str_schema = ",  ".join(list(map(lambda tp: " ".join(tp), schema)))
    #     query = self.read_query(query="create_table", format=dict(TableName=table_name, Schema=str_schema))
    #     self.execute_query(query)
    #
    #
    #
    # def drop_table(self, table_name: str) -> None:
    #     try:
    #         if not table_name:
    #             raise ValueError("table_name invalide")
    #
    #         query = f"""
    #         IF OBJECT_ID('{table_name}', 'U') IS NOT NULL
    #             DROP TABLE {table_name};
    #         """
    #
    #         self.execute_query(query)
    #
    #         if self.logger:
    #             self.logger.info(f"DROP TABLE OK: {table_name}")
    #
    #     except Exception as e:
    #         if self.logger:
    #             self.logger.exception(e)
    #         raise
    #
    #
    # def create_table_if_not_exist(self,table_name: str, schema: list[tuple[str, str, str]]) -> None:
    #     """
    #     Create table only if it does not exist (SQL Server safe version)
    #     """
    #     try:
    #         if not table_name:
    #             raise ValueError("table_name vide")
    #
    #         # ----------------------------
    #         # temp table detection robuste
    #         # ----------------------------
    #         is_temp = table_name.startswith("#")
    #
    #         if is_temp:
    #             full_table = f"tempdb..{table_name}"
    #             condition = f"""
    #             IF OBJECT_ID('tempdb..{table_name}') IS NULL
    #             """
    #         else:
    #             full_table = f"dbo.{table_name}"
    #             condition = f"""
    #             IF OBJECT_ID('dbo.{table_name}', 'U') IS NULL
    #             """
    #
    #         # ----------------------------
    #         # schema build (inchangé chez toi)
    #         # ----------------------------
    #         str_schema = ", ".join(
    #             f"{col} {sql_type} {nullable}"
    #             for col, sql_type, nullable in schema
    #         )
    #
    #         # ----------------------------
    #         # SQL template call
    #         # ----------------------------
    #         query = self.read_query(
    #             query="create_table_if_not_exist",
    #             format={
    #                 "Condition": condition,
    #                 "TableName": full_table,
    #                 "Schema": str_schema
    #             }
    #         )
    #         self.execute_query(query)
    #         if self.logger:
    #             self.logger.info(f"TABLE CREATED IF NOT EXISTS: {full_table}")
    #     except Exception as e:
    #         if self.logger:
    #             self.logger.exception(e)
    #         raise
    #
    #
    #
    #
    # def drop_tables(self, table_names: Union[List[str], Iterator]) -> None:
    #     """Applique de la commande SQL 'DROP TABLE' sur une liste de tables
    #
    #     :param table_names: liste des tables que l'on souhaite effacer
    #     :return: None
    #     """
    #     table_names = list(table_names)
    #
    #     if self.logger:
    #         self.logger.info(
    #             f"Suppression de {len(table_names)} table(s)"
    #         )
    #
    #     if table_names is None:
    #         return
    #     for table_name in table_names:
    #         if not table_name:
    #             continue
    #         try:
    #             self.drop_table(table_name)
    #
    #         except Exception as e:
    #             if self.logger:
    #                 self.logger.exception(
    #                     f"Impossible de supprimer la table : {table_name}"
    #                 )
    #             raise
    #
    #
    #
    # def drop_tables_by_object_id(self, tables: Union[List[str], Iterator]) -> None:
    #     for table in tables:
    #         query = self.read_query(query="drop_table_by_object_id", format=dict(Table=table))
    #         self.execute_query(query)
    #
    # def drop_views_by_object_id(self, views: Union[List[str], Iterator]):
    #     for view in views:
    #         query = self.read_query(query="drop_view_by_object_id", format=dict(View=view))
    #         self.execute_query(query)
    #
    #
    #
    # def update_table(self, table: str, set: List[str], where: List[str] | None = None) -> None:
    #     """Construction de la commane SQL UPDATE pour modifier des valeurs dans une table
    #
    #     :param table: Nom de la table SQL sur laquelle on souhaite faire un update
    #     :param set: liste des update à réaliser
    #     :param where: liste de filtre à appliquer sur la table
    #     :return: None
    #     """
    #     try:
    #         if not table:
    #             raise ValueError("table vide")
    #         if not set:
    #             raise ValueError("set vide")
    #
    #         set_clause = self.build_columns(set)
    #         where_clause = self.build_where(where)
    #
    #         query = self.read_query(
    #             query="update_table",
    #             format={
    #                 "Table": table,
    #                 "Set": set_clause,
    #                 "Where": where_clause
    #             }
    #         )
    #
    #         self.execute_query(query)
    #     except Exception as e:
    #
    #         if self.logger:
    #             self.logger.exception(e)
    #         raise
    #
    #
    # def delete_rows(self, src_table: str, where: Union[List[str], Iterator[str]]) -> None:
    #     """
    #     Suppression de lignes d'une table SQL.
    #
    #     :param src_table: table source
    #     :param where: conditions de filtrage
    #     """
    #     try:
    #         if not src_table:
    #             raise ValueError("src_table vide")
    #         where_clause = self.build_where(where)
    #
    #         # sécurité anti DELETE complet involontaire
    #         if not where_clause.strip():
    #             raise ValueError(
    #                 f"DELETE interdit sans clause WHERE ({src_table})"
    #             )
    #
    #         query = self.read_query(
    #             query="delete_rows",
    #             format={
    #                 "SrcTable": src_table,
    #                 "Where": where_clause
    #             }
    #         )
    #         self.execute_query(query)
    #     except Exception as e:
    #         if self.logger:
    #             self.logger.exception(e)
    #         raise
    #
    #
    #
    #
    #
    # def delete_inner_join(
    #         self,
    #         table_1: str,
    #         table_2: str,
    #         join_columns: Dict[str, List[str]],
    #         operator: str = "="
    # ) -> None:
    #     """
    #     Supprime les lignes de table_1 présentes dans table_2.
    #
    #     Parameters
    #     ----------
    #     table_1 : str
    #         Table cible.
    #     table_2 : str
    #         Table de jointure.
    #     join_columns : dict
    #         Colonnes de jointure.
    #     operator : str
    #         Opérateur de comparaison.
    #     """
    #
    #     join_condition = self.build_join_condition(
    #         "table1",
    #         "table2",
    #         join_columns,
    #         operator=operator
    #     )
    #
    #     query = self.read_query(
    #         query="delete_inner_join",
    #         format={
    #             "Table1": table_1,
    #             "Table2": table_2,
    #             "JoinCondition": join_condition
    #         }
    #     )
    #     self.execute_query(query)
    #
    #
    #
    # def create_clustered_columnstore_index(
    #         self,
    #         table_name: str,
    #         index_name: str,
    #         options: List[str] | None = None,
    #         partition: str | None = None
    # ) -> None:
    #     """
    #     Création d'un Clustered Columnstore Index.
    #
    #     Parameters
    #     ----------
    #     table_name : str
    #         Nom de la table.
    #     index_name : str
    #         Nom de l'index.
    #     options : list[str]
    #         Options SQL Server.
    #     partition : str
    #         Schéma de partition éventuel.
    #     """
    #
    #     if options is None:
    #         options = [
    #             "DROP_EXISTING = OFF",
    #             "COMPRESSION_DELAY = 0"
    #         ]
    #
    #     options_sql = (
    #         f"WITH ({self.build_columns(options)})"
    #         if options
    #         else ""
    #     )
    #
    #     partition_sql = (
    #         f"ON {partition}"
    #         if partition
    #         else ""
    #     )
    #
    #     query = self.read_query(
    #         query="create_clustered_columnstore_index",
    #         format={
    #             "TableName": table_name,
    #             "IndexName": index_name,
    #             "Options": options_sql,
    #             "Partition": partition_sql
    #         }
    #     )
    #
    #     self.execute_query(query)
    #
    #
    #
    # def create_clustered_index(self, table_name: str, index_name: str, columns_order: List[Tuple[str, str]],
    #                            on: str = '[PRIMARY]', options: List[str] = None):
    #     columns = self.build_columns(map(lambda item: " ".join(item), columns_order))
    #
    #     if options is not None:
    #         options = 'WITH (' + self.build_columns(options) + ')'
    #     else:
    #         options = ''
    #
    #     query = self.read_query("create_clustered_index", format=dict(TableName=table_name, IndexName=index_name,
    #                                                                   Columns=columns, On=on, Options=options))
    #     self.execute_query(query)
    #
    # def create_index(self, index_name: str, table: str, columns: List[str]):
    #     query = self.read_query("create_index", format=dict(IndexName=index_name, Table=table,
    #                                                         Columns=', '.join(columns)))
    #     self.execute_query(query)
    #
    #
    # def insert_values_bulk(self, table_name: str, path_data: str, field_terminator: str = ',',
    #                        additional_option: List[str] = None) -> None:
    #     #additional_option = '' if additional_option is None else self.build_columns(additional_option)
    #     if additional_option:
    #         additional_option = ",\n" + self.build_columns(additional_option)
    #     else:
    #         additional_option = ""
    #
    #     path_error = os.path.join(os.path.dirname(path_data), 'insert_error.log')
    #     query = self.read_query(query="insert_values_bulk",
    #                             format=dict(TableName=table_name, DataFile=path_data, ErrorFile=path_error,
    #                                         FieldTerminator=field_terminator, AdditionalOption=additional_option))
    #     self.execute_query(query, path_error=path_error)
    #     #rmtree(os.path.dirname(path_error))
    #
    #
    #
    # def insert_values_bulks(self, table_name: str, paths_data: List[str], field_terminator: str = ',',
    #                         additional_options: List[str] = None) -> None:
    #     additional_options = '' if additional_options is None else self.build_columns(additional_options)
    #
    #     path_error = os.path.join(os.path.dirname(paths_data[0]), 'insert')
    #     for path_data in paths_data:
    #         query = self.read_query(query="insert_values_bulk",
    #                                 format=dict(TableName=table_name, DataFile=path_data, ErrorFile=path_error,
    #                                             FieldTerminator=field_terminator, AdditionalOption=additional_options))
    #         self.execute_query(query, path_error=path_error)
    #     rmtree(os.path.dirname(path_error))
    #
    #
    # def insert_values0(self, data: Dict[str, str], table_name: str, schema: List[Tuple[str, str, str]]) -> None:
    #     columns = get_columns_from_schema(schema)
    #     values = "'" + "', '".join([data.get(column, '') for column in columns]) + "'"
    #     values = values.replace("'NULL'", "NULL")
    #
    #     query = self.read_query(query="insert_values", format=dict(TableName=table_name, Columns=", ".join(columns),Values=values))
    #     self.execute_query(query)
    #
    #
    #
    # def insert_values(
    #         self,
    #         data: dict,
    #         table_name: str,
    #         schema: list[tuple[str, str, str]]
    # ) -> None:
    #     columns = get_columns_from_schema(schema)
    #     sql_values = []
    #     for column in columns:
    #         value = data.get(column)
    #
    #         if value is None:
    #             sql_values.append("NULL")
    #
    #         elif isinstance(value, (int, float)):
    #             sql_values.append(str(value))
    #         else:
    #             value = str(value).replace("'", "''")
    #             sql_values.append(f"'{value}'")
    #
    #     query = self.read_query(
    #         query="insert_values",
    #         format={
    #             "TableName": table_name,
    #             "Columns": ", ".join(columns),
    #             "Values": ", ".join(sql_values)
    #         }
    #     )
    #     self.execute_query(query)
    #
    #
    #
    #
    # def insert_into_select(self, src_table: str, dst_table: str, columns: List[str],
    #                        schema: List[Tuple[str, str, str]] = None,
    #                        condition_src_table: str = None):
    #     columns = ", ".join(columns)
    #     if condition_src_table is not None:
    #         condition_src_table = " WHERE " + condition_src_table
    #     else:
    #         condition_src_table = " "
    #
    #     schema_columns = columns
    #     if schema is not None:
    #         schema_columns = ', '.join(get_columns_from_schema(schema, self.logger))
    #
    #     query = self.read_query("insert_into_select",
    #                             format=dict(DstTable=dst_table, Columns=columns, SrcTable=src_table,
    #                                         SchemaColumns=schema_columns, ConditionSrcTable=condition_src_table))
    #     self.execute_query(query)
    #
    # def create_synonym(self, synonym_name: str, base_object_name: str):
    #     query = self.read_query("drop_synonym", format=dict(SynonymName=synonym_name))
    #     self.execute_query(query)
    #
    #     query = self.read_query("create_synonym",
    #                             format=dict(SynonymName=synonym_name, BaseObjectName=base_object_name))
    #     self.execute_query(query)
    #
    # def select_table(self, src_table: str, columns: List[str], where: List[str] = None, distinct: bool = False,
    #                  coerce_float: bool = False, chunk_size: int = None, index_col: Union[str, List[str]] = None,
    #                  order_by: List[str] = None) -> \
    #         Union[pd.DataFrame, types.GeneratorType]:
    #     try:
    #         if len(columns) == 0:
    #             columns = ['*']
    #
    #         prefix = 'a.' if distinct else ''
    #         columns = ', '.join(map(lambda x: prefix + x, columns))
    #
    #         if distinct:
    #             columns = 'DISTINCT ' + columns
    #
    #         if where is not None:
    #             where = 'WHERE ' + ' AND '.join(where)
    #         else:
    #             where = ''
    #
    #         if order_by is not None:
    #             order_by = 'ORDER BY ' + ', '.join(order_by)
    #         else:
    #             order_by = ''
    #
    #         prefix = 'AS ' + prefix if prefix != '' else ''
    #         query = self.read_query("select_table", format=dict(SrcTable=src_table, Columns=columns, Where=where,
    #                                                             Prefix=prefix.replace('.', ''), OrderBy=order_by))
    #         return self.load_df(query, coerce_float=coerce_float, chunk_size=chunk_size, index_col=index_col)
    #     except Exception as e:
    #         self.logger.exception(e)
    #
    # def select_top(self, src_table: str, nrows: int = 10) -> pd.DataFrame:
    #     columns = "TOP({Nrows}) *".format(Nrows=nrows)
    #     query = self.read_query("select_table", format=dict(SrcTable=src_table, Columns=columns, Where='',
    #                                                         Prefix='', OrderBy=''))
    #     return self.load_df(query)
    #
    # def select_openquery(self, src_table: str, dst_table: str, server: str, columns: List[str],
    #                      where: List[str] = None):
    #     if where is not None:
    #         where = 'WHERE ' + ' AND '.join(where)
    #     else:
    #         where = ''
    #     query = self.read_query("select_openquery",
    #                             format=dict(DstTable=dst_table, Server=server, Columns=', '.join(columns),
    #                                         SrcTable=src_table, Where=where))
    #     self.execute_query(query)
    #
    # def create_insert_table_from_files(self, df: Union[pd.DataFrame, pd.io.parsers.TextFileReader, dd.DataFrame],
    #                                    dw_dict: dict, csv_dict: dict) -> None:
    #     """Créer et insertion par bulk insert des valeurs d'un dataframe pandas
    #
    #     :param df: dataframe pandas des valeurs à insérer
    #     :param dw_dict: dictionaire contenant le nom de la table temporaire sur le serveur SQl,
    #                     le schema de la table à insérer et le chemin sur le serveur SQL sur lequel est écrite df
    #     :param csv_dict: dictionaire contenant  nom du fichier qui sera utlisé et l'encodage
    #     :return: None
    #     """
    #     try:
    #         table_name = '#' + dw_dict['table_dw']
    #         path_table = self.get_directory_table_insert(dw_dict['path_dw'], csv_dict['table_csv'])
    #         self.write_df_table_insert(df, path_table,
    #                                    csv_dict['table_csv'],
    #                                    csv_dict.get('encoding', 'UTF-8'), csv_dict.get('separator', ','),
    #                                    csv_dict.get('decimal', '.'), csv_dict.get('float_format', '%.19f'),
    #                                    csv_dict.get('quoting', csv.QUOTE_MINIMAL))
    #         write_xml(dw_dict['schema'], csv_dict['table_csv'], path_table, separator=csv_dict.get('separator', ','),
    #                   logger=self.logger)
    #         self.create_table(table_name, dw_dict['schema'])
    #         path_xml = os.path.join(path_table, list(filter(lambda file: file.endswith('.xml'),os.listdir(path_table)))[0])
    #         for file in self.get_path_csv_files(path_table):
    #             additional_options = ["CodePage = '{0}'".format(dw_dict['CodePage'])] if 'CodePage' in dw_dict.keys() else None
    #             self.insert_values_openrowset(table_name, dw_dict['schema'], file, path_xml,additional_options=additional_options)
    #     except Exception as e:
    #         self.logger.exception(e)
    #
    # def get_directory_table_insert(self, path_dw: str, table_csv: str) -> str:
    #     """Création répertoire de travail pour un bulk insert sur le DW
    #
    #     :param path_dw: path du DW
    #     :param table_csv: nom de la table à créer
    #     :return: path_table (str)
    #     """
    #     # create \table directory
    #     suffix = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S.%f')
    #     path_table = path_dw + r"\{0}_{1}".format(table_csv, suffix)
    #     try:
    #         if os.path.exists(path_table):
    #             shutil.rmtree(path_table)
    #         make_dirs(path_table, logger=self.logger)
    #         return path_table
    #     except Exception as e:
    #         self.logger.error("Une erreur s'est produite lors de la création du répertoire: {0}".format(path_table))
    #         self.logger.exception(e)
    #
    # def write_df_table_insert(self, df: Union['df_pandas', pd.io.parsers.TextFileReader, 'df_dask'],
    #                           path_table: str, table_csv: str, encoding: str, separator: str, decimal: str,
    #                           float_format: str, quoting: int) -> None:
    #     """ Ecriture du dataframe sur le DW en vue d'un bulk insert au format csv
    #
    #     :param encoding: encodage à utiliser pour l'ecriture sur le csv
    #     :param df: dataframe à insérer
    #     :param path_table: path sur le DW où est écrit le dataframe df
    #     :param table_csv: nom de la table
    #     :param encoding: type d'encodage pour l'écriture du csv
    #     :param separator: séparateur du fichier csv
    #     :param decimal: float decimal separator
    #     :param float_format:
    #     :param quoting: parametre de quotes
    #     :return: None
    #     """
    #     # write df as csv on path_dw
    #     path_data = path_table + "/{0}".format(table_csv)
    #     if isinstance(df, dd.DataFrame):
    #         path_data += '_*'
    #     path_data += '.csv'
    #     write_csv(df, path_data, float_format=float_format, encoding=encoding, sep=separator, decimal=decimal,
    #               quoting=quoting, logger=self.logger)
    #
    # @staticmethod
    # def get_path_csv_files(path_table: str) -> List[str]:
    #     """
    #     :param path_table:
    #     :return:
    #     """
    #     return list(map(lambda file: os.path.join(path_table, file),
    #                     list(filter(lambda file: file.endswith('.csv'), os.listdir(path_table)))))
    #
    # def insert_values_openrowset(self, table_name: str, schema: list, path_data: str, path_xml: str,
    #                              additional_options: List[str] = None) -> None:
    #     columns = ", ".join(get_columns_from_schema(schema, logger=self.logger))
    #
    #     additional_options = '' if additional_options is None else ', ' + self.build_columns(additional_options)
    #
    #     query = self.read_query("insert_values_openrowset",
    #                             format=dict(TableName=table_name, Columns=columns, FileName=path_data,
    #                                         FormatXml=path_xml, AdditionalOptions=additional_options))
    #     self.execute_query(query)
    #
    #
    # def insert_values_openrowset_json(self, table_name: str, schema: List[Tuple[str, str, str]], path_data: str):
    #     columns = ", ".join(get_columns_from_schema(schema, logger=self.logger))
    #     schema = ",  ".join(list(map(lambda tp: " ".join(tp[:2]), schema)))
    #     query = self.read_query("insert_values_openrowset_json",
    #                             format=dict(TableName=table_name, Columns=columns, PathData=path_data, Schema=schema))
    #     self.execute_query(query)
    #
    #
    # def alter_database_set_recovery(self, base: str, option: str) -> None:
    #     query = self.read_query("alter_database_set_recovery", format=dict(Base=base, Option=option.upper()))
    #     self.execute_query(query)
    #
    # def bulk_load(self, src_table: str, dst_table: str, schema: List[Tuple[str, str, str]]) -> None:
    #     # self.alter_database_set_recovery(base, 'BULK_LOGGED')
    #     columns = get_columns_from_schema(schema)
    #     self.insert_into_select(src_table, dst_table, columns=columns)
    #     # self.alter_database_set_recovery(base, 'FULL')
    #
    #
    # def alter_table_add_column(self, table: str, schema_column: Tuple[str, str, str], default_value: str = None,
    #                            constraint_name: str = None) -> None:
    #     format = dict(Table=table, Column=schema_column[0], TypeColumn=schema_column[1], NullOption=schema_column[2])
    #
    #     if default_value is not None:
    #         format.update(dict(Default=" DEFAULT '{0}'".format(default_value)))
    #     else:
    #         format.update(dict(Default=' '))
    #
    #     if constraint_name is not None:
    #         format.update(dict(Constraint=' CONSTRAINT {0}'.format(constraint_name)))
    #     else:
    #         format.update(dict(Constraint=''))
    #
    #     query = self.read_query('alter_table_add_column', format=format)
    #     self.execute_query(query)
    #
    # def alter_table_drop_column(self, table: str, column: str) -> None:
    #     query = self.read_query('alter_table_drop_column', format=dict(Table=table, Column=column))
    #     self.execute_query(query)
    #
    # def alter_table_drop_constraint(self, table: str, constraint: str) -> None:
    #     query = self.read_query('alter_table_drop_constraint', format=dict(Table=table, Constraint=constraint))
    #     self.execute_query(query)
    #
    # def union_all(self, dst_table: str, src_tables: Union[List[str], Iterator],
    #               columns: Union[List[str], Iterator[str]] = None) -> None:
    #     if columns is None:
    #         columns = '*'
    #     else:
    #         columns = self.build_columns(columns)
    #
    #     union_tables = ' UNION ALL '.join(['SELECT {0} FROM {1}'.format(columns, table) for table in src_tables])
    #     query = self.read_query('union_all', format=dict(DstTable=dst_table, UnionTables=union_tables, Columns=columns))
    #     self.execute_query(query)
    #
    # def set_table(self, src_table: str, dst_table: str, columns: List[str], where: Union[List[str], Iterator[str]] = None,
    #               join: str = None) -> None:
    #     """Méthode de set dans une table temporaire sql
    #
    #     :param src_table: table source
    #     :param dst_table: temporary table destination
    #     :param columns: columns to select
    #     :param where: sql where condition
    #     :param join: sql join condition
    #     :return: None
    #     """
    #     if where is not None:
    #         where = 'WHERE ' + ' AND '.join(where)
    #     else:
    #         where = ''
    #
    #     if join is None:
    #         join = ''
    #
    #     query = self.read_query("set_table", format=dict(Columns=', '.join(columns), DstTable=dst_table,
    #                                                      SrcTable=src_table, Where=where, Join=join))
    #     self.execute_query(query)
    #
    # def drop_duplicated_rows(self, src_table: str, dst_table: str, columns: List[str]) -> None:
    #     """Méthode pour supprimer les doublons sur un liste de colonnes donnée
    #
    #     :param src_table: table source
    #     :param dst_table: temporary table destination
    #     :param columns: columns to select
    #     :return: None
    #     """
    #     query = self.read_query("drop_duplicated_rows", format=dict(Columns=', '.join(columns), DstTable=dst_table,
    #                                                      SrcTable=src_table))
    #     self.execute_query(query)
    #
    # def rename_column(self, table_name: str, old_column: str, new_column: str) -> None:
    #     query = self.read_query('rename_column', format=dict(TableName=table_name, OldColumn=old_column,
    #                                                          NewColumn=new_column))
    #     self.execute_query(query)
    #
    # def count_table(self, src_table: str, where: List[str] = None) -> int:
    #     """Calcul du nombre de ligne d'une table SQL
    #
    #     Parameters
    #     ----------
    #     src_table: nom de la table dont on veut obtenir le nombre de lignes
    #     where: liste des filtres permettant de définir la table dont on veut calculer le nombre de lignes
    #
    #     Returns
    #     -------
    #     Nombre de lignes
    #     """
    #     where = self.build_where(where)
    #     query = self.read_query(query='count_table', format=dict(SrcTable=src_table, Where=where))
    #     return int(self.load_df(query)['Count'].values[0])
    #
    # def jointure_tables(self, table_1: str, table_2: str, dst_table: str, columns: Dict[str, List[str]],
    #                     join_columns: Dict[str, List[str]], prefixes: Dict[str, bool], join: str = 'INNER JOIN',
    #                     where: List[str] = None) -> None:
    #     """Méthode pour réaliser une jointure entre deux tables : table_1 et table_2
    #
    #     :param table_1: nom de la table sql
    #     :param table_2: nom de la table sql
    #     :param dst_table: nom de la table temporaire pour stocker le résultat de la jointure
    #     :param columns: nom des colonnes à conserver des tables_1 et table_2
    #     :param join_columns: colonnes sur lesquelles est réalisée la jointure
    #     :param prefixes: utilisation des prefixes pour la définition des colonnes à sélectionner
    #     :param join: type de jointure ('INNER JOIN' par défaut)
    #     :param where: condition where (optionnel)
    #     :return: None
    #     """
    #     prefixe_1 = 'table1' if prefixes[table_1] else ''
    #     prefixe_2 = 'table2' if prefixes[table_2] else ''
    #
    #     columns_1 = self.build_columns(columns[table_1], prefixe_1) if len(columns[table_1]) != 0 else ''
    #     columns_2 = self.build_columns(columns[table_2], prefixe_2) if len(columns[table_2]) != 0 else ''
    #     columns = columns_1
    #     if columns_2 != '':
    #         columns = columns + ', ' + columns_2
    #     if columns == '':
    #         columns = '*'
    #
    #     where = self.build_where(where)
    #     join_columns['table1'] = join_columns.pop(table_1)
    #     join_columns['table2'] = join_columns.pop(table_2)
    #     join_columns = self.build_join_condition('table1', 'table2', join_columns)
    #     query = self.read_query('jointure_tables', format=dict(Columns=columns, Table1=table_1, Table2=table_2,
    #                                                            DstTable=dst_table,
    #                                                            Join=join, JoinColumns=join_columns, Where=where))
    #     self.execute_query(query)
    #
    # def count_distinct_table(self, src_table: str, columns: List[str], where: List[str] = None) -> Dict[str, int]:
    #     """Calcul du nombre de valeurs distinctes sur une liste de colonnes
    #
    #     Parameters
    #     ----------
    #     src_table: Nom de la table SQL
    #     columns: colonnes dont on veut calculer le nombre de valeurs distinctes
    #     where: listes des conditions de filtrage
    #
    #     Returns
    #     -------
    #     Dictionnaire {colonne: nombre de valeur distincte}
    #     """
    #     where = self.build_where(where)
    #     distinct_columns = self.build_columns(map(lambda x: 'COUNT(DISTINCT {0}) AS {0}'.format(x), columns))
    #     query = self.read_query('count_distinct_table',
    #                             format=dict(SrcTable=src_table, DistinctColumns=distinct_columns, Where=where))
    #     count_distinct = self.load_df(query)[columns].to_dict('list')
    #     return {column: count_distinct[column][0] for column in columns}
    #
    # def count_group_by(self, src_table: str, column: str, where: List[str] = None) -> pd.DataFrame:
    #     where = self.build_where(where)
    #     query = self.read_query('count_group_by',
    #                             format=dict(SrcTable=src_table, Column=column, Where=where))
    #     return self.load_df(query)
    #
    # def sum_group_by(self, src_table: str, columns: List[str], variables: List[str],
    #                  dst_table: str = None, rename_variables: Dict[str, str] = None) -> Union['df_pandas', None]:
    #     """Aggregation pour faire une somme
    #
    #     :param src_table: table source
    #     :param columns: list des colonnes sur lesquelles on réalise le group by
    #     :param variables: variable dont on veut faire la somme
    #     :param dst_table: table de destination [Optionnel]
    #     :param rename_variables: dictionnaire pour nommer les résultats de somme
    #     :return: pandas dataframe ou None (execute query)
    #     """
    #     columns = self.build_columns(columns)
    #     if rename_variables is None:
    #         renaming_name = map(lambda variable: "SUM({0}) AS Sum{0}".format(variable), variables)
    #     else:
    #         renaming_name = list()
    #         for column in variables:
    #             renaming_name.append(f"SUM({column}) AS {rename_variables[column]}")
    #     variables = self.build_columns(renaming_name)
    #     dst_table = '' if dst_table is None else 'INTO ' + dst_table
    #     query = self.read_query('sum_group_by', format=dict(SrcTable=src_table, Columns=columns, Variables=variables,
    #                                                         DstTable=dst_table))
    #     if dst_table == '':
    #         return self.load_df(query)
    #     else:
    #         self.execute_query(query)
    #
    # def avg_group_by(self, src_table: str, columns: List[str], mean_column: str, where: List[str] = None) -> 'df_pandas':
    #     columns = self.build_columns(columns)
    #     where = self.build_where(where)
    #     query = self.read_query('avg_group_by',
    #                             format=dict(SrcTable=src_table, Columns=columns, MeanColumn=mean_column, Where=where))
    #     return self.load_df(query)
    #
    # def sum_columns_table(self, src_table: str, columns: List[str], where: List[str] = None,
    #                       sum_big: bool = False) -> Dict[str, float]:
    #     """Calcul de la somme sur une liste de colonnes
    #
    #     Parameters
    #     ----------
    #     src_table: Nom de la table SQL
    #     columns: colonnes dont on veut calculer le nombre de valeurs distinctes
    #     where: listes des conditions de filtrage
    #     sum_big: cast en bigint pour le résultat de la somme
    #     Returns
    #     -------
    #     Dictionnaire {colonne: somme des valeurs de la colonne}
    #     """
    #     where = self.build_where(where)
    #
    #     sum_type = "SUM(CAST({0} AS BIGINT)) AS {0}" if sum_big else 'SUM({0}) AS {0}'
    #
    #     sum_columns = self.build_columns(map(lambda x: sum_type.format(x), columns))
    #
    #     query = self.read_query('columns_sum',
    #                             format=dict(SrcTable=src_table, SumColumns=sum_columns, Where=where))
    #     sum_columns = self.load_df(query)[columns].to_dict('list')
    #     return {column: 'NULL' if sum_columns[column][0] is None else sum_columns[column][0] for column in columns}
    #
    # def min_columns_table(self, src_table: str, columns: List[str], where: List[str] = None) -> Dict[str, float]:
    #     """Calcul du minimum de colonnes
    #
    #     Parameters
    #     ----------
    #     src_table: Nom de la table SQL
    #     columns: colonnes dont on veut calculer le nombre de valeurs distinctes
    #     where: listes des conditions de filtrage
    #     Returns
    #     -------
    #     Dictionnaire {colonne: minimum des valeurs de la colonne}
    #     """
    #     where = self.build_where(where)
    #
    #     min_columns = self.build_columns(map(lambda x: f"MIN({x}) AS {x}", columns))
    #
    #     query = self.read_query('columns_min',
    #                             format=dict(SrcTable=src_table, MinColumns=min_columns, Where=where))
    #     minimum = self.load_df(query)[columns].to_dict('list')
    #     return {column: 'NULL' if minimum[column][0] is None else minimum[column][0] for column in columns}
    #
    # def max_columns_table(self, src_table: str, columns: List[str], where: List[str] = None) -> Dict[str, float]:
    #     """Calcul du minimum de colonnes
    #
    #     Parameters
    #     ----------
    #     src_table: Nom de la table SQL
    #     columns: colonnes dont on veut calculer le nombre de valeurs distinctes
    #     where: listes des conditions de filtrage
    #     Returns
    #     -------
    #     Dictionnaire {colonne: maximum des valeurs de la colonne}
    #     """
    #     where = self.build_where(where)
    #
    #     max_columns = self.build_columns(map(lambda x: f"MAX({x}) AS {x}", columns))
    #
    #     query = self.read_query('columns_max',
    #                             format=dict(SrcTable=src_table, MaxColumns=max_columns, Where=where))
    #     maximum = self.load_df(query)[columns].to_dict('list')
    #     return {column: 'NULL' if maximum[column][0] is None else maximum[column][0] for column in columns}
    #
    # def create_view(self, view_name: str, query: str):
    #     query = self.read_query('create_view', format=dict(ViewName=view_name, Query=query))
    #     self.execute_query(query)
    #
    # def create_partition_function(self, name_function: str, periodes: List[str]) -> None:
    #     periodes = ", ".join(map(lambda x: str(x), periodes))
    #     query = self.read_query('create_partition_function', format=dict(NameFunction=name_function, Values=periodes))
    #     self.execute_query(query)
    #
    # def drop_partition_function(self, name_function: str) -> None:
    #     query = self.read_query('drop_partition_function', format=dict(NameFunction=name_function))
    #     self.execute_query(query)
    #
    # def drop_partition_scheme(self, name_scheme: str) -> None:
    #     query = self.read_query('drop_partition_scheme', format=dict(NameScheme=name_scheme))
    #     self.execute_query(query)
    #
    # def alter_database_add_filegroups(self, base_name: str, file_groups: List[str]):
    #     for file_group in file_groups:
    #         self.alter_database_add_filegroup(base_name, file_group)
    #
    # def alter_database_add_filegroup(self, base_name: str, file_group: str):
    #     self.alter_database_remove_file(base_name, file_group)
    #     self.alter_database_remove_filegroup(base_name, file_group)
    #
    #     query = self.read_query('alter_database_add_filegroup', format=dict(BaseName=base_name, FileGroup=file_group))
    #     self.execute_query(query)
    #
    # def alter_database_remove_filegroup(self, base_name: str, file_group: str):
    #     query = self.read_query('alter_database_remove_filegroup', format=dict(BaseName=base_name,
    #                                                                            FileGroup=file_group))
    #     self.execute_query(query)
    #
    # def alter_database_remove_filegroups(self, base_name: str, file_groups: List[str]):
    #     for file_group in file_groups:
    #         query = self.read_query('alter_database_remove_filegroup', format=dict(BaseName=base_name,
    #                                                                                FileGroup=file_group))
    #         self.execute_query(query)
    #
    # def alter_database_add_files(self, base_name: str, paths_partition: Dict[str, str], file_groups: List[str]):
    #     make_dirs(paths_partition['partage'], exist_ok=True, logger=self.logger)
    #     for file_group in file_groups:
    #         self.alter_database_add_file(base_name, paths_partition['local'], file_group)
    #
    # def alter_database_add_file(self, base_name: str, path_partition: str, file_group: str):
    #     path_file = path_partition + "\\" + file_group + '.ndf'
    #     query = self.read_query('alter_database_add_file', format=dict(BaseName=base_name, File=file_group,
    #                                                                    FileGroup=file_group, PathFile=path_file))
    #     self.execute_query(query)
    #
    # def alter_database_remove_file(self, base_name: str, file: str):
    #     query = self.read_query('alter_database_remove_file', format=dict(BaseName=base_name, File=file))
    #     self.execute_query(query)
    #
    # def alter_database_remove_files(self, base_name: str, files: List[str]):
    #     for file in files:
    #         query = self.read_query('alter_database_remove_file', format=dict(BaseName=base_name, File=file))
    #         self.execute_query(query)
    #
    # def create_partition_scheme(self, name_scheme: str, name_function: str, file_groups: List[str]):
    #     query = self.read_query('create_partition_scheme',
    #                             format=dict(NameScheme=name_scheme, NameFunction=name_function,
    #                                         FileGroups=", ".join(file_groups)))
    #     self.execute_query(query)
    #
    # def drop_index(self, table_name: str, index_name: str):
    #     query = self.read_query('drop_index', format=dict(TableName=table_name, IndexName=index_name))
    #     self.execute_query(query)
    #
    # def alter_partition_scheme(self, scheme_name: str, file_group: str):
    #     query = self.read_query('alter_partition_scheme', format=dict(SchemeName=scheme_name, FileGroup=file_group))
    #     self.execute_query(query)
    #
    # def alter_partition_function(self, function_name: str, range_partition: str):
    #     query = self.read_query(query='alter_partition_function', format=dict(FunctionName=function_name,
    #                                                                     Range=range_partition))
    #     self.execute_query(query)
    #
    # @staticmethod
    # def build_where(where: Union[List[str], Iterator[str]]) -> str:
    #     """Construction d'une condition SQL de type 'WHERE'
    #         Parameters
    #         ----------
    #         where: liste des conditions
    #         Returns
    #         -------
    #         String de la condition 'WHERE'
    #     """
    #     if where is None:
    #         return ''
    #     else:
    #         return 'WHERE ' + ' AND '.join(where)
    #
    # @staticmethod
    # def build_having(having: Union[List[str], Iterator[str]]) -> str:
    #     """Construction d'une condition SQL de type 'WHERE'
    #
    #     Parameters
    #     ----------
    #     where: liste des conditions
    #
    #     Returns
    #     -------
    #     String de la condition 'WHERE'
    #     """
    #     if having is None:
    #         return ''
    #     else:
    #         return 'HAVING ' + ' AND '.join(having)
    #
    #
    # @staticmethod
    # def build_columns(columns: Union[List[str], Iterator[str]], prefixe: str = '') -> str:
    #     """Construction d'une string de colonnes séparée par des virgules
    #
    #     :param columns:
    #     :param prefixe:
    #     :return:
    #     """
    #     if prefixe != '':
    #         prefixe += '.'
    #     return ", ".join(map(lambda column: prefixe + column, columns))
    #
    #
    # @staticmethod
    # def build_join_condition(table_1: str, table_2: str, columns: Dict[str, List[str]], operator: str = '=') -> str:
    #     """Définition des conditions de jointures entre deux tables à partir d'une liste de colonnes
    #
    #     :param table_1: table à joindre ou préfixe sql
    #     :param table_2: table à joindre ou préfixe sql
    #     :param columns: liste des colonnes sur lesquelles portent la jointure
    #     :param operator: opérateur à utiliser pour la définition de jointure
    #     :return: commande SQL de la condition de jointure
    #     """
    #     zip_columns = zip(columns[table_1], columns[table_2])
    #     return 'ON ' + ' AND '.join(map(lambda column: table_1 + '.' + column[0] + ' ' + operator + ' ' + table_2 + '.' + column[1], zip_columns))
    #
    #
    #
    #
    # def get_temporary_table_columns(self, table_name: str) -> List[str]:
    #     query = self.read_query('get_temporary_table_columns', format=dict(TableName=table_name))
    #     return list(self.load_df(query)['name'].values)
    #
    #
    # def define_index_table(self, src_table: str, dst_table: str, columns: List[str], index_name: str):
    #     columns = self.build_columns(columns)
    #     query = self.read_query('define_index_table', format=dict(Columns=columns, IndexName=index_name,
    #                                                               DstTable=dst_table, SrcTable=src_table))
    #     self.execute_query(query)
    #
    # def drop_procedure(self, procedure_name: str) -> None:
    #     query = self.read_query('drop_procedure', format=dict(ProcedureName=procedure_name))
    #     self.execute_query(query)
    #
    # def create_procedure(self, procedure_name: str, parameters: List[Tuple[str, str]], query: str) -> None:
    #     parameters = ", ".join(" ".join(tp) for tp in parameters)
    #     query = self.read_query('create_procedure', format=dict(ProcedureName=procedure_name, Parameters=parameters,
    #                                                             Query=query))
    #     self.execute_query(query)
    #
    # def drop_function(self, function_name: str) -> None:
    #     query = self.read_query('drop_function', format=dict(FunctionName=function_name))
    #     self.execute_query(query)
    #
    #
    # def create_function_table(self, function_name: str, parameters: List[Tuple[str, str]], query: str) -> None:
    #     parameters = ", ".join(" ".join(tp) for tp in parameters)
    #     query = self.read_query(query='create_function_table',
    #                             format=dict(FunctionName=function_name,
    #                                         Parameters=parameters,
    #                                         Query=query)
    #                             )
    #     self.execute_query(query)
    #
    #
    #
    # def insert_dataframe(self, table_sql: str, df, chunksize: int = 5000, logger=None):
    #     if self.is_empty_dataframe(df):
    #         return 0
    #     if logger:
    #         logger.info(f"table_sql : {table_sql}")
    #     database, schema, table = self.parse_table_name(table_sql)
    #     total_rows = len(df)
    #     for start in range(0, total_rows, chunksize):
    #         chunk = df.iloc[start:start + chunksize]
    #         chunk.to_sql(
    #             name=table,
    #             schema=schema,
    #             con=self.engine,
    #             if_exists="append",
    #             index=False,
    #             method=None
    #         )
    #         if logger:
    #             logger.info(f"Inserted {len(chunk):,} rows into {schema}.{table}")
    #     return total_rows
    #
    #
    #
    #
    # @staticmethod
    # def parse_table_name(table_name: str):
    #     table_name = table_name.replace("[", "").replace("]", "")
    #     parts = table_name.split(".")
    #     if len(parts) == 3:
    #         database, schema, table = parts
    #     elif len(parts) == 2:
    #         schema, table = parts
    #         database = None
    #     else:
    #         database = None
    #         schema = "dbo"
    #         table = parts[0]
    #     return database, schema, table
    #
    #
    # @staticmethod
    # def is_empty_dataframe(df) -> bool:
    #     import pandas as pd
    #     import polars as pl
    #     """
    #     Vérifie si un DataFrame Pandas/Polars est vide.
    #     """
    #     if df is None:
    #         return True
    #
    #     if isinstance(df, pl.LazyFrame):
    #         return df.limit(1).collect().is_empty()
    #
    #     if isinstance(df, pl.DataFrame):
    #         return df.is_empty()
    #
    #     if isinstance(df, pd.DataFrame):
    #         return df.empty
    #
    #     raise TypeError(
    #         f"Type non supporté : {type(df)}"
    #     )
    #
    #
    #
    # def count_df(self, df) -> int:
    #     import polars as pl
    #     import pandas as pd
    #     """
    #     Retourne le nombre de lignes d'un DataFrame
    #     (Polars LazyFrame, Polars DataFrame ou Pandas DataFrame).
    #     """
    #
    #     if isinstance(df, pl.LazyFrame):
    #         return (
    #             df.select(pl.len())
    #             .collect()
    #             .item()
    #         )
    #
    #     if isinstance(df, pl.DataFrame):
    #         return df.height
    #
    #     if isinstance(df, pd.DataFrame):
    #         return len(df)
    #
    #     raise TypeError(
    #         f"Type non supporté : {type(df)}"
    #     )
    #
    # def table_exists(self, table_sql: str) -> bool:
    #     database, schema, table = self.parse_table_name(table_sql)
    #     query = f"""
    #     SELECT COUNT(*)
    #     FROM {database}.INFORMATION_SCHEMA.TABLES
    #     WHERE TABLE_SCHEMA = '{schema}'
    #       AND TABLE_NAME = '{table}'
    #     """
    #     return self.execute_query(query)
    #
    # def table_exists2(self, table_name: str) -> bool:
    #
    #     query = f"""
    #     SELECT
    #         CASE
    #             WHEN OBJECT_ID('{table_name}', 'U') IS NOT NULL
    #             THEN 1
    #             ELSE 0
    #         END
    #     """
    #     return bool(self.execute_query(query))

# if __name__=="__main__":
#     import sys
#     from tabulate import tabulate
#     from os import path, getcwd, chdir
#     print('******* succès : SQLOperations(SQLManager):'+50*'*')
#     server = get_variable_environnement(variable_environnement=load_variable_environnement(),variable='dw_gersit')
#     odbc_driver = get_variable_environnement(variable_environnement=load_variable_environnement(), variable='odbc_driver')
#     conn = SQLOperations(server_name='dw_gersit',odbc_driver=odbc_driver)
#     print(conn.get_path_csv_files(path_table=r"D:\data_figees")) # return la liste des fichiers présents dans le repetoire
#     #print(conn.get_path_sql())