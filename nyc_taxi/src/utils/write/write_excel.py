# -*- coding: utf-8 -*-
"""
 Fonctions de sauvegarde de DataFrame au format Excel
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logger import LOGGER
    from pandas import DataFrame


def write_excel(df: 'DataFrame', path: str, sheet_name: str = 'Sheet1', index: bool = False,
                logger: 'LOGGER' = None) -> None:
    """Sauvegarde du dataframe df au format csv

    Parameters
    ----------
    :param df : DataFrame à sauvegarder - type possible: pandas.Dataframe, dask.dataframe
    :param path : Chemin où est sauvegardé le DataFrame
    :param sheet_name: nom de la feuille dans laquelle le dataframe est sauvegardé
    :param logger: gestionnaire des logs
    :return: None
    """
    try:
        df.to_excel(path, sheet_name=sheet_name, index=index)
    except Exception as e:
        logger.exception(e)
