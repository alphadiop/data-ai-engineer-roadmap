# -*- coding: utf-8 -*-
"""
 Fonction get_path_from_json
"""
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nyc_taxi.src.logger.logger import PipelineLogger


def get_path_from_json(
    path: str | Path,
    json_data: dict,
    key: str,
    logger: "PipelineLogger | None" = None,
) -> Path:
    """Résout le chemin d'une requête à partir du registre JSON."""

    if json_data is None:
        raise ValueError("json_data est None")

    if key not in json_data:
        raise KeyError(
            f"Clé '{key}' introuvable dans le fichier JSON.\n"
            f"Clés disponibles : {list(json_data.keys())}"
        )

    try:
        return Path(path) / json_data[key]

    except Exception as e:
        if logger:
            logger.exception(e)
        raise
