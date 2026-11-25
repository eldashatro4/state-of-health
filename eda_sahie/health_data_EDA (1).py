# Databricks notebook source
# Load the data
from pyspark.sql import functions as F
from pyspark.sql.types import NumericType
import matplotlib.pyplot as ply

file_path = "/Volumes/workspace/default/health_data_volume/sahie_combined.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)
display(df.limit(10))

print("Rows: ", df.count())
print("Columns: ", len(df.columns))
df.printSchema()

# COMMAND ----------

# Feature Selection
numeric_cols = [f.name for f in df.schema.fields
                if isinstance(f.dataType, NumericType)]
print("Numeric columns: ", numeric_cols)
categorical_cols = [c for c in df.columns if c not in numeric_cols]
print("Categorical columns: ", categorical_cols)

selected_cols = ['year', 'state_name', 'agecat', 'racecat', 'sexcat', 'iprcat', 'NIC', 'NUI']

df_selected = df.select(*selected_cols)

# Mapping Dictionaries for Selected Columns

age_map = {
    0: "Under 65 years",
    1: "18 to 64 years",
    2: "40 to 64 years",
    3: "50 to 64 years",
    4: "Under 19 years",
    5: "21 to 64 years",
    6: "21 to 29 years"
}

race_map = {
    0: "All races",
    1: "White, non-Hispanic",
    2: "Black, non-Hispanic",
    3: "Hispanic or Latino",
    4: "American Indian/Alaska Native",
    5: "Asian, non-Hispanic",
    6: "Native Hawaiian/Pacific Islander",
    7: "Two or More Races"
}

sex_map = {
    0: "Both sexes",
    1: "Male",
    2: "Female"
}

income_map = {
    0: "All income levels",
    1: "At or below 200% poverty",
    2: "At or below 250% poverty",
    3: "At or below 138% poverty",
    4: "At or below 400% poverty",
    5: "Between 138%-400% poverty"
}


# Function to replace numeric codes with labels
def map_category(df, column, mapping):
    map_expr = F.create_map(
        *[x for k, v in mapping.items()
          for x in (F.lit(k), F.lit(v))]
    )

    return df.withColumn(
        column,
        map_expr[F.col(column).cast("int")]
    )

# Replace category codes with descriptive labels
df_selected = map_category(df_selected, "agecat", age_map)
df_selected = map_category(df_selected, "racecat", race_map)
df_selected = map_category(df_selected, "sexcat", sex_map)
df_selected = map_category(df_selected, "iprcat", income_map)

display(df_selected.limit(10))

# Note - the race, age, income, and gender is categorical data that is being explored from the original dataset. The cleaned data will not include these categories as the cleaned data intends to keep one value for each state per year for merging, and therefore the values that we will be focusing the most on is NUI (number of uninsured individuals) and NIC (number of insured individuals). The other columns will consist of values of 0 as per the maps above to indicate that the individual data points represent all individuals belonging to each category.



# COMMAND ----------



# Descriptive Statistics
from pyspark.sql import functions as F

selected_num = ["NIC", "NUI"]
selected_cat = ["state_name", "agecat", "racecat", "sexcat", "iprcat"]
selected_time = ["year"]

# Convert NIC and NUI to numeric values
for col in selected_num:
    df_selected = df_selected.withColumn(
        col,
        F.expr(
            f"try_cast(regexp_replace(trim(`{col}`), ',', '') as double)"
        )
    )

# Verify data types
df_selected.select(*selected_num).printSchema()

# Numerical descriptive statistics
for col in selected_num:
    print(f"\nDescriptive Statistics for {col}")

    # Basic statistics
    display(df_selected.select(col).describe())

    # Median and quartiles
    q1, median, q3 = df_selected.approxQuantile(
        col, [0.25, 0.50, 0.75], 0.01
    )

    print(f"Q1: {q1}")
    print(f"Median: {median}")
    print(f"Q3: {q3}")
    print()

# Frequency counts for categorical features
for col in selected_cat:
    print(f"Value Counts for {col}:")

    display(
        df_selected.groupBy(col)
        .count()
        .orderBy(F.desc("count"))
    )

# Number of records per year
print("Number of Records per Year:")

display(
    df_selected.groupBy("year")
    .count()
    .orderBy("year")
)



# COMMAND ----------

# Visualizations and Key Observations

# The initial histograms and box plots for NIC and NUI appeared highly compressed due to substantial differences in population counts. Logarithmic transformations were applied to improve visualization and reveal the underlying distributions. Outlier markers were hidden in the box plots for readability, but the original observations were retained for subsequent outlier detection and analysis.
import matplotlib.pyplot as plt
import numpy as np

# Random sample for plotting
pdf = df_selected.sample(
    fraction=0.1, seed=42
).limit(5000).toPandas()

for col in selected_num:
    data = pdf[col].dropna()
    data = data[data >= 0]

    plt.figure(figsize=(10, 5))

    plt.hist(np.log1p(data), bins=40, edgecolor="black")

    plt.title(f"Distribution of {col} (Log Scale)")
    plt.xlabel(f"Log(1 + {col})")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


