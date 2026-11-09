
SELECT
    {Columns},
    {Variables}
    {DstTable}
FROM
    {SrcTable} WITH (NOLOCK)
    GROUP BY {Columns};