from pyspark.sql.functions import col, regexp_replace

file_path = "/Volumes/workspace/default/health_data_volume/base_cdi.csv"

df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(file_path)

columns_to_drop = [
    "LocationAbbr", "DataSource", "DataValueAlt", "DataValueFootnote", "DataValueFootnoteSymbol", 
    "LowConfidenceLimit", "HighConfidenceLimit", "Geolocation", "LocationID", 
    "StratificationCategory2", "StratificationCategory3", "Stratification2", "Stratification3", 
    "TopicID", "QuestionID", "ResponseID", "DataValueTypeID", "StratificationCategoryID1", 
    "StratificationCategoryID2", "StratificationCategoryID3", "StratificationID1", 
    "StratificationID2", "StratificationID3", "Question", "Response"
]

df_cleaned = df.drop(*columns_to_drop)

df_cleaned = df_cleaned.withColumn("DataValue", regexp_replace(col("DataValue"), ",", "").cast("double"))
    
# Drop rows where critical numeric values are null
df_cleaned = df_cleaned.dropna(subset=["DataValue"])