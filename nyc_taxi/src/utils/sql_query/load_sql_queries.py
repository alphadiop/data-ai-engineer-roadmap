# -*- coding: utf-8 -*-
"""
 Load du fichier json de requêtes
"""

import os
from typing import Dict, Tuple
from typing import TYPE_CHECKING

from nyc_taxi.src.utils.load_json import load_json

if TYPE_CHECKING:
    from nyc_taxi.src.logger.logger import PipelineLogger


def load_sql_queries(path_lib: str, name_lib: str, logger: 'PipelineLogger' = None) -> Tuple[str, Dict[str, str]]:
    path_sql = os.path.join(path_lib, 'sql_queries')
    return path_sql, load_json(os.path.join(path_sql,  name_lib + '.json'), logger=logger)
