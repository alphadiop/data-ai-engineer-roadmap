import os
import sys

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
from nyc_taxi.src.common.logger import PipelineLogger

if TYPE_CHECKING:
    from nyc_taxi.src.common.logger import PipelineLogger

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
    path = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/nyc_taxi/src/schema/yellow/audit_load.json"
    load_json = load_json(path)
    schema = build_schema(load_json)
    print(schema)
    colums = get_columns_from_schema(schema)
    print(colums)
