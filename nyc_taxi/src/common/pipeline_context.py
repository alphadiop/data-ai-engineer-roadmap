class PipelineContext:

    def __init__(self,env:str = "local",taxi_type:str=None):
        self.env = env
        self.taxi_type = taxi_type
        self.periode = None
        self.table_name = None

        self.catalogue= None
        self.schema= None
        
        self.df_bronze = None
        self.df_silver = None

        self.df_fact_trips = None
        self.df_dim_date = None
        self.df_kpi_daily = None
        self.dim_location = None
      
        self.nb_rows = 0
        self.status = None

        self.duration_seconds=0

        self.start_time=None
        self.end_time=None
        self.path_sql_schema = None

        self.message = ""
        self.current_step = ""

        self.row_count = {}
