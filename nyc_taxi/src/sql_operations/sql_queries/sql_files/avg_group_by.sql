
SELECT
    {Columns}, AVG({MeanColumn}) AS Moyenne
FROM
    {SrcTable} WITH (NOLOCK)
    {Where}
    GROUP BY {Columns};