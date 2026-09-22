import pandas as pd
import geopandas as gpd

from .config import (
    GROUNDWATER_FILE,
    NATIONAL_BOUNDARY_FILE,
    DISTRICT_BOUNDARY_FILE,
)


def load_groundwater_data(path=GROUNDWATER_FILE):
    """Load and prepare the groundwater CSV file."""

    df = pd.read_csv(
        path,
        skiprows=4
    )

    # Remove completely empty rows and columns
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    return df


def load_boundaries():
    """Load Bangladesh national and district boundary layers."""

    national = gpd.read_file(NATIONAL_BOUNDARY_FILE)

    districts = gpd.read_file(DISTRICT_BOUNDARY_FILE)

    return national, districts


def save_geodataframe(gdf, path):
    """Save the GeoDataFrame as a GeoPackage."""

    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        path.unlink()

    gdf.to_file(
        path,
        layer="groundwater",
        driver="GPKG"
    )