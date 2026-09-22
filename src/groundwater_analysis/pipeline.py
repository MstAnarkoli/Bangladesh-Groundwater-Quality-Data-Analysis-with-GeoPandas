from .config import (
    TRANSFORMED_DATA_FILE,
    SAMPLING_MAP_FILE,
    ARSENIC_MAP_FILE,
    DIVISION_BOXPLOT_FILE,
    TOP_DISTRICTS_MAP_FILE,
    DISTRICT_ARSENIC_MAP_FILE,
    INTERACTIVE_MAP_FILE
)
from .io import (
    load_groundwater_data,
    load_boundaries,
    save_geodataframe,
)
from .transform import (
    clean_groundwater_data,
    transform_arsenic_data,
    create_geodataframe,
    spatial_join_districts,
)
from .visualization import (
    plot_sampling_locations,
    plot_arsenic_map,
    plot_arsenic_by_division,
    plot_top_districts,
    plot_district_arsenic,
    create_interactive_arsenic_map
)


def run_pipeline():
    """Run the groundwater data transformation and visualization pipeline."""

    df = load_groundwater_data()

    df = clean_groundwater_data(df)

    df = transform_arsenic_data(df)

    gdf = create_geodataframe(df)

    

    # Load administrative boundaries
    national, districts = load_boundaries()

    # Spatially join groundwater points with district boundaries
    gdf = spatial_join_districts(gdf, districts)
    save_geodataframe(gdf, TRANSFORMED_DATA_FILE)

    # Create visualizations
    plot_sampling_locations(
        gdf,
        SAMPLING_MAP_FILE,
        national,
        districts
    )

    plot_arsenic_map(
        gdf,
        ARSENIC_MAP_FILE,
        national,
        districts
    )

    plot_arsenic_by_division(
        gdf,
        DIVISION_BOXPLOT_FILE
    )

    plot_top_districts(
        gdf,
        TOP_DISTRICTS_MAP_FILE
    )

    plot_district_arsenic(
        gdf,
        DISTRICT_ARSENIC_MAP_FILE,
        national,
        districts
    )

    create_interactive_arsenic_map(
    gdf,
    INTERACTIVE_MAP_FILE
    )

    return gdf