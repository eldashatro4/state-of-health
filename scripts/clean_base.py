from pyspark.sql.functions import col, regexp_replace
from pyspark.sql import functions as F

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

# Save only data from 2016-2020
df_filtered = df_cleaned.filter(
    (F.col("YearStart") >= 2016) & (F.col("YearEnd") <= 2020)
)

df2 = df_filtered.withColumn(
    "col_name",
    F.concat_ws("_", "Topic", "StratificationCategory1", "Stratification1", "DataValueUnit")
)

df2 = df2.withColumn("col_name", F.regexp_replace("col_name", r"[^A-Za-z0-9_]", "_"))

df_pivot = (
    df2
    .groupBy("YearStart", "YearEnd", "LocationDesc")
    .pivot("col_name")
    .agg(F.first("DataValue"))
)

df_pivot = df_pivot.filter(~F.col("LocationDesc").isin(["Puerto Rico", "Virgin Islands", "District of Columbia", "Guam", "United States"]))