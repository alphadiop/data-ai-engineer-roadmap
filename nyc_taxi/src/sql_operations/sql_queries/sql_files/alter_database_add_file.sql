
ALTER DATABASE {BaseName}
ADD FILE
(  NAME = N'{File}'
   , FILENAME = N'{PathFile}'
   , SIZE = 10
   , MAXSIZE = UNLIMITED
   , FILEGROWTH = 10)
TO FILEGROUP {FileGroup} ;