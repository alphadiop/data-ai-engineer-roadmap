
SELECT *
  INTO {DstTable}
  FROM OPENQUERY({Server}, '{Query};')