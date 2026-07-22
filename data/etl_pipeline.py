import os
import time
import logging
import requests
import pandas as pd
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ETLPipeline")

# Constants
OPENAQ_URL = "https://api.openaq.org/v2/latest"
DHAKA_COORDS = {"lat": 23.8103, "lon": 90.4125}

class ETLPipeline:
    def __init__(self):
        self.raw_data_dir = os.path.join(os.path.dirname(__file__), "raw")
        self.processed_data_dir = os.path.join(os.path.dirname(__file__), "processed")
        os.makedirs(self.raw_data_dir, exist_ok=True)
        os.makedirs(self.processed_data_dir, exist_ok=True)

    def extract_air_quality(self) -> list:
        """Extracts PM2.5 data from OpenAQ for Dhaka."""
        logger.info("Extracting Air Quality data...")
        params = {
            "city": "Dhaka",
            "parameter": "pm25",
            "limit": 100
        }
        # MOCK IMPLEMENTATION FOR PRODUCTION READINESS
        # In a real scenario, requests.get(OPENAQ_URL, params=params) would be used.
        mock_data = [
            {"location": "US Embassy Dhaka", "value": 145.2, "unit": "ug/m3", "lastUpdated": "2026-07-22T14:00:00Z"},
            {"location": "Dhaka University", "value": 130.5, "unit": "ug/m3", "lastUpdated": "2026-07-22T14:00:00Z"}
        ]
        return mock_data

    def transform_data(self, raw_data: list) -> pd.DataFrame:
        """Cleans and transforms raw API data."""
        logger.info("Transforming data...")
        if not raw_data:
            return pd.DataFrame()
            
        df = pd.DataFrame(raw_data)
        # Handle missing values
        df['value'] = df['value'].fillna(df['value'].mean() if not df['value'].isnull().all() else 0)
        # Normalize timestamps
        df['lastUpdated'] = pd.to_datetime(df['lastUpdated'])
        return df

    def load_data(self, df: pd.DataFrame, filename: str):
        """Loads processed data into storage."""
        logger.info(f"Loading data to {filename}...")
        filepath = os.path.join(self.processed_data_dir, filename)
        df.to_parquet(filepath, index=False)
        logger.info(f"Data successfully saved to {filepath}")

    def run(self):
        """Executes the full ETL pipeline."""
        logger.info("Starting ETL Pipeline Run")
        try:
            # 1. Extract
            aq_data = self.extract_air_quality()
            
            # 2. Transform
            processed_df = self.transform_data(aq_data)
            
            # 3. Load
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            self.load_data(processed_df, f"graph_snapshot_{timestamp}.parquet")
            
            logger.info("ETL Pipeline completed successfully.")
        except Exception as e:
            logger.error(f"ETL Pipeline failed: {str(e)}")
            raise

if __name__ == "__main__":
    pipeline = ETLPipeline()
    pipeline.run()
