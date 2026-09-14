from typing import Iterator, List, Tuple
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nyc_taxi.src.common.logger import PipelineLogger


def build_schema(json_schema:dict, format:dict = None, logger:'PipelineLogger'=None) -> List[Tuple[str, str, str]]:
    """
        Builds a schema from a JSON schema.
    """
    try :
        if format is None:
            format = {}

        schema = []

        for column, info in json_schema.items():
            col = column.format(**format)
            sql_type = info['sql_type']
            nullable = info.get("nullable", "")
            schema.append((col, sql_type, nullable))
        return schema
    except Exception as e:
        if logger:
            logger.error(f"Error building schema: {e}")
        raise