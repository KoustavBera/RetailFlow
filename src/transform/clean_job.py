# src/transform/clean_job.py
import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession

# WHY: Import the 4 workers + the pipeline manager we built in transformers.py
# NOTE: we use "src.transform.transformers" to match your project structure
from src.transform.transformers import (
    CleaningPipeline, TypeCastTransformer, StandardizeTransformer,
    ValidRowsTransformer, DeduplicateTransformer,
)


def main():
    # ---- 1. Load AWS secrets from your .env file ----
    load_dotenv()
    aws_access_key = os.getenv("S3_ACCESS_KEY")
    aws_secret_key = os.getenv("SECRET_ACCESS_KEY")

    # WHY: Fail FAST with a clear message if secrets are missing,
    # instead of crashing deep inside Spark with a confusing error.
    if not aws_access_key or not aws_secret_key:
        raise ValueError("❌ AWS credentials not found. Check your .env file!")

    # ---- 2. Fire up the Spark engine ----
    spark = (
        SparkSession.builder
        .appName("RetailFlowClean")
        # WHY: local[*] = use ALL CPU cores on your laptop for speed.
        .master("local[*]")
        # WHY: Hand Spark the Hadoop "travel adapters" so it can talk to S3.
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4")
        # WHY: Spark needs YOUR AWS keys to read/write your private buckets.
        .config("spark.hadoop.fs.s3a.access.key", aws_access_key)
        .config("spark.hadoop.fs.s3a.secret.key", aws_secret_key)
        # WHY: Snappy = the industry-standard Parquet compression (fast + small).
        .config("spark.sql.parquet.compression.codec", "snappy")
        .getOrCreate()
    )

    # TODO: 🔧 UPDATE these to YOUR actual bucket names!
    raw_bucket = "retailflow-raw-kb082026"
    processed_bucket = "retailflow-processed-kb082026"

    # ---- 3. Go get the raw materials from S3 ----
    print("📥 Reading raw data from S3...")
    raw_df = (
        spark.read
        .option("header", True)              # first row = column names
        .option("encoding", "ISO-8859-1")    # this dataset is Latin-1, not UTF-8
        .csv(f"s3a://{raw_bucket}/transactions/dt=2026-08-08/")
    )

    # ---- 4. Run it through the assembly line ----
    pipeline = CleaningPipeline([
        TypeCastTransformer(),
        StandardizeTransformer(),
        ValidRowsTransformer(),
        DeduplicateTransformer(),
    ])

    print("⚙️  Running transformation pipeline...")
    clean_df = pipeline.run(raw_df)

    # ---- 5. Ship the finished product ----
    # WHY cache + count FIRST: Spark is lazy (see explanation below).
    # Counting now computes the pipeline ONCE and holds the result in memory,
    # so the write below reuses it instead of recomputing everything.
    clean_df.cache()
    row_count = clean_df.count()

    print("📤 Writing clean Parquet to S3...")
    clean_df.write.mode("overwrite").parquet(
        f"s3a://{processed_bucket}/transactions/dt=2026-08-08/"
    )

    print(f"🎉 SUCCESS! Cleaned rows written: {row_count}")
    spark.stop()


if __name__ == "__main__":
    main()