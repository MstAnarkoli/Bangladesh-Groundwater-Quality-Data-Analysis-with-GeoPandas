import pandas as pd
import geopandas as gpd


def clean_groundwater_data(df):
    """Clean the groundwater data before spatial transformation."""

    df = df.copy()

    # Remove the units row
    df = df[df["SAMPLE_ID"].notna()].copy()

    # Convert coordinates to numeric values
    df["LAT_DEG"] = pd.to_numeric(df["LAT_DEG"], errors="coerce")
    df["LONG_DEG"] = pd.to_numeric(df["LONG_DEG"], errors="coerce")

    # Remove records without valid coordinates
    df = df.dropna(subset=["LAT_DEG", "LONG_DEG"])

    return df


def transform_arsenic_data(df):
    """Create numeric arsenic values while preserving censored results."""

    df = df.copy()

    df["As_numeric"] = pd.to_numeric(
        df["As"].str.replace("<", "", regex=False).str.strip(),
        errors="coerce"
    )

    df["As_censored"] = df["As"].str.startswith("<")

    return df


def create_geodataframe(df):
    """Convert groundwater coordinates into spatial point geometry."""

    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(
            df["LONG_DEG"],
            df["LAT_DEG"]
        ),
        crs="EPSG:4326"
    )

    return gdf


def spatial_join_districts(gdf, districts):
    """Assign district names to groundwater points using a spatial join."""

    joined = gpd.sjoin(
        gdf,
        districts,
        how="left",
        predicate="within"
    )

    # Keep the district found by the spatial join
    joined["district_spatial"] = joined["adm2_en"]

    # For points not matched spatially, retain the original
    # district recorded in the groundwater dataset
    joined["district_final"] = joined["district_spatial"].fillna(
        joined["DISTRICT"]
    )

    # Remove the boundary feature ID created by the spatial join.
    # GeoPackage uses its own feature ID field.
    if "fid" in joined.columns:
        joined = joined.drop(columns=["fid"])

    return joined