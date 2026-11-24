Group: Healthcare \- Understanding Chronic Diseases  
Elda Shatro  
Advait Mallela  
Saifullah Shakeel  
Aashika Lilaramani  
**RQ 1.1. Documentation of Data Selection**  
**1\. Project Goal** 

* Briefly describe the problem your team intends to solve.  
  * We intend to answer the following question:  
  * “Which state-level demographic, socioeconomic and healthcare factors are associated with higher chronic disease rates?”  
* Explain why this problem is worth investigating.  
  * This question is worth investigating because it can help the United States make better decisions about how the allocation of resources can greatly improve the health of the people. We aim to understand and identify patterns between these resources and chronic disease rates to reach conclusions on how to better support the country.

**2\. Data Sources**

* Provide direct links to the datasets or data repositories you intend to use.  
  * All datasets have been cut down to focus on the 2016-2020 time-frame.  
  * Base Dataset  
    * U.S. Chronic Disease Indicators (CDI): [https\://catalog.data.gov/dataset/u-s-chronic-disease-indicators](https://catalog.data.gov/dataset/u-s-chronic-disease-indicators)  
  * Supplementary Datasets  
    * American Community Survey (ACS) 2016-2020 5-year Estimates: [https\://www\.census.gov/programs-surveys/acs](https://www.census.gov/programs-surveys/acs)  
    * Small Area Health Insurance Estimates (SAHIE): [https\://www\.census.gov/programs-surveys/sahie.html](https://www.census.gov/programs-surveys/sahie.html)  
    * US State Boundaries (USB):   
      [https\://www\.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)  
* Identify the organizations, platforms, or individuals responsible for publishing the data, when known.  
  * For the base dataset, the data is reported and published by the U.S. Department of Health & Human Services. The data has been collected by CDC’s Division of Population Health, and includes information from the Council of State and Territorial Epidemiologists and the National Association of Chronic Disease Directors.  
  * The ACS data is census survey data, collected by an ongoing survey conducted by the U.S. Census Bureau. The data is collected across the 50 states, the District of Columbia, and Puerto Rico.  
  * The SAHIE data is also census survey data collected by the U.S. Census Bureau. The SAHIE data includes all counties in the United States.  
  * The USB data is published by the U.S. Census Bureau and the data comes from the Census Bureau’s MAF/TIGER geographic database  
* Describe how the data can be accessed or downloaded.  
  * All data can be accessed using the links above. The data can also be downloaded table by table or feature by feature, or can be downloaded as a complete dataset. Supported formats include CSV, JSON, and XML.  
* Identify any licensing, access, or usage restrictions that may affect your project.  
  * The CDI dataset is available for public use and will not affect any licensing issues.  
  * ACS releases its data for public use and download every year and every 5 years in the form of summaries on the Data Census website.  
  * The SAHIE dataset is also for public use and all PII has been removed to support the privacy and safety of participants.  
  * The USB dataset has been published for public use.

**3\. Dataset Description**

* Describe the contents of the dataset  
  * Chronic Health Indicators: A survey of metrics related to chronic diseases for every US state  
  * Statewide Health Insurance Data: Health insurance and poverty data for all counties and states in the United States  
  * American Community Survey Data: General socioeconomic characteristics compiled by the US Census Bureau for every US state  
  * US State Boundary Shape Files: Geospatial data to help visualize the boundaries of the United States  
* Report the available number of records, file sizes, formats, and other relevant characteristics.  
  * Chronic Health Indicators: 124 MB, 398793 records, JSON  
  * Statewide Health Insurance Data: 394 MB, 1601586 records, CSV  
  * American Community Survey Data: 49 KB, 52 records, CSV  
  * US State Boundary Shape Files: 4675 KB, 50 records, Shapefile  
* Identify the important attributes, columns, or fields  
  * Chronic Health Indicators: Topic \- The disease which a record is related to, LocationDesc \- State name, DataValue \- The actual number associated with a metric, DataValueUnit \- The meaning of DataValue (%, number, etc.)  
  * Statewide Health Insurance Data: agecat \- Integer describing age category, racecat \- Integer describing race category, sexcat \- Integer describing gender category, iprcat \- Integer describing income category, NUI \- number uninsured in category, NIC \- number insured in category, state\_name \- State described by category  
  * American Community Survey Data: NAME \- state name, B17019 \- Poverty Status in the past 12 months of families by household type and tenure, B23006 \- Educational attainment by employment status, B23001 \- Employment status by age and sex for individuals over 16  
  * US State Boundary Shape Files: N/A (not tabular)  
* Explain whether you will use one dataset or integrate multiple sources.  
  * I will be integrating these different datasets by joining the statewide health insurance dataset and the American community survey dataset with the chronic health indicators dataset (our base dataset) on their respective keys that describe the state. The state boundary shapefiles will be used in conjunction with the joined dataset and geospatial visualization libraries to help showcase interesting data points

**4\. Analysis of the Five Vs**  
**Volume**

* How many records does the dataset contain?  
  * Chronic Health Indicators: 398,793  
  * Statewide Health Insurance Data: 1,601,586  
  * American Community Survey Data: 52  
  * US State Boundary Shape Files: 50   
* How large is the dataset in bytes, megabytes, or gigabytes?  
  * Chronic Health Indicators: 124 MB  
  * Statewide Health Insurance Data: 394 MB  
  * American Community Survey Data: 49 KB  
  * US State Boundary Shapefiles: 4675 KB  
* Does the dataset contain multiple files, tables, or partitions?  
  * The shapefiles, as per the format, are distributed into multiple files that are all loaded together, and all the other datasets are contained in a single file each  
* Will your team analyze the entire dataset or only a subset?  
  * Our team will analyze the entire dataset, but if we begin to run into performance issues then we will reduce the features we are processing. We will also be looking at a subset of the data between the years 2016 and 2020, as this is the greatest range where all of our datasets contain datapoints  
* What challenges might arise when processing the data of this size, and as its size increases?  
  * Processing this data using standard libraries such as Pandas may lead to slow performance, especially depending on the machine we are running our scripts on. This will be especially true as the dataset size increases if we feel the need to include additional data, and as we try to perform machine learning techniques on the data. As such, we plan to use Databricks or Spark to bridge this performance gap 

**Velocity**

* Is the data generated continuously, periodically, or as a one-time collection?  
  * We are using 4 datasets. They are all generated periodically. Each one is collected over time by a federal agency and published once or twice a year.  
* How frequently is the dataset updated?  
  * U.S Chronic Disease Indicators (CDC): updated once a year or less  
  * ACS 5-Year Estimates (Census Bureau): updated once a year  
  * US State Boundaries: updated once a year  
  * SAHIE: updated once a year  
* Can new records be incorporated as they become available?  
  * Yes, most of the time each new year release has the same structure which consists of one record per state or each year. It can be appended and merged on state and year without changing the schema itself. However, the CDC changed its indicators in 2024, therefore newer CDI data may need its indicators mapped to the old ones.   
* Would a real-time or streaming architecture be useful for this project, or is batch processing sufficient?  
  * Batch processing is sufficient. The data arrived at most once per year, the analysis compares states over several years, and SVD, K-means and regression all run on the full dataset at once. On the other side, streaming would add complexity.  
* If the dataset is static, how could the system accommodate future updates?  
  * Make the year range a setting so a new year can be added by rerunning the pipeline.  
  * Schedule a yearly bath job in Databricks to match the release cycle and refresh the Power BI dashboard.  
  * Add schema checks to catch changed columns or indicators before they break the merge.

**Variety**

* Does your project use more than one data source? Identify the source of each dataset and explain what information it contributes.  
  * Chronic Health Indicators: state by state statistics on chronic disease indicators  
    * [https\://catalog.data.gov/dataset/u-s-chronic-disease-indicators](https://catalog.data.gov/dataset/u-s-chronic-disease-indicators)  
  * Statewide Health Insurance Data: statistics about each state such as health insurance and poverty data  
    * [https\://www\.census.gov/programs-surveys/sahie.html](https://www.census.gov/programs-surveys/sahie.html)  
  * American Community Survey Data: State level data describing socioeconomic characteristics such as educational attainment  
    * [https\://www\.census.gov/programs-surveys/acs](https://www.census.gov/programs-surveys/acs)  
  * US State Boundary Shapefiles: Data describing US state boundaries to be used for visualizations  
    * [https\://www\.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)  
* What file formats or data structures are involved? Identify the formats and structures of your data, such as CSV, JSON, relational tables, text, images, or other relevant formats.  
  * The first dataset listed above is a JSON file, and the next two data sources listed above are CSVs, and the last data source is a geographic shapefile  
* Does the project combine different types of information? Explain whether the data comes from multiple sources and, if so, how the sources relate to one another.  
  * The data comes from multiple US government sources, specifically [data.gov](http://data.gov) and [census.gov](http://census.gov), and all of the datasets contain the given state for each statistic. Thus, we can use the US state as a key to join the datasets together  
* Describe the challenges involved in combining, transforming, or processing the different data types.  
  * The chronic health indicators dataset is very big so joining information to this dataset will require us to use a big data processing platform such as Databricks or Spark. It is also a JSON dataset, so we will need to convert it to a DataFrame so that it can be easily manipulated in the same format as the other CSVs  
* Will you need to clean, transform, or integrate data from different sources?  
  * Because our four datasets are taken from different sources, we will need to remove missing values and unnecessary features, convert from JSON to tabular, and then join all of the tabular datasets together using the US state as the key. We will also need to find a way to join this tabular data together with the geographic data in order to create visualizations  
* How will your system handle these different formats?  
  * Our system will combine all non-visualization datasets together using Spark or Pandas Dataframes, and of course, we will first convert the JSON dataset into this format. To visualize the data using the shapefiles, we can use a Python library dedicated to GIS visualization such as GeoPandas

**Veracity**

* Who collected or published the data?  
  * The base dataset was published by the U.S. Department of Health & Human Services. The ACS, SAHIE, and USB data is collected and published by the U.S. Census Bureau.  
* Is the source trustworthy and well-documented?  
  * All four datasets are provided by various government departments within the United States and were downloaded from government websites. Therefore, we can assume that the source of the data is trustworthy. Additionally, the datasets included data dictionaries and other supporting information, so the data is also well-documented.  
* Are there missing values, duplicates, or inconsistent records?  
  * CDI dataset has large amount of missing values in the following columns: Response, DataValueFootnoteSymbol, DataValueFootnote, StrateficationCategory2, Stratification2, StrateficationCategory3, Stratification3. None of these columns are particularly relevant to our project goal.  
  * No columns in the ACS, SAHIE, or USB datasets contain any missing values or duplicate rows.  
* Could the data contain measurement errors, outdated information, or biases?  
  * Although it is possible that the data contains some measurement errors, I do not believe the datasets are likely to contain outdated information or biases. All four datasets are collected by the U.S. government and are unlikely to have bias as CDI is based on demographic data while ACS and SAHIE datasets are represented by random samples of the U.S. population. It is also unlikely that the USB geospatial data has many measurement errors as it is collected by the U.S. government and updated every time there are any boundary changes.  
* What validation, cleaning, or preprocessing steps might be necessary?  
  * We will need to identify and resolve issues such as missing values, duplicates, or outliers. We may also need to work to consolidate the datasets into merged tables or connected tables as necessary based on our overall analysis, and we will need to map our geospatial data to our base chronic disease dataset to provide geographical and map-based visualizations.


**Value**

* What problem are you trying to solve?  
  * Chronic diseases such diabetes, heart disease, obesity and COPD are a leading cause of death and health care costs. Also, their rates vary widely from state to state. Health data is usually published separately from economic and insurance data, so it’s hard to see why some states have higher rates than others. We combine CDC chronic disease data with Census data on income, employment, housing and insurance to find which state-level factors are linked to higher chronic disease rates.   
* Who could benefit from the results?  
  * State health departments  
  * Public health researchers  
  * Nonprofits and community health organizations  
  * Healthcare organizations  
* What questions do you want your system to answer?  
1. Which socioeconomic factors, such as poverty, income, unemployment and housing cost are most strongly linked to chronic disease rates?  
2. Do states with higher uninsured rates have higher chronic diseases?  
3. Which states have similar chronic disease profiles and what are the factors?  
4. Are there states with high disease rates despite good economic conditions, or low rates despite poor conditions?  
* What patterns, predictions, recommendations, or other insights could you extract?  
  * We can instruct patterns such as SVD and K-means. Svd condenses dozens of correlated disease indicators into a few main components. One might be the “cardimetabolic burden” and the other one might be “respiratory and tobacco-related burden”. We can use K-means to group states into clusters, such as high-burden clustered and describe each cluster with ACS and SAHIE variables.   
  * Associations for each major disease indicator we rank which features have the largest standardized coefficients. For example we can determine how a 1 point increase in the poverty rate is associated with diabetes, or other respiratories diseases.  
  * We will use the Power BI dashboard which will show disease indicators, clusters and their related factors on a U.S map so people without the technical background can also explore the results.  
* How will you determine whether your results are useful?  
  * By performing model quality. We will use R^2 plus cross validation error. Based on the number of the observations we will use section or regularization and check for multicollinearity.  
  * By checking cluster quality. We will use silhouette scores and the elbow methods to choose k. We will also check that the clusters stay stable across years and differ on the socioeconomic features.  
  * SVD quality: we will check how much variance the top components explain and whether those components have a clear meaning.  
  * Agreement with known research

**5\. Data Preparation**

* Identify anticipated data-cleaning, transformation, integration, or preprocessing tasks.  
  * We have already addressed one form of data transformation. For our project, we wanted to use a specific subset of years to make our analysis more focused. We trimmed down all datasets to only contain information from years 2016 to 2020\.  
  * After a brief exploration of the CDI data, we identified a few columns that have large amounts of missing values. Although those columns are not relevant to our research question, it is important to deal with these data quality issues. We are also expecting to run into some outliers or duplicate values, and those will be handled depending on the context of the specific dataset or feature.   
  * The SAHIE dataset is based on county rather than state, so we anticipate some data transformations to take place so that we can aggregate those values into state categories for each year from 2016-2020.  
* Explain any challenges you expect to encounter.  
  * We may initially struggle with some of the data cleaning due to not knowing exactly how to take care of specific issues \- however, we believe once we have cleaned our data thoroughly we can move forward with the rest of our analysis. We also anticipate a few issues with connecting our geographic JSON data with the rest of our datasets, but we are confident we can resolve those issues.


**6\. Limitations and Risks**

* Identify any limitations in data availability, quality, representativeness, or update frequency.  
  * Small sample size: Each year has only 51 observations. Models with many features may overfit, so we will use few features, regularizations and cross-validation.  
  * Quality: CDC prevalence data comes from self-reported surveys, which are subject to reporting bias. SAHIE values are model estimates not direct counts.  
  * The data is aggregated at the state level which hides differences between counties and communities.   
  * The data is released several years late, so 2016-2020 may not reflect current conditions. COVID-19 also disrupted 2020 data collection.  
* Explain how these limitations might affect the project.  
  * The dataset has few observations, models with many features may overfit and give unstable results, so we will use few features, regularization and cross-validation. Indicators with too many gaps must be dropped, which narrows the disease profiles used for clustering.   
  * Survey bias and estimation error and noise can weaken the relationships we detect. Also, the year 2020 may be an outlier that distorts trends or clusters, so we may analyze it separately. In conclusion, our results will show association as we expect but not causes. 