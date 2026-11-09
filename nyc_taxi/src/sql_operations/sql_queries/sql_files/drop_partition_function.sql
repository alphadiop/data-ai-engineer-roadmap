
IF EXISTS (SELECT * FROM sys.partition_functions WHERE name = N'{NameFunction}')
  DROP PARTITION FUNCTION {NameFunction} ;