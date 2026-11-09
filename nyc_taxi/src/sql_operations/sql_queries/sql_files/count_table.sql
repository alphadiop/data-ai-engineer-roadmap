
SELECT
    COUNT(*) AS Count
FROM
    {SrcTable} WITH (NOLOCK)
    {Where};