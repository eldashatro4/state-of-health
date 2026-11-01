# State of Health

### Mapping the Socioeconomic Drivers of Chronic Disease Across U.S. States

**CS 483 Course Project — Team: Healthcare**

| Name | NetID |
|------|-------|
| Elda Shatro | eshatr2 |
| Advait Mallela | amalle5 |
| Aashika Lilaramani | alila2 |
| Saifullah Shakeel | sshak7 |

## Research Question

> **Which state-level demographic, socioeconomic, and healthcare factors are associated with higher chronic disease rates?**

We combine state-level chronic disease indicators with supplementary data on income, employment, housing, and health insurance coverage to find out how a state's resources and demographics relate to its chronic disease rates.

**Time frame:** We focus on **2016–2020**, so every dataset in `data/` has been cut down to those years.

## Datasets

### Base dataset
- **U.S. Chronic Disease Indicators (CDI)**: chronic disease indicators by year and state (2015–2023).
  Source: https://catalog.data.gov/dataset/u-s-chronic-disease-indicators
  *(Not committed to the repo yet. Download it from the link above.)*

### Supplementary datasets (state-wide factors)
- **American Community Survey (ACS) 2016–2020 5-year estimates**: `data/ACS_2016_2020.csv`
  One row per state, with 144 columns covering travel time to work, poverty, household income distribution, unemployment by age group, housing crowding, housing cost burden, and occupation categories.
  Source: https://www.census.gov/programs-surveys/acs
- **Small Area Health Insurance Estimates (SAHIE)**: `data/sahie_combined.zip` (contains `sahie_combined.csv`, about 400 MB once unzipped)
  Yearly estimates of health insurance coverage (insured and uninsured counts and percentages) by state and county, broken down by age, race, sex, and income-to-poverty ratio.
  Source: https://www.census.gov/programs-surveys/sahie.html

Data dictionaries for all three datasets are in `data_dictionaries/`.

## Methodology

1. **Data integration:** Use Spark or Databricks to merge geospatial data and the supplementary features into the base dataset by state and year.
2. **Dimensionality reduction:** Apply SVD to the chronic disease indicators.
3. **Clustering:** Use K-means to group states with similar chronic disease profiles.
4. **Regression:** Fit linear regression to find which features have the strongest association with chronic disease indicators.
5. **Visualization:** Build an interactive Power BI dashboard that overlays disease indicators and their factors on a U.S. map.

## Repository Structure

```
state-of-health/
├── data/
│   ├── ACS_2016_2020.csv          # ACS socioeconomic features by state
│   └── sahie_combined.zip         # SAHIE health insurance estimates (zipped CSV)
├── data_dictionaries/
│   ├── ACS_datadictionary.pdf
│   ├── chronic_disease_dictionary.pdf
│   └── sahie_datadictionary.pdf
├── doc/
│   └── Project Proposal - CS483.pdf
├── main.py                        # Entry point (placeholder)
└── README.md
```

## Getting Started

```bash
# Clone the repository and enter it
git clone https://github.com/eldashatro4/state-of-health.git
cd state-of-health

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Unzip the SAHIE data
unzip data/sahie_combined.zip -d data/

# Run the project
python main.py
```

> **Note:** `data/sahie_combined.csv` is about 400 MB. Don't commit the unzipped file. Keep only the `.zip` in the repo.

## Schedule

| Milestone | Due | Deliverables |
|-----------|-----|--------------|
| Midterm Check | Nov 11, 2026 | Interim report: progress, roadblocks, draft of work so far |
| Final Report | Dec 6, 2026 | Final report with data and code: problem context, algorithms, dashboard output |
| Final Presentation | Dec 8, 2026 | Class presentation: problem intro, experiment results, dashboard |

## Team Process

- **Development model:** Agile/Scrum
- **Project management:** Jira
- **Version control:** Git/GitHub
