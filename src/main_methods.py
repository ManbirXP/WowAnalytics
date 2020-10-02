from datetime import timedelta
from datetime import datetime as dt
from pyspark import SparkContext
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *



sc = SparkContext()
sqlContext = SQLContext(sc)
spark = SparkSession.builder.appName("data_getter").getOrCreate()

# Field structure on the item info data
#field_data = [StructField("Id", IntegerType(), True), \
 #             StructField("Name", StringType(), True), \
 #             StructField("itemLevel", IntegerType(), True), \
  #            StructField("requiredLevel", IntegerType(), True), \
   #           StructField("itemClass", IntegerType(), True), \
    #          StructField("itemSubClass", IntegerType(), True), \
     #         StructField("bonusStat", ArrayType(IntegerType,True), True),\
      #        StructField("bonusamount", ArrayType(IntegerType,True),True),\
       #       StructField("inventoryType",IntegerType(), True)]

#schema_data= StructType(field_data)

# Methods to retrieve and write data
path_items = f's3a://wowitems/*.json'
path_auctions = f's3a://wowanalyticsdata/*.json'
#df_data = spark.read.option("header", "false").option("inferSchema", "false").schema(schema_data).json(path_items)
df_data = spark.read.json(path_items)
df_auctions = spark.read.json(path_auctions)
df_data = df_data.na.drop()
df_final = df_data.select("id","name",col("itemLevel").as("item_level"),col("requiredLevel").as("requird_level"), col("itemClass").as("item_class"),col("itemSubClass").as("item_subclass"),"bonusStats.stat","bonusStats.amount","inventoryType".as("inventory_type"))\
df_auctions_final = df_auctions.select("item","buyout","bid",col("ownerRealm").as("realm"),"owner")
df_final.write\
        .format("jdbc")\
        .option("url","jdbc:postgresql://local:5431/wow_db")\
        .option("dbtable","items_db")\
        .option("user","user")\
        .option("password","password")\
        .option("driver","org.postgresql.Driver")\
        .save()



df_auctions_final.write\
        .format("jdbc")\
        .option("url","jdbc:postgresql://ec2-3-238-72-162.compute-1.amazonaws.com:5431/wow_db")\
        .option("dbtable","auctions_db")\
        .option("user","manbir")\
        .option("password","m4nb!r1123")\
        .option("driver","org.postgresql.Driver")\
        .save()
                                 
                                                                
