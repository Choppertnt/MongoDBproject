from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col

spark = SparkSession.builder \
    .appName("MongoDBIntegration") \
    .master("local")\
    .config("spark.jars", 
            r"C:\Users\chopp\mongo-spark-connector_2.12-10.4.0-all.jar,"
            r"C:\Users\chopp\mongodb-driver-core-5.2.0-javadoc.jar,"
            r"C:\Users\chopp\bson-5.2.0-javadoc.jar," 
            r"C:\Users\chopp\postgresql-42.2.20.jar") \
    .config("spark.mongodb.read.connection.uri", "mongodb://localhost:27017/mydb") \
    .config("spark.mongodb.write.connection.uri", "mongodb://localhost:27017/mydb") \
    .getOrCreate()

spark.stop()



spark = SparkSession.builder \
    .appName("MongoDBIntegration") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.0.0,org.postgresql:postgresql:42.3.1") \
    .config("spark.mongodb.read.connection.uri", "mongodb+srv://test:1234@cluster0.tlwua.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") \
    .config("spark.mongodb.write.connection.uri", "mongodb+srv://test:1234@cluster0.tlwua.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") \
    .getOrCreate()



# Load data from MongoDB
df = spark.read \
    .format("mongodb") \
    .option("database", "user_database") \
    .option("collection", "user_data") \
    .load()

# Display loaded data
df.show()

# Transform the DataFrame
df_product = df.withColumn("product", explode(col("product"))) \
    .select("customername", "sale_date", col("product.product").alias("band"), col("product.unit").alias("unit"), col("product.price").alias("price"))
df_product.show(truncate=False)

df_information = df.select("sale_date", "customername", "phone_number")
df_information.show(truncate=False)

def write_to_postgresql(df, table_name):
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/projectmongodb") \
        .option("dbtable", table_name) \
        .option("user", "postgres") \
        .option("password", "1160") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

# Write DataFrames to PostgreSQL
write_to_postgresql(df_product, "product")
write_to_postgresql(df_information, "information")

# Stop the Spark session
spark.stop()
