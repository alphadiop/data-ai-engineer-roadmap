class PipelineContext:

    def __init__(self):
        self.periode = None
        self.table_name = None
        self.taxi_type = None

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

        self.message = ""

        self.row_count = {}
