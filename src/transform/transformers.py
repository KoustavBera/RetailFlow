"""
Transformation helper functions for retail transaction data.
"""

import pandas as pd


def clean_retail_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw retail transaction DataFrame.

    - Drop records with missing InvoiceNo or CustomerID.
    - Remove negative or zero Quantity and UnitPrice.
    - Ensure correct data types for InvoiceDate and CustomerID.
    """
    cleaned_df = df.copy()

    # Drop null critical fields
    cleaned_df = cleaned_df.dropna(subset=["InvoiceNo", "CustomerID"])

    # Filter out invalid quantities or prices
    cleaned_df = cleaned_df[(cleaned_df["Quantity"] > 0) & (cleaned_df["UnitPrice"] > 0)]

    # Type conversions
    cleaned_df["CustomerID"] = cleaned_df["CustomerID"].astype(int)
    cleaned_df["InvoiceDate"] = pd.to_datetime(cleaned_df["InvoiceDate"])

    # Add calculated TotalAmount
    cleaned_df["TotalAmount"] = cleaned_df["Quantity"] * cleaned_df["UnitPrice"]

    return cleaned_df
