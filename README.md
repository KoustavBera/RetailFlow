# RetailFlow

RetailFlow is an end-to-end data pipeline that ingests raw retail transaction data, lands it in object storage, cleans and transforms it, runs data quality checks, and loads the result into a PostgreSQL data warehouse — orchestrated end-to-end with Apache Airflow.

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | [Apache Airflow](https://airflow.apache.org/) 2.8 (DAG-based scheduling, `PythonOperator` tasks) |
| Ingestion | [Boto3](https://boto3.amazonaws.com/) — lands raw CSVs into S3 under a date-partitioned key prefix |
| Transformation | [Pandas](https://pandas.pydata.org/) 2.2 (cleaning, type coercion, derived columns); [PySpark](https://spark.apache.org/) 3.5 available for batch processing at scale |
| Data Quality | Custom validation checks (`src/quality/checks.py`); [Great Expectations](https://greatexpectations.io/) 0.18 |
| Data Warehouse | [PostgreSQL](https://www.postgresql.org/) 15 (star-schema: `dim_customers`, `dim_products`, `fact_sales`), loaded via [SQLAlchemy](https://www.sqlalchemy.org/) + `psycopg2` |
| Infrastructure | [Docker Compose](https://docs.docker.com/compose/) (Postgres service, schema auto-init) |
| Testing | [pytest](https://pytest.org/) + `pytest-cov` |
| Config | [python-dotenv](https://pypi.org/project/python-dotenv/) for environment variable management |
| Language | Python 3.9+ |

## Project Structure

```
RetailFlow/
├── data/
│   └── raw/                  # Raw dataset storage
├── src/
│   ├── ingestion/
│   │   └── land_to_s3.py     # Ingest raw data to object storage (S3)
│   ├── transform/
│   │   ├── transformers.py   # Core transformation logic & data cleaning functions
│   │   └── clean_job.py      # Pandas batch transformation job
│   ├── warehouse/
│   │   ├── schema.sql        # PostgreSQL schema definitions
│   │   └── load.py           # Data warehouse loading scripts
│   └── quality/
│       └── checks.py         # Data quality validation & checks
├── dags/
│   └── retailflow_dag.py     # Airflow DAG orchestration
├── tests/
│   └── test_transformers.py  # Unit tests for transformation logic
├── docker-compose.yaml       # Docker environment (Postgres)
└── requirements.txt          # Python dependencies
```

## Pipeline Flow

`ingest_to_s3` → `clean_and_transform` → `run_quality_checks` → `load_to_warehouse`

1. **Ingest** — raw CSV is uploaded to S3 under `transactions/dt=<date>/`.
2. **Transform** — nulls in critical fields are dropped, invalid quantities/prices filtered out, types coerced, and a `TotalAmount` column derived.
3. **Quality** — required columns and non-null constraints are validated before loading.
4. **Load** — cleaned data is appended into the `fact_sales` table in PostgreSQL.

## Getting Started

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- AWS credentials configured (for S3 ingestion).

### Installation
1. Clone the repository and navigate to the root directory.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Spin up local services with Docker Compose:
   ```bash
   docker-compose up -d
   ```

### Running Tests
Run unit tests using pytest:
```bash
pytest tests/
```
