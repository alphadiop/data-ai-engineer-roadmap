
import os
import sys

PROJECT_ROOT = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/src/nyc"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from typing import List, Tuple
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logger.logger import PipelineLogger

def get_columns_from_schema(schema: List[Tuple[str, str, str]], logger: 'PipelineLogger' = None) -> List[str]:
    try:
        if logger:
            logger.info(f"Schema: {schema}")
        return [column[0] for column in schema]
    except Exception as e:
        if logger:
            logger.error(f"Error getting columns from schema: {e}")
        raise e