"""
Data Quality checks module for RetailFlow data pipeline.
"""

import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_schema(df: pd.DataFrame, required_columns: list) -> bool:
    """
    Verify that all required columns are present in DataFrame.
    """
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        logger.error(f"Data quality error: Missing columns: {missing_cols}")
        return False
    return True


def check_no_nulls(df: pd.DataFrame, columns: list) -> bool:
    """
    Verify specified columns contain no null values.
    """
    null_counts = df[columns].isnull().sum()
    has_nulls = null_counts[null_counts > 0]
    if not has_nulls.empty:
        logger.error(f"Data quality error: Null values found in columns: {has_nulls.to_dict()}")
        return False
    return True


def run_all_checks(df: pd.DataFrame) -> bool:
    """
    Run full suite of data quality checks.
    """
    required_cols = ["InvoiceNo", "StockCode", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID"]
    
    if not validate_schema(df, required_cols):
        return False
        
    if not check_no_nulls(df, ["InvoiceNo", "CustomerID"]):
        return False
        
    logger.info("All data quality checks passed.")
    return True
