
SELECT {Columns},
       ROW_NUMBER() OVER(ORDER BY {Columns}) AS {IndexName}
INTO {DstTable}
FROM {SrcTable} ;