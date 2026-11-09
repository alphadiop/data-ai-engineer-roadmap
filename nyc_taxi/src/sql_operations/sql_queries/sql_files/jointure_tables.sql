
SELECT
    {Columns}
    INTO {DstTable}
FROM
    {Table1} AS table1 WITH (NOLOCK)
    {Join} {Table2} AS table2 WITH (NOLOCK)
    {JoinColumns}
    {Where} ;