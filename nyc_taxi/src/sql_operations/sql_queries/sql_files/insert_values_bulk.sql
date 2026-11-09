
BULK INSERT {TableName} FROM '{DataFile}' WITH (FIRSTROW = 2,
    FIELDTERMINATOR = '{FieldTerminator}',
    ROWTERMINATOR = '\n',
    ERRORFILE = '{ErrorFile}',
   {AdditionalOption}       );