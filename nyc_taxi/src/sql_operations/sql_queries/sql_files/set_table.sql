
SELECT {Columns}
    INTO {DstTable}
    FROM {SrcTable} WITH (NOLOCK)
    {Join}
    {Where};