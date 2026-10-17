# -*- coding: utf-8 -*-
"""
 Fonction read_queries
"""
from pathlib import Path
from typing import Union
from typing import List
from typing import TYPE_CHECKING

from nyc_taxi.src.utils.get_path_from_json import get_path_from_json
from nyc_taxi.src.utils.open_file import open_file

if TYPE_CHECKING:
    from nyc_taxi.src.logger.logger import PipelineLogger

def read_queries(
        path: str | Path,
        json_data: dict,
        key: str,
        format: dict | None = None,
        logger= None
) -> List[str]:
    """Lecture à partir d'un fichier d'une liste de requête SQL

    :param path: chemin racine où se trouve les fichiers de requêtes SQL
    :param json_data: nom du fichier contenant les requêtes SQL
    :param key: clé correspondant à la requête que l'on souhaitte récupérer
    :param format: dictionnaire des variables pour affectation dynamique dans la requête SQL
    :param logger: getionnaire des logs
    :return: liste de requêtes SQl au format string
    """
    if format is None:
        format = {}

    try:
        query_path = get_path_from_json(
            path,
            json_data,
            key,
            logger
        )
        with open_file(query_path, logger=logger) as file:

            queries = [
                " ".join(query.replace("\n", " ").split())
                for query in file.read().split("\n\n")
                if query.strip()
            ]
        return [
            query.format(**format)
            for query in queries
        ]
    except Exception as e:
        if logger:
            logger.exception(e)
        raise
