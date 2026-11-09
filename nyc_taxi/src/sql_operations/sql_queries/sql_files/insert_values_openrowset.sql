
INSERT INTO {TableName} WITH (TABLOCK) ({Columns})
                                        SELECT {Columns}
                                        FROM OPENROWSET(BULK '{FileName}',
                                                        FORMATFILE = '{FormatXml}',
                                                        FirstRow = 2
                                                        {AdditionalOptions}) AS t;