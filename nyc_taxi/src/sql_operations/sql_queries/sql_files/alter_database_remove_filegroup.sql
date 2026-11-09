
IF EXISTS (SELECT * FROM sys.filegroups WHERE name = N'{FileGroup}')
BEGIN
  ALTER DATABASE {BaseName} REMOVE FILEGROUP {FileGroup} ;
END