
SELECT
    name
FROM
    Tempdb.Sys.Columns
WHERE
    Object_ID = Object_ID('tempdb..{TableName}') ;