# -*- coding: utf-8 -*-
"""
 Ecriture du corps de fichier xml
"""
from typing import List

from logger import PipelineLogger


def get_xml(columns: List[str], separator: str = ',', logger: PipelineLogger = None) -> str:
    """Script de fichier XML

    :param columns: liste de colonnes de DataFrame
    :param separator: type de delimiter du fichier csv
    :param logger: Logger
    :return: string XML à produire
    """
    try:
        xml = '<?xml version="1.0"?>\n<BCPFORMAT xmlns="http://schemas.microsoft.com/sqlserver/2004/bulkload/format"'
        xml += ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n<RECORD>'
        corps = list(map(lambda column: '\n' + ' ' * 8 + ' <FIELD ID="{0}"'.format(column), columns))

        cmd = ' xsi:type="CharTerm" MAX_LENGTH="250"  TERMINATOR="{0}"/> '.format(separator)
        xml += cmd.join(corps)
        xml += ' xsi:type="CharTerm" MAX_LENGTH="250"  TERMINATOR="\\r\\n"/>'
        xml += '\n' + '</RECORD>\n<ROW>'

        body = list(map(lambda column: '\n' + ' ' * 8 + ' <COLUMN SOURCE="{0}" NAME="{0}"'.format(column), columns))
        xml += ' xsi:type="SQLNVARCHAR"/>'.join(body) + ' xsi:type="SQLNVARCHAR"/>' + '\n' + '</ROW>\n </BCPFORMAT>'
        return xml
    except Exception as e:
        logger.exception(e)
