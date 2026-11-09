
IF EXISTS (SELECT * FROM sys.partition_schemes WHERE name = N'{NameScheme}')
  DROP PARTITION SCHEME {NameScheme} ;