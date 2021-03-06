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
df_item_info = df_data.select("id","name","requiredLevel","itemLevel", "itemClass","itemSubClass","bonusStats.stat","bonusStats.amount", "weaponinfo.dps","inventoryType")
#df_auctions = df.select("auc","item","bid","buyout", "ownerRealm", "owner")

df_auctions=df.withColumn("auctions", explode("auctions")).select(
col("_links.*"),col("auctions.*"))
#df2 = df_auctions.withColumn("item",explode("item")).select("*",col("item.*")).show()
#df_auctions.withColumn("col1", split(col("item"), ",").getItem(0)).withColumn("col2", split(col("item"), ",").getItem(1)).show()
df_auctions_v1 = df_auctions.withColumn("realm_id", split(col("self.href"), "\/").getItem(6)).withColumnRenamed("id","auc").select("auc","item.id","item.modifiers.type","item.modifiers.value","bid","buyout","unit_price","quantity","realm_id")
df_auctions_v2=df_auctions_v1.withColumnRenamed("id","item").select("auc","item","type","value","bid","buyout","unit_price","quantity","realm_id")
#Write to postgresql
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
        .option("url","jdbc:postgresql://localhost:5431/wow_db")\
        .option("dbtable","auctions_db")\
        .option("user","user")\
        .option("password","password")\
        .option("driver","org.postgresql.Driver")\
        .save()
                                 
                                                                
