# src/ingestion/land_to_s3.py
import boto3
import os

def land_raw_file(local_path: str, bucket: str, date_str: str):
    """Upload a raw data file to S3 under a date-partitioned prefix."""
    s3 = boto3.client("s3")
    
    # Create the date-partitioned key structure
    key = f"transactions/dt={date_str}/{os.path.basename(local_path)}"
    
    s3.upload_file(Filename=local_path, Bucket=bucket, Key=key)
    print(f"✅ Landed {local_path} -> s3://{bucket}/{key}")

if __name__ == "__main__":
    # IMPORTANT: Replace with YOUR actual bucket name
    land_raw_file(
        "data/raw/online_retail_II.csv", 
        "retailflow-raw-kb082026",  # ← CHANGE THIS to your bucket name!
        "2026-08-08"
    )