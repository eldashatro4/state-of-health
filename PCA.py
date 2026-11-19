from pyspark.ml import Pipeline
from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import col, regexp_replace
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler, PCA


file_path = "/Volumes/workspace/default/health_data_volume/chronic_2016_2020.csv"

df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(file_path)

# display(df.limit(5))


columns_to_drop = [
    'DataSource', 'DataValueFootnoteSymbol', 'DataValueFootnote', 
    'Geolocation', 'TopicID', 'QuestionID', 'ResponseID', 
    'DataValueTypeID', 'StratificationCategoryID1', 'StratificationID1',
    'StratificationCategoryID2', 'StratificationID2', 'StratificationCategoryID3', 'StratificationID3',
    'Response', 'DataValueUnit' 
]

df_cleaned = df.drop(*columns_to_drop)

# Cast numeric columns properly (handling non-numeric values gracefully)
df_cleaned = df_cleaned \
    .withColumn("DataValue", regexp_replace(col("DataValue"), ",", "").cast("double")) \
    .withColumn("LowConfidenceLimit", regexp_replace(col("LowConfidenceLimit"), ",", "").cast("double")) \
    .withColumn("HighConfidenceLimit", regexp_replace(col("HighConfidenceLimit"), ",", "").cast("double"))

# Drop rows where critical numeric values are null
df_cleaned = df_cleaned.dropna(subset=["DataValue"])


# Choose categorical columns to one-hot encode 
categorical_cols = ["Topic", "DataValueType", "LocationDesc"]

indexers = [StringIndexer(inputCol=c, outputCol=f"{c}_indexed", handleInvalid="keep") for c in categorical_cols]
encoders = [OneHotEncoder(inputCol=f"{c}_indexed", outputCol=f"{c}_vec") for c in categorical_cols]


# Combine numeric features and the newly created one-hot encoded vectors
numeric_cols = ["DataValue", "LowConfidenceLimit", "HighConfidenceLimit", "YearStart"]
feature_input_cols = numeric_cols + [f"{c}_vec" for c in categorical_cols]

assembler = VectorAssembler(inputCols=feature_input_cols, outputCol="raw_features", handleInvalid="skip")

# Scaling is mandatory for PCA so large ranges don't dominate the components
scaler = StandardScaler(inputCol="raw_features", outputCol="features", withMean=True, withStd=True)

# Apply PCA to reduce the dimensionality to 2 components
pca = PCA(k=2, inputCol="features", outputCol="pca_features")

# Build and fit a Spark Pipeline containing all these steps
pipeline = Pipeline(stages=indexers + encoders + [assembler, scaler, pca])

model = pipeline.fit(df_cleaned)
transformed_df = model.transform(df_cleaned)

# Preview the final 2D PCA output alongside location info
# display(transformed_df.select("LocationAbbr", "YearStart", "pca_features").limit(10))

# Extract PC1 and PC2 from the vector
get_pc1 = udf(lambda v: float(v[0]), DoubleType())
get_pc2 = udf(lambda v: float(v[1]), DoubleType())

final_pca_df = transformed_df \
    .withColumn("PC1", get_pc1("pca_features")) \
    .withColumn("PC2", get_pc2("pca_features"))

# Display columns needed for the chart
display(final_pca_df.select("LocationAbbr", "YearStart", "PC1", "PC2"))