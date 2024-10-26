import os

NSE_URL = os.getenv("NSE_URL", "https://archives.nseindia.com/content/indices/ind_nifty500list.csv")
CSV_FILE_DIR = os.getenv("CSV_FILE_DIR", "/opt/airflow/dags/datasets")
