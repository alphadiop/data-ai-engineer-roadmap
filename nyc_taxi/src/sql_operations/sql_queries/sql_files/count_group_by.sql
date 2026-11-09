
SELECT
    {Column}, COUNT(*) AS Count
FROM
    {SrcTable} WITH (NOLOCK)
    {Where}
    GROUP BY {Column};