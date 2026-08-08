"""
Unit tests for transformation logic in transformers.py.
"""

import pandas as pd
from src.transform.transformers import clean_retail_transactions


def test_clean_retail_transactions():
    raw_data = {
        "InvoiceNo": ["536365", "536366", None, "536367"],
        "StockCode": ["85123A", "71053", "84406B", "84029G"],
        "Quantity": [6, -1, 2, 8],
        "InvoiceDate": ["2026-08-01 08:26:00", "2026-08-01 08:28:00", "2026-08-01 08:30:00", "2026-08-01 08:34:00"],
        "UnitPrice": [2.55, 3.39, 2.75, 0.00],
        "CustomerID": [17850, 17850, 13047, 13047],
    }
    df = pd.DataFrame(raw_data)
    cleaned = clean_retail_transactions(df)

    # Valid record should be only the first row (InvoiceNo 536365)
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["InvoiceNo"] == "536365"
    assert cleaned.iloc[0]["TotalAmount"] == 15.3  # 6 * 2.55
