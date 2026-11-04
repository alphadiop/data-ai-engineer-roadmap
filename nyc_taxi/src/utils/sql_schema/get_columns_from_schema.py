
import os
import sys

from typing import List, Tuple
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nyc_taxi.src.logger.logger import PipelineLogger

def get_columns_from_schema(schema: List[Tuple[str, str, str]], logger: 'PipelineLogger' = None) -> List[str]:
    try:
        if logger:
            logger.info(f"Schema: {schema}")
        return [column[0] for column in schema]
    except Exception as e:
        if logger:
            logger.error(f"Error getting columns from schema: {e}")
        raise e