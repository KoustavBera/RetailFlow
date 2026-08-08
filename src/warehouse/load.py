"""
Data loader module to push cleaned datasets to the data warehouse.
"""

import os
import logging
import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_engine():
    """
    Construct database engine connection from environment variables.
    """
    db_user = os.getenv("POSTGRES_USER", "retailflow_user")
    db_password = os.getenv("POSTGRES_PASSWORD", "retailflow_password")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "retailflow_db")

    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(db_url)


def load_cleaned_data_to_warehouse(df: pd.DataFrame, table_name: str = "fact_sales"):
    """
    Load DataFrame into PostgreSQL table.
    """
    engine = get_db_engine()
    logger.info(f"Loading {len(df)} records into table '{table_name}'...")
    df.to_sql(table_name, engine, if_exists="append", index=False)
    logger.info("Data load complete.")


if __name__ == "__main__":
    logger.info("Data loader script initialized.")
