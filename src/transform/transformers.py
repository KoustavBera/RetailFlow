# src/transform/transformers.py
from abc import ABC, abstractmethod
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_timestamp, trim, upper, round as spark_round


# WHY ABC: This is a contract. It forces every new transformer we write 
# to have a 'transform' method. If we forget it, Python throws an error 
# immediately instead of failing mid-pipeline.
class Transformer(ABC):
    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        ...


class TypeCastTransformer(Transformer):
    """Cast raw string columns to proper types."""
    def transform(self, df: DataFrame) -> DataFrame:
        return (
            # WHY: CSVs read everything as text. We must cast to real types 
            # so downstream math and filters work correctly.
            df.withColumn("InvoiceDate", to_timestamp(col("InvoiceDate"), "M/d/yyyy H:mm"))
            .withColumn("Quantity", col("Quantity").cast("int"))
            .withColumn("Price", spark_round(col("Price").cast("double"), 2))
        )


class StandardizeTransformer(Transformer):
    """Normalize text fields for consistent grouping/joining later."""
    def transform(self, df: DataFrame) -> DataFrame:
        return (
            # WHY: "France", "france ", and " FRANCE" are 3 different countries 
            # to a computer. This forces them to be identical.
            df.withColumn("Country", upper(trim(col("Country"))))
            .withColumn("Description", trim(col("Description")))
        )


class ValidRowsTransformer(Transformer):
    """Drop rows that don't represent a genuine completed sale."""
    def transform(self, df: DataFrame) -> DataFrame:
        return (
            # WHY: These map directly to your Step 2 profiling findings!
            df.filter(col("Quantity") > 0)           # Removes the 22,950 returns
            .filter(col("Price") > 0)                # Removes the 5 data-entry errors
            .filter(col("Customer ID").isNotNull())  # Removes the 243,007 guest checkouts
            .filter(~col("Invoice").startswith("C")) # Removes cancelled invoices
        )


class DeduplicateTransformer(Transformer):
    def transform(self, df: DataFrame) -> DataFrame:
        # WHY: We use the business key (Invoice + StockCode + Customer) to 
        # define a duplicate, rather than checking every single column.
        return df.dropDuplicates(["Invoice", "StockCode", "Customer ID"])


class CleaningPipeline:
    """Runs a list of Transformers in sequence -- the Strategy pattern."""
    def __init__(self, steps: list[Transformer]):
        self.steps = steps

    def run(self, df: DataFrame) -> DataFrame:
        for step in self.steps:
            df = step.transform(df)
        return df