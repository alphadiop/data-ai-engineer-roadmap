import os
import sys

PROJECT_ROOT = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/src/nyc"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
from common.logger import PipelineLogger

if TYPE_CHECKING:
    from common.logger import PipelineLogger

def load_json(path: Union[str, Path], logger: Optional["PipelineLogger"] = None) -> dict:
    path = Path(path)

    try:
        if not path.exists():
            if logger:
                logger.error(f"File not found: {path}")
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    except Exception as e:
        if logger:
            logger.error(f"Error loading file: {path}")
        raise e


if __name__ == "__main__":

    from sql_schema.build_schema import build_schema
    from sql_schema.get_columns_from_schema import get_columns_from_schema

    logger = PipelineLogger("build_schema")
    path = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/src/nyc/schema/yellow/audit_load.json"
    load_json = load_json(path)
    schema = build_schema(load_json)
    print(schema)
    colums = get_columns_from_schema(schema)
    print(colums)
