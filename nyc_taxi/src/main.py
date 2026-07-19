from datetime import datetime
from extract import Extract
from transformations import Transformation
from audit_manager import AuditManager
from load import Load

class TaskTaxi:
    def __init__(self, spark, parameters):
        self.spark = spark
        self.parameters = parameters
        self.logger = self.get_logger()


    def get_logger(self):
        return self.spark._jvm.org.apache.log4j.LogManager.getLogger("UberBronze")

    def run(self):
        #taxi_type = "yellow"
        #taxi_type = "green"
        #taxi_type = "fhv"
        extractor = Extract(
            spark=spark,
            **self.parameters
        )

        audit_manager = AuditManager(
            spark=spark
        )

        load = Load()

        if not audit_manager.is_period_loaded(
            table_name="silver_nyc_taxi",
            taxi_type=self.parameters.get('taxi_type'),
            periode=self.parameters.get('periode')
        ):
            start_time = datetime.now()
            try:
                print("Period not loaded")
                start_time = datetime.now()
                df = extractor.extract()
                transformer = Transformation(spark=spark)
                df_silver = transformer.get_silver_transformation(df)
                df_dimdate = transformer.get_dimdate(df_silver)
                df_fact_trips = transformer.get_fact_trips(df_silver)
                df_kpi_daily = transformer.get_kpi_daily(df_silver)
                df_location = transformer.get_dim_location()
                
                load.sauvegarde_tables_df(
                    df_silver,
                    "silver",
                    "silver_nyc_taxi"
                )
    

                load.sauvegarde_tables_df(
                    df_fact_trips,
                    "gold",
                    "gold_fact_trips"
                )

                load.sauvegarde_tables_df(
                    df_kpi_daily,
                    "gold",
                    "gold_kpi_daily"
                )
                    
                load.sauvegarde_tables_df(
                    df_dimdate,
                    "gold",
                    "gold_dim_date"
                )

                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                audit_manager.insert_audit(
                    periode=self.parameters["periode"],
                    table_name="silver_nyc_taxi",
                    taxi_type = self.parameters.get("taxi_type"),
                    nb_rows=df_silver.count(),
                    status='SUCCESS',
                    start_time=start_time,
                    end_time=end_time,
                    duration_seconds=duration,
                    message=""
                )

            except Exception as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                audit_manager.insert_audit(
                    periode=self.parameters["periode"],
                    table_name="silver_nyc_taxi",
                    taxi_type=self.parameters["taxi_type"],
                    nb_rows=0,
                    status="ERROR",
                    start_time=start_time,
                    end_time=end_time,
                    duration_seconds=duration,
                    message=str(e)
                )

                raise



    #display(df_silver.limit(5))
    #display(df_dimdate.limit(5))
    #display(df_fact_trips.limit(5))
    #display(df_kpi_daily.limit(5))
    #display(df_location.limit(5))

    

#transformer.sauvegarde_tables_df(df_location, "ref","gold_dim_location")
        
if __name__ == "__main__":
    parameters = {
            "periode": 202408,
            "path_volume": "/Volumes/nyc_taxi/bronze/raw_files",
            "taxi_type": "yellow"
        }
    taxi = TaskTaxi(spark, parameters)
    taxi.run()

