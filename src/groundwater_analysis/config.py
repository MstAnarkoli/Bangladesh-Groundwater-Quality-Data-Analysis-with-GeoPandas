from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Project directories
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Input file
GROUNDWATER_FILE = DATA_DIR / "groundwater.csv"

# Boundary files
NATIONAL_BOUNDARY_FILE = DATA_DIR / "boundaries" / "bangladesh_boundary.geojson"
DISTRICT_BOUNDARY_FILE = DATA_DIR / "boundaries" / "district_boundaries.geojson"

# Output file
TRANSFORMED_DATA_FILE = OUTPUT_DIR / "groundwater_transformed.gpkg"

SAMPLING_MAP_FILE = OUTPUT_DIR / "sampling_locations.png"

ARSENIC_MAP_FILE = OUTPUT_DIR / "arsenic_map.png"

DIVISION_BOXPLOT_FILE = OUTPUT_DIR / "arsenic_by_division.png"

TOP_DISTRICTS_MAP_FILE = OUTPUT_DIR / "top_districts_arsenic.png"

DISTRICT_ARSENIC_MAP_FILE = OUTPUT_DIR / "district_arsenic_map.png"

INTERACTIVE_MAP_FILE = OUTPUT_DIR / "arsenic_interactive_map.html"