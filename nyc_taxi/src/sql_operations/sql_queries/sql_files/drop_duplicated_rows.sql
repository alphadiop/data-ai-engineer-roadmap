
SELECT
    *,
    row_number() OVER (PARTITION
BY
    {Columns}
ORDER BY
    {Columns} ) AS row
INTO
    {DstTable}
from
    {SrcTable};


DELETE
FROM {DstTable}
WHERE row > 1;


ALTER TABLE {DstTable}
DROP COLUMN row;
