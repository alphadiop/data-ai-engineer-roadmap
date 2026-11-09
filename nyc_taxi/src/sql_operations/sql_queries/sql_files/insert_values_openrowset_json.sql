
BEGIN
DECLARE @JSON VARCHAR(MAX) ;

SELECT @JSON = BulkColumn
FROM OPENROWSET
(BULK '{PathData}', SINGLE_CLOB)
AS j ;

INSERT INTO {TableName}  ({Columns})
                                        SELECT {Columns}
                                        FROM OPENJSON (@JSON)
                                        WITH ({Schema});

END