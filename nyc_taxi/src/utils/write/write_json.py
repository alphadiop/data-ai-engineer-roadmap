# -*- coding: utf-8 -*-
"""
 Fonctions de sauvegarde de DataFrame au format JSON
"""


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame
    from logger import LOGGER


def write_json(df: 'DataFrame', path: str, orient: str = "records", logger: 'LOGGER' = None) -> None:
    """Ecrite d'un dataframe pandas au format json

    :param df: dataframe à sauvegarder
    :param path: chemin pour la sauvegarde
    :param orient: option du format json
    :param logger: logger
    :return: None
    """
    try:
        df.to_json(path, orient=orient)
    except Exception as e:
        logger.exception(e)
