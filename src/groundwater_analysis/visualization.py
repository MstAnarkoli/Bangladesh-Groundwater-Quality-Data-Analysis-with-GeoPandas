import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LogNorm


def plot_sampling_locations(gdf, output_path, national, districts):
    """Create and save a map of groundwater sampling locations with boundaries."""

    fig, ax = plt.subplots(figsize=(10, 12))

    # District boundaries
    districts.boundary.plot(
        ax=ax,
        linewidth=0.6,
        color="black",
        alpha=0.7
    )

    # National boundary
    national.boundary.plot(
        ax=ax,
        linewidth=1.5,
        color="black"
    )

    # Groundwater sampling locations
    gdf.plot(
        ax=ax,
        markersize=5,
        alpha=0.6
    )

    ax.set_title(
        "Groundwater Sampling Locations",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def plot_arsenic_map(gdf, output_path, national, districts):
    """Create and save a spatial map of arsenic concentrations with boundaries."""

    fig, ax = plt.subplots(figsize=(10, 12))

    plot_data = gdf[gdf["As_numeric"] > 0].copy()

    # District boundaries
    districts.boundary.plot(
        ax=ax,
        linewidth=0.5,
        color="black",
        alpha=0.6
    )

    # National boundary
    national.boundary.plot(
        ax=ax,
        linewidth=1.5,
        color="black"
    )

    # Arsenic concentrations
    plot_data.plot(
        ax=ax,
        column="As_numeric",
        cmap="viridis",
        norm=LogNorm(
            vmin=plot_data["As_numeric"].min(),
            vmax=plot_data["As_numeric"].max()
        ),
        markersize=8,
        alpha=0.7,
        legend=True,
        legend_kwds={
            "label": "Arsenic concentration"
        }
    )

    ax.set_title(
        "Spatial Distribution of Arsenic Concentration",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

def plot_arsenic_by_division(gdf, output_path):
    """Create a colorful boxplot of arsenic concentration by division."""

    divisions = [
        "Chittagong",
        "Dhaka",
        "Rajshahi",
        "Khulna",
        "Barisal",
        "Sylhet",
    ]

    data = [
        gdf.loc[gdf["DIVISION"] == division, "As_numeric"].dropna()
        for division in divisions
    ]

    fig, ax = plt.subplots(figsize=(11, 7))

    box = ax.boxplot(
        data,
        patch_artist=True,
        tick_labels=divisions,
        showfliers=True,
        medianprops={
            "color": "black",
            "linewidth": 2
        },
        whiskerprops={
            "linewidth": 1.2
        },
        capprops={
            "linewidth": 1.2
        },
        flierprops={
            "marker": "o",
            "markersize": 3,
            "alpha": 0.4
        }
    )

    # Apply a different color to each division
    colors = plt.cm.viridis(
        [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    )

    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)

    # Logarithmic scale
    ax.set_yscale("log")

    ax.set_title(
        "Arsenic Concentration by Division",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel(
        "Division",
        fontsize=11
    )

    ax.set_ylabel(
        "Arsenic concentration",
        fontsize=11
    )

    ax.grid(
        axis="y",
        which="major",
        linestyle="--",
        alpha=0.3
    )

    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

def plot_top_districts(gdf, output_path):
    """Create a bar chart of the top 15 districts by median arsenic concentration."""

    district_summary = (
        gdf.groupby("DISTRICT")["As_numeric"]
        .agg(["count", "mean", "median", "max"])
        .sort_values("median", ascending=False)
    )

    top_districts = district_summary.head(15).sort_values("median")

    values = top_districts["median"].values
    labels = top_districts.index.tolist()

    norm = mpl.colors.Normalize(
        vmin=values.min(),
        vmax=values.max()
    )

    colors = plt.cm.viridis(norm(values))

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.barh(labels, values, color=colors)

    ax.set_title("Top 15 Districts by Median Arsenic Concentration")
    ax.set_xlabel("Median arsenic concentration")
    ax.set_ylabel("District")

    for i, value in enumerate(values):
        ax.text(
            value + 5,
            i,
            f"{value:.1f}",
            va="center"
        )

    sm = mpl.cm.ScalarMappable(
        norm=norm,
        cmap="viridis"
    )

    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label("Median arsenic concentration")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_district_arsenic(gdf, output_path, national, districts):
    """Create and save a district-level map of median arsenic concentration."""

    # Calculate median arsenic concentration using the spatially joined district
    district_summary = (
        gdf.groupby("district_final")["As_numeric"]
        .median()
        .reset_index()
    )

    district_summary.columns = [
        "DISTRICT",
        "median_arsenic"
    ]

    # Match spatial-join district names with boundary district names
    district_map = districts.merge(
        district_summary,
        left_on="adm2_en",
        right_on="DISTRICT",
        how="left"
    )

    # Create map
    fig, ax = plt.subplots(figsize=(10, 12))

    # Districts colored by median arsenic concentration
    district_map.plot(
        ax=ax,
        column="median_arsenic",
        cmap="Reds",
        norm=LogNorm(
            vmin=district_map["median_arsenic"].dropna().min(),
            vmax=district_map["median_arsenic"].dropna().max()
        ),
        legend=True,
        missing_kwds={
            "color": "lightgrey",
            "edgecolor": "black",
            "label": "No groundwater samples"
        },
        edgecolor="black",
        linewidth=0.5
    )

    # National boundary
    national.boundary.plot(
        ax=ax,
        color="black",
        linewidth=1.5
    )

    ax.set_title(
        "District-Level Median Arsenic Concentration",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def create_interactive_arsenic_map(gdf, output_path):
    """Create and save an interactive arsenic map."""

    m = gdf.explore(
    column="As_numeric",
    cmap="plasma",
    tooltip=[
        "SAMPLE_ID",
        "DISTRICT",
        "DIVISION",
        "As_numeric"
    ],
    legend=True,
    tiles="OpenStreetMap",
    marker_kwds={
        "radius": 3,
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.9
    }
)

    m.save(output_path)