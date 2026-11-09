
SELECT *
  INTO {DstTable}
  FROM OPENQUERY({Server}, 'SELECT {Columns} FROM {SrcTable} WITH (NOLOCK) {Where};')