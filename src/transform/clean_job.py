"""
Batch ETL transformation script.
"""

import os
import logging
import pandas as pd
from src.transform.transformers import clean_retail_transactions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_clean_job(input_path: str, output_path: str):
    """
    Reads raw data from input_path, transforms it, and writes cleaned data to output_path.
    """
    logger.info(f"Loading raw data from {input_path}...")
    if not os.path.exists(input_path):
        logger.warning(f"File {input_path} not found. Skipping clean job.")
        return

    raw_df = pd.read_csv(input_path)
    cleaned_df = clean_retail_transactions(raw_df)
    
    logger.info(f"Saving cleaned dataset ({len(cleaned_df)} rows) to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cleaned_df.to_csv(output_path, index=False)
    logger.info("Cleaning job completed successfully.")


if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    raw_csv = os.path.join(base_dir, "data/raw/online_retail.csv")
    cleaned_csv = os.path.join(base_dir, "data/processed/cleaned_online_retail.csv")
    run_clean_job(raw_csv, cleaned_csv)
