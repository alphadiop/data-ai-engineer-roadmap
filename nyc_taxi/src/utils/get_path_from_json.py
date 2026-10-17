# -*- coding: utf-8 -*-
"""
 Fonction get_path_from_json
"""

import os
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from nyc_taxi.src.logger.logger import PipelineLogger


def get_path_from_json(path: Path, json_data: dict, key: str, logger: 'PipelineLogger' = None) -> Path | None:
    """Get du path des requête à partir du join(path + json_data[key])

    :param path: root path
    :param json_data: dictionnary key: path requêtes sql
    :param key: key du json_data dic
    :param logger: geston des logs
    :return: path
    """
    if json_data is None:
        raise ValueError("json_data est None")

    if key not in json_data:
        raise KeyError(
            f"Clé '{key}' introuvable dans le fichier json.\n"
            f"Clés disponibles : {list(json_data.keys())}"
        )
    try:
        return Path(os.path.join(path, json_data[key]))
    except Exception as e:
        if logger:
            logger.exception(e)
        raise