for col in selected_num:
    data = pdf[col].dropna()
    data = data[data >= 0]

    plt.figure(figsize=(10, 4))

    plt.boxplot(
        np.log1p(data),
        vert=False,
    )

    plt.title(f"Box Plot of {col} (Log Scale)")
    plt.xlabel(f"Log(1 + {col})")
    plt.tight_layout()
    plt.show()



plt.figure(figsize=(9, 6))

plt.scatter(
    np.log1p(pdf["NIC"]),
    np.log1p(pdf["NUI"]),
    alpha=0.4,
    s=15
)

plt.title("NIC vs NUI (Log Scale)")
plt.xlabel("Log(1 + NIC)")
plt.ylabel("Log(1 + NUI)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# Numerical Visualizations — Key Observations & Takeaways

# Histograms: After applying logarithmic transformations, the distributions of NIC (number insured) and NUI (number uninsured) appeared approximately symmetric and centered, resembling a normal distribution. This suggests that most observations are concentrated around the middle of the log-transformed values, with fewer observations at the extremes.

# Box Plots: The box plots revealed several potential outliers in both NIC and NUI, including a few unusually low values and a larger number of unusually high values. These extreme observations may reflect differences in population sizes across states and demographic groups. Further outlier detection using the IQR method will help identify and evaluate these values.

# Scatter Plot: The scatter plot showed a clear positive relationship between NIC and NUI, with the points following an upward, somewhat curved pattern. This suggests that observations with larger insured populations generally also have larger uninsured populations. However, this relationship may be influenced by differences in overall population size rather than insurance coverage rates.

# Overall Takeaway: The logarithmic transformations improved the readability of the numerical visualizations and revealed underlying distribution patterns. While NIC and NUI appear positively associated, potential outliers and population-size differences should be considered during further analysis.

# COMMAND ----------

# Outlier Detection and Handling
# Our box plots already showed some outliers, so this will help us explicitly identify and count them.

# Outlier Detection using IQR
outlier_results = []

for col in selected_num:
    # Calculate quartiles
    q1, q3 = df_selected.approxQuantile(
        col, [0.25, 0.75], 0.01
    )

    iqr = q3 - q1

    # Calculate outlier boundaries
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    # Identify outliers
    outliers = df_selected.filter(
        (F.col(col) < lower) | (F.col(col) > upper)
    )

    count = outliers.count()

    outlier_results.append(
        (col, q1, q3, iqr, lower, upper, count)
    )

    print(f"{col}: {count} outliers detected")

# Display results
outlier_df = spark.createDataFrame(
    outlier_results,
    ["Feature", "Q1", "Q3", "IQR",
     "Lower_Bound", "Upper_Bound", "Outlier_Count"]
)

display(outlier_df)


# Display examples of outliers
for col in selected_num:
    q1, q3 = df_selected.approxQuantile(
        col, [0.25, 0.75], 0.01
    )

    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    print(f"Outliers for {col}:")

    display(
        df_selected.filter(
            (F.col(col) < lower) | (F.col(col) > upper)
        )
        .select("year", "state_name", "agecat",
                "racecat", "sexcat", "iprcat", col)
        .orderBy(F.desc(col))
        .limit(20)
    )

    
# **Outlier Detection:** The Interquartile Range (IQR) method was applied to NIC (number insured) and NUI (number uninsured) to identify potential outliers. Values falling below Q1 − 1.5 × IQR or above Q3 + 1.5 × IQR were classified as potential outliers.

# **Results:** The analysis identified **233,055 outliers in NIC** and **230,414 outliers in NUI**. These findings indicate substantial variation in population counts across the dataset and are consistent with the extreme values observed in the box plots.

# **Outlier Handling Strategy:** The detected outliers will be retained because NIC and NUI represent population estimates that naturally vary across states and demographic groups. Removing or capping these values could distort the data and eliminate legitimate population differences.

# **Conclusion:** No automatic outlier removal or capping was performed. The original numerical values were preserved. During data cleaning and preprocessing, the dataset will be filtered to the overall demographic categories to create one observation per state and year. Any invalid population counts will be investigated separately.



# COMMAND ----------

# After analysis, we only want to keep year, state_name, total # of NIC and total # of NUI to be merged with other datasets.

# Filter to overall population estimates
df_cleaned = df_selected.filter(
    (F.col("agecat") == "Under 65 years") &
    (F.col("racecat") == "All races") &
    (F.col("sexcat") == "Both sexes") &
    (F.col("iprcat") == "All income levels")
)

# Remove whitespace from state names
df_cleaned = df_cleaned.withColumn(
    "state_name", F.trim(F.col("state_name"))
)

# Keep only the four required columns
df_cleaned = df_cleaned.select(
    "year", "state_name", "NIC", "NUI"
).orderBy("year", "state_name")

display(df_cleaned)


# Aggregate by year and state
df_cleaned = df_cleaned.groupBy(
    "year", "state_name"
).agg(
    F.sum("NIC").cast("long").alias("NIC"),
    F.sum("NUI").cast("long").alias("NUI")
).orderBy("year", "state_name")

display(df_cleaned)

# COMMAND ----------

# Export our final dataset
output_path = "/Volumes/workspace/default/health_data_volume/sahie_cleaned"

df_cleaned.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(output_path)