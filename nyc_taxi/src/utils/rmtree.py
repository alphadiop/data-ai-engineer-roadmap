# -*- coding: utf-8 -*-
"""
 Fonction rmtree
"""

import shutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logger import LOGGER


def rmtree(path: str, logger: 'LOGGER' = None) -> None:
    """
    :param path:
    :param logger:
    :return: None
    """
    try:
        shutil.rmtree(path, ignore_errors=True)
    except Exception as e:
        logger.exception(e)
