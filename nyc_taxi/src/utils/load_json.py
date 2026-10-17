# -*- coding: utf-8 -*-
"""
 Fonction load_json
"""

import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nyc_taxi.src.logger.logger import PipelineLogger


def load_json(path: str | Path, logger: 'PipelineLogger' = None) -> dict:
    """Chargement d'un fichier JSON

    :param path: chemin d'un fichier JSON
    :param logger: gestion des logs
    :return: dictionnaire du contenu du fichier JSON chargée
    """
    path = Path(path)

    if not path.exists():
        return {}

    if path.stat().st_size == 0:
        return {}

    try:
        if not path.exists():
            raise FileNotFoundError(path)

        if path.is_dir():
            raise IsADirectoryError(
                f"{path} est un répertoire et non un fichier JSON"
        )

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        if logger:
            logger.exception(e)
        raise
