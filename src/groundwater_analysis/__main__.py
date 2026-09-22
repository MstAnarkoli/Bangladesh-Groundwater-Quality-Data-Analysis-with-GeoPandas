import logging

from .logging_config import setup_logging
from .pipeline import run_pipeline


def main():
    """Run the groundwater analysis pipeline."""

    setup_logging()

    logger = logging.getLogger(__name__)

    gdf = run_pipeline()

    logger.info(
        "Pipeline completed successfully: %s records",
        gdf.shape[0]
    )
    logger.info("CRS: %s", gdf.crs)


if __name__ == "__main__":
    main()