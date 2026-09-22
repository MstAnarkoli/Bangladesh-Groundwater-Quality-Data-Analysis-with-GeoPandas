# Geospatial Data Analysis with Python: Bangladesh Groundwater Quality

A Python-based geospatial analysis project exploring groundwater sampling locations and arsenic concentration across Bangladesh using **Pandas, GeoPandas, and Matplotlib**.

The project transforms groundwater CSV data into a spatial dataset, performs a spatial join with Bangladesh district boundaries, analyses arsenic concentrations by division and district, and generates geographic visualizations.


## Project Overview

This project demonstrates how geospatial Python tools can be used to:

* Clean and prepare groundwater sampling data
* Convert latitude/longitude coordinates into geographic points
* Create and work with GeoDataFrames
* Use Coordinate Reference Systems (CRS)
* Perform spatial joins with administrative boundaries
* Analyse arsenic concentration geographically
* Compare groundwater arsenic levels across divisions and districts
* Create maps and statistical visualizations
* Create interctive maps 
* Save processed spatial data in GeoPackage format


## Technologies Used

* **Python**
* **Pandas** – data cleaning and manipulation
* **GeoPandas** – geospatial data processing
* **Matplotlib** – data visualization
* **NumPy** – numerical operations
* **GeoPackage / GeoJSON** – geospatial data formats
* **EPSG:4326 (WGS 84)** – coordinate reference system


## Project Structure

```text
Geospatial analysis by Python/
│
├── data/
│   ├── groundwater.csv
│   └── boundaries/
│       ├── bangladesh_boundary.geojson
│       └── district_boundaries.geojson
│
├── output/
│   ├── groundwater_transformed.gpkg
│   ├── sampling_locations.png
│   ├── arsenic_map.png
│   ├── arsenic_by_division.png
│   ├── top_districts_arsenic.png
│   ├── district_arsenic_map.png
│   └── arsenic_interactive_map.html
│
├── src/
│   └── groundwater_analysis/
│       ├── __init__.py
│       ├── __main__.py
│       ├── config.py
│       ├── io.py
│       ├── logging_config.py
│       ├── pipeline.py
│       ├── transform.py
│       └── visualization.py
│
│ 
├── requirements.txt
└── README.md
```

## Data Processing Workflow

The project follows this workflow:

```text
Groundwater CSV
      ↓
Data cleaning
      ↓
Arsenic data preparation
      ↓
Latitude / Longitude validation
      ↓
GeoDataFrame creation
      ↓
CRS: EPSG:4326
      ↓
Load Bangladesh boundaries
      ↓
Spatial Join
      ↓
District assignment
      ↓
Arsenic analysis
      ↓
Maps and visualizations
      ↓
GeoPackage output
```

## Dataset

After cleaning, the groundwater dataset contains:

**3,534 sampling records**

The data includes geographical coordinates and groundwater-quality information, including arsenic concentration.

## Geospatial Processing

Latitude and longitude coordinates are converted into Point geometries using GeoPandas.

The project uses:

```text
EPSG:4326 – WGS 84
```

The groundwater points are spatially joined with Bangladesh district boundaries using:

```python
gpd.sjoin(
    gdf,
    districts,
    how="left",
    predicate="within"
)
```

The spatial join produced:

* **3,518 spatially matched records**
* **16 records requiring fallback district information**
* **0 records without a final district assignment**

For the 16 unmatched points, the original district value in the groundwater dataset is retained as a documented fallback rather than deleting the observations.


## Analysis

### Division-Level Analysis

Arsenic concentration was summarized for six administrative divisions:

| Division   | Samples |   Mean | Median | Maximum |
| ---------- | ------: | -----: | -----: | ------: |
| Chittagong |     445 | 137.08 |  51.50 |    1090 |
| Khulna     |     474 |  84.80 |  30.75 |    1660 |
| Sylhet     |     260 |  29.16 |  14.00 |     320 |
| Dhaka      |     988 |  63.32 |  11.70 |     924 |
| Barisal    |     295 |  38.62 |   1.80 |     862 |
| Rajshahi   |   1,072 |  12.25 |   0.60 |     708 |

Median values are included because arsenic concentrations show substantial variation and extreme observations.

### District-Level Analysis

District-level median arsenic concentration was calculated using the spatially reconciled `district_final` field.

Examples of districts with high median values in the dataset include:

* Chandpur
* Munshiganj
* Gopalganj
* Comilla
* Noakhali
* Faridpur
* Bagerhat
* Satkhira

These results describe the available groundwater samples and should not automatically be interpreted as representative of the entire district.

## Visualizations

The project generates five visualizations.

### Sampling Locations

`sampling_locations.png`

Shows the geographical distribution of groundwater sampling points across Bangladesh.

### Arsenic Concentration Map

`arsenic_map.png`

Displays groundwater sampling locations according to arsenic concentration.

### Arsenic by Division

`arsenic_by_division.png`

Compares the distribution of arsenic concentration across Bangladesh's administrative divisions.

### Top Districts

`top_districts_arsenic.png`

Visualizes districts according to median arsenic concentration.

### District-Level Arsenic Map

`district_arsenic_map.png`

A choropleth map showing median arsenic concentration by district. Districts without groundwater samples are displayed separately as missing data.

### Interactive Arsenic Map

`arsenic_interactive_map.html`

An interactive map of groundwater sampling locations using GeoPandas and Folium. Users can zoom and pan across Bangladesh and inspect individual sampling points. The map displays arsenic concentration using colour and provides information such as sample ID, district, division, and arsenic concentration when exploring the points.


## Output Data

The processed spatial dataset is saved as:

```text
output/groundwater_transformed.gpkg
```

The GeoPackage contains the groundwater attributes, point geometries, arsenic information, CRS, spatially joined district information, and final district assignments.

## Running the Project

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd "Geospatial analysis by Python"
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the analysis

```bash
python -m src.groundwater_analysis
```

The pipeline will process the groundwater data and generate the GeoPackage and visualization files in the `output/` directory.


## Project Architecture

The project uses a modular structure to separate different responsibilities.

### `config.py`

Stores project paths, input files, and output filenames.

### `io.py`

Handles:

* Groundwater data loading
* Boundary loading
* GeoPackage output

### `transform.py`

Handles:

* Data cleaning
* Arsenic transformation
* GeoDataFrame creation
* Spatial joining

### `visualization.py`

Contains functions for generating the project maps and statistical visualizations.

### `pipeline.py`

Coordinates the complete analysis workflow.

### `__main__.py`

Provides the command-line entry point:

```bash
python -m src.groundwater_analysis
```

## Learning Outcomes

Through this project, the following practical skills were developed:

* Working with environmental datasets
* Data cleaning with Pandas
* Geospatial data processing with GeoPandas
* Creating Point geometries
* Understanding and applying CRS
* Working with GeoJSON and GeoPackage formats
* Performing spatial joins
* Aggregating environmental measurements geographically
* Creating choropleth and statistical maps
* Structuring a Python data-analysis project into modules
* Building a reproducible analysis pipeline

## Author

**Mst Anarkoli**

Data Science Project – Geospatial Data Analysis with Python
