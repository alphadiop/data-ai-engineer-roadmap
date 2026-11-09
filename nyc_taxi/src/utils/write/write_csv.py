# -*- coding: utf-8 -*-
"""
 Fonctions de sauvegarde de DataFrame au format CSV par chunk ou pas
"""

import csv
import gc
import types
from typing import TYPE_CHECKING
from typing import Union

import dask.dataframe as dd
import pandas as pd

if TYPE_CHECKING:
    from logger import LOGGER


def write_csv(df: Union[pd.DataFrame, dd.DataFrame, types.GeneratorType],
              path: str, mode: str = 'w', sep: str = ",", header: bool = True, float_format: str = None,
              encoding: str = 'utf-8-sig', chunksize: int = None, decimal: str = ".", index: bool = False,
              single_file: bool = False, quoting: int = csv.QUOTE_MINIMAL, logger: 'LOGGER' = None) -> None:
    """Sauvegarde du dataframe df au format csv

    Parameters
    ----------
    :param single_file:
    :param df : DataFrame à sauvegarder - type possible: pandas.Dataframe, dask.dataframe
    :param path : Chemin où est sauvegardé le DataFrame
    :param mode: mode écriture Python
    :param sep: Séparateur dans le fichier csv (default ",")
    :param header: Ecrire ou pas un header à la table
    :param float_format: format string pour float
    :param encoding: encodage
    :param chunksize: nombre de lignes à écrire à la fois
    :param decimal: decimal separator
    :param index: write index
    :param quoting: integer quote parameter
    :param logger: variable de la class LOGGER (gestion des logs)
    :return: None
    """
    try:
        if isinstance(df, pd.DataFrame):
            df.to_csv(path, mode=mode, sep=sep, header=header, float_format=float_format, encoding=encoding,
                      chunksize=chunksize, decimal=decimal, index=index, quoting=quoting)
        elif isinstance(df, dd.DataFrame):
            df.to_csv(path, header=header, encoding=encoding, single_file=single_file, index=index)

            # gestion bug dask: non prise en compte de la commande terminator, d'où l'ajout de lignes vides dans le
            # fichier écrit. Code pour supprimer les lignes vides.
            # path_dir, _ = os.path.split(path)
            # for file in list(filter(lambda file: file.endswith('.csv'), os.listdir(path_dir))):
            #     with open(os.path.join(path_dir, file), 'r') as f:
            #         data = f.read()
            #         cleaned = data.replace('\n\n', '\n')
            #         f.close()
            #
            #     with open(os.path.join(path_dir, file), 'w') as f:
            #         f.write(cleaned)
            #         f.close()
        elif isinstance(df, types.GeneratorType) or isinstance(df, pd.io.parsers.TextFileReader):
            mode_write, header_write = mode, header
            for chunk in df:
                chunk.to_csv(path, mode=mode_write, sep=sep, header=header_write, float_format=float_format,
                             encoding=encoding, index=index)
                mode_write, header_write = 'a', False
            del chunk
            gc.collect()
    except Exception as e:
        logger.exception(e)
