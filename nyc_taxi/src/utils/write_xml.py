# -*- coding: utf-8 -*-
"""
 Création d'un fichier XML
"""

import os
from typing import List, Tuple
from typing import TYPE_CHECKING

from get_xml import get_xml
from write import write_text

if TYPE_CHECKING:
    from logger import LOGGER


def write_xml(schema: List[Tuple[str, str, str]], table: str, path: str, separator: str = ',',
              logger: 'LOGGER' = None) -> None:
    """Création de fichier XML

    :param schema: le schema contenant les colonnes d'un dataframe
    :param table: nom de la table
    :param path: chemin où est restitué le fichier xml
    :param  separator: type de delimiter du fichier csv
    :param logger: gestion des logs
    :return None
    """
    try:
        write_text(get_xml([tup[0] for tup in schema], separator=separator, logger=logger),
                   os.path.join(path, '{0}.xml'.format(table)))
    except Exception as e:
        logger.exception(e)
