# -*- coding: utf-8 -*-
"""
 Fonction open_file
"""
from pathlib import Path
from typing import TextIO
from nyc_taxi.src.logger.logger import PipelineLogger


def open_file(
        path: str | Path,
        mode: str = "r",
        encoding : str ='utf-8',
        logger: PipelineLogger = None
) -> TextIO:
    try:
        return open(path, mode=mode, encoding=encoding)
    except Exception as e:
        if logger:
            logger.exception(e)
        raise
