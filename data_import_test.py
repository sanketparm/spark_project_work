from os.path import abspath

from pyspark.sql import SparkSession


# Create spark session with hive enabled
spark = SparkSession.builder \
    .appName("HealthInsurance") \
    .enableHiveSupport() \
    .getOrCreate()


postgres_url = "jdbc:postgresql://ec2-3-9-191-104.eu-west-2.compute.amazonaws.com:5432/testdb"
postgres_properties = {
    "user": "consultants",
    "password": "WelcomeItc@2022",
    "driver": "org.postgresql.Driver",
}
postgres_table_name = "health_insurance"

# Read data from PostgreSQL
df_postgres = spark.read.jdbc(url=postgres_url, table=postgres_table_name, properties=postgres_properties)
df_postgres.show()


# full load data to hive

# Create database
spark.sql("CREATE DATABASE IF NOT EXISTS sanket_db")

# Hive database and table names
hive_database_name = "sanket_db"
hive_table_name = "health_insurance"

# Create Hive Internal table
df_postgres.write.mode('overwrite') \
    .saveAsTable("sanket_db.health_insurance")

# Read Hive table
df = spark.read.table("sanket_db.health_insurance")
df.show()
