# -*- coding: utf-8 -*-
"""
 Fonctions de copie de fichiers
"""

import shutil
from typing import TYPE_CHECKING

from open_file import open_file

if TYPE_CHECKING:
    from logger import LOGGER


def copy_file(src_path: str, dst_path: str, length: int = 10000000, encodings: dict = None,
              logger: 'LOGGER' = None) -> None:
    """Copie de fichier de src_path vers dest_path

    Parameters
    ----------
    :param src_path : path du fichier source
    :param dst_path : path du fichier de destination
    :param length: taille du buffer
    :param encodings: type d'encodage de la source et destination
    :param logger: variable de la class LOGGER (gestion des logs)
    :return None
    """
    if encodings is None:
        encodings = {'src': 'utf-8', 'dst': 'utf-8'}
    src = open_file(src_path, mode='r', encoding=encodings.get('src'), logger=logger)
    dst = open_file(dst_path, mode='w', encoding=encodings.get('dst'), logger=logger)

    try:
        shutil.copyfileobj(src, dst, length=length)
        src.close()
        dst.close()
    except Exception as e:
        logger.exception(e)
