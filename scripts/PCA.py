from pyspark.ml.feature import PCA, StandardScaler, VectorAssembler
from pyspark.sql import functions as F
from pyspark.sql.functions import col, regexp_replace, udf
from pyspark.sql.types import DoubleType

file_path = "/Volumes/workspace/default/health_data_volume/chronic_2016_2020.csv"


df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(file_path)
)

columns_to_drop = [
    "LocationAbbr",
    "DataSource",
    "DataValueAlt",
    "DataValueFootnote",
    "DataValueFootnoteSymbol",
    "LowConfidenceLimit",
    "HighConfidenceLimit",
    "Geolocation",
    "LocationID",
    "StratificationCategory2",
    "StratificationCategory3",
    "Stratification2",
    "Stratification3",
    "TopicID",
    "QuestionID",
    "ResponseID",
    "DataValueTypeID",
    "StratificationCategoryID1",
    "StratificationCategoryID2",
    "StratificationCategoryID3",
    "StratificationID1",
    "StratificationID2",
    "StratificationID3",
    "Question",
    "Response",
]

df_cleaned = df.drop(*columns_to_drop)

df_cleaned = df_cleaned.withColumn(
    "DataValue", regexp_replace(col("DataValue"), ",", "").cast("double")
)

# Drop rows where critical numeric values are null
df_cleaned = df_cleaned.dropna(subset=["DataValue"])

# Save only data from 2016-2020
df_filtered = df_cleaned.filter(
    (F.col("YearStart") >= 2016) & (F.col("YearEnd") <= 2020)
)

df2 = df_filtered.withColumn(
    "col_name",
    F.concat_ws(
        "_", "Topic", "StratificationCategory1", "Stratification1", "DataValueUnit"
    ),
)

df2 = df2.withColumn("col_name", F.regexp_replace("col_name", r"[^A-Za-z0-9_]", "_"))

df_pivot = (
    df2.groupBy("YearStart", "YearEnd", "LocationDesc")
    .pivot("col_name")
    .agg(F.first("DataValue"))
)

df_pivot = df_pivot.filter(
    ~F.col("LocationDesc").isin(
        [
            "Puerto Rico",
            "Virgin Islands",
            "District of Columbia",
            "Guam",
            "United States",
        ]
    )
)

# -------------------------------------------------------------
# 2D PCA on Pivoted Indicator Features
# -------------------------------------------------------------


id_cols = {"YearStart", "YearEnd", "LocationDesc"}
feature_cols = [c for c in df_pivot.columns if c not in id_cols]

# Fill nulls in pivoted feature columns with 0.0 so VectorAssembler can include all rows
df_pca_ready = df_pivot.fillna(0.0, subset=feature_cols)

assembler = VectorAssembler(
    inputCols=feature_cols, outputCol="raw_features", handleInvalid="skip"
)
assembled_df = assembler.transform(df_pca_ready)

scaler = StandardScaler(
    inputCol="raw_features", outputCol="scaled_features", withMean=True, withStd=True
)
scaled_df = scaler.fit(assembled_df).transform(assembled_df)

pca = PCA(k=2, inputCol="scaled_features", outputCol="pca_features")
pca_df = pca.fit(scaled_df).transform(scaled_df)

get_pc1 = udf(lambda v: float(v[0]) if v is not None else None, DoubleType())
get_pc2 = udf(lambda v: float(v[1]) if v is not None else None, DoubleType())

pca_plot_df = (
    pca_df.withColumn("PC1", get_pc1("pca_features"))
    .withColumn("PC2", get_pc2("pca_features"))
    .select("LocationDesc", "YearStart", "YearEnd", "PC1", "PC2")
)

# Display output for scatter plot (created manually)
display(pca_plot_df)