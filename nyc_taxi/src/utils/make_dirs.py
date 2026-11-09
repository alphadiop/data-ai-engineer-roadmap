# -*- coding: utf-8 -*-
"""
 Fonction mkdir: création d'un répertoire
"""

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logger import LOGGER


def make_dirs(directory: str, exist_ok: bool = False, logger: 'LOGGER' = None) -> None:
    """Création d'un répertoire

    :param directory: path du répertoire à créer
    :param exist_ok: paramètre de gestion de l'erreur si le répertoire existe déjà
    :param logger: gestion des logs
    :return: None
    """
    try:
        os.makedirs(directory, exist_ok=exist_ok)
    except Exception as e:
        logger.exception(e)
