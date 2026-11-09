# -*- coding: utf-8 -*-
"""
 Ecriture d'un fichier text
"""

from typing import TYPE_CHECKING

from open_file import open_file

if TYPE_CHECKING:
    from logger import LOGGER


def write_text(text: str, path: str, logger: 'LOGGER' = None) -> None:
    """Création de fichier XML

    :param text: script
    :param path: chemin où est créé le fichier xml
    :param logger: gestionnaire des logs
    :return None
    """
    try:
        with open_file(path, "w") as f:
            f.writelines(text)
            f.close()
    except Exception as e:
        logger.exception(e)
