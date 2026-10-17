# -*- coding: utf-8 -*-
"""
 Fonction read_query: lecture d'une requête SQL d'uns fichier
"""
from pathlib import Path
from typing import TYPE_CHECKING

from nyc_taxi.src.utils.get_path_from_json import get_path_from_json
from nyc_taxi.src.utils.open_file import open_file

if TYPE_CHECKING:
    from nyc_taxi.src.logger.logger import PipelineLogger


def read_query(path: Path, json_data: dict, key: str, format: dict = None, logger: 'PipelineLogger' = None) -> str:
    """ Lecture à partir d'un fichier d'une requête SQL

    :param path: chemin racine où se trouve les fichiers de requêtes SQL
    :param json_data: nom du fichier contenant la requête SQL
    :param key: clé correspondant à la requête que l'on souhaite récupérer
    :param format: dictionnaire des variables pour affectation dynamique dans la requête SQL
    :param logger: getionnaire des logs
    :return: requête SQl au format string
    """
    if format is None:
        format = {}

    try:
        sql_path = get_path_from_json(path,json_data,key,logger)
        with open_file(sql_path, logger=logger) as file:
            query = file.read()
        return query.format(**format)
    except Exception as e:
        if logger:
            logger.exception(e)
        raise
