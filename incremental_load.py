from os.path import abspath
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create spark session with hive enabled
spark = SparkSession.builder.appName("carInsuranceClaimsApp").enableHiveSupport().getOrCreate()
# .config("spark.jars", "/Users/hmakhlouf/Desktop/TechCnsltng_WorkSpace/config/postgresql-42.7.2.jar") \

# 1- Establish the connection to PostgresSQL and hive:

# PostgresSQL connection properties
postgres_url = "jdbc:postgresql://ec2-3-9-191-104.eu-west-2.compute.amazonaws.com:5432/testdb"
postgres_properties = {
    "user": "consultants",
    "password": "WelcomeItc@2022",
    "driver": "org.postgresql.Driver",
}
postgres_table_name = "health_insurance"

# hive database and table names
hive_database_name = "sanket_db"
hive_table_name = "health_insurance"


# 2. read & show new dataset from PostgresSQL:
new_data = spark.read.jdbc(url=postgres_url, table=postgres_table_name, properties=postgres_properties)
new_data.show(3)

# 3. read and show the existing_data in hive table
existing_hive_data = spark.read.table("{}.{}".format(hive_database_name, hive_table_name))    #table("project1db.carinsuranceclaims")
existing_hive_data.show(3)

# 4. Determine the incremental data
incremental_data_df = new_data.join(existing_hive_data.select("BeneID"), new_data["BeneID"] == existing_hive_data["BeneID"], "left_anti")
incremental_data_df.show()

# 5.  Adding the incremental_data DataFrame to the existing hive table
# write & append to the Hive table
incremental_data_df.write.mode("append").insertInto("{}.{}".format(hive_database_name, hive_table_name))


# 6. Show the new  records in hive table
# newDataHive_df = spark.sql("SELECT * FROM project1db.carinsuranceclaims cic WHERE cic.ID = 1 OR cic.ID = 2")
# newDataHive_df.show()


# 7. Stop Spark session
spark.stop()


