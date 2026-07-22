import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class FeatureEngineer:
    def __init__(self):
        self.pm25_scaler = StandardScaler()
        self.meteo_scaler = MinMaxScaler()
        self.is_fitted = False

    def add_cyclical_features(self, df: pd.DataFrame, col_name: str, max_val: float) -> pd.DataFrame:
        """
        Applies sine and cosine transformations to cyclical temporal features.
        """
        df[f"{col_name}_sin"] = np.sin(2 * np.pi * df[col_name] / max_val)
        df[f"{col_name}_cos"] = np.cos(2 * np.pi * df[col_name] / max_val)
        return df

    def fit_transform_node_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fits scalers on the training data and transforms node features.
        Expected columns: ['timestamp', 'pm25', 'temperature', 'humidity']
        """
        df = df.copy()
        
        # 1. Temporal Cyclical Encoding
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['dayofweek'] = df['timestamp'].dt.dayofweek
            
            df = self.add_cyclical_features(df, 'hour', 24.0)
            df = self.add_cyclical_features(df, 'dayofweek', 7.0)
            df.drop(columns=['hour', 'dayofweek'], inplace=True)
            
        # 2. Scaling PM2.5
        if 'pm25' in df.columns:
            df['pm25_scaled'] = self.pm25_scaler.fit_transform(df[['pm25']])
            
        # 3. Scaling Meteorological data
        meteo_cols = [col for col in ['temperature', 'humidity'] if col in df.columns]
        if meteo_cols:
            df[meteo_cols] = self.meteo_scaler.fit_transform(df[meteo_cols])
            
        self.is_fitted = True
        return df

    def transform_node_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms new node features using already fitted scalers.
        """
        if not self.is_fitted:
            raise ValueError("Scalers have not been fitted. Call fit_transform_node_features first.")
            
        df = df.copy()
        
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['dayofweek'] = df['timestamp'].dt.dayofweek
            
            df = self.add_cyclical_features(df, 'hour', 24.0)
            df = self.add_cyclical_features(df, 'dayofweek', 7.0)
            df.drop(columns=['hour', 'dayofweek'], inplace=True)
            
        if 'pm25' in df.columns:
            df['pm25_scaled'] = self.pm25_scaler.transform(df[['pm25']])
            
        meteo_cols = [col for col in ['temperature', 'humidity'] if col in df.columns]
        if meteo_cols:
            df[meteo_cols] = self.meteo_scaler.transform(df[meteo_cols])
            
        return df

    def process_edge_features(self, edges_df: pd.DataFrame) -> pd.DataFrame:
        """
        Processes edge features like traffic bottleneck weights.
        Expected columns: ['traffic_speed']
        """
        df = edges_df.copy()
        if 'traffic_speed' in df.columns:
            # Prevent division by zero
            safe_speed = df['traffic_speed'].replace(0, 0.1)
            df['bottleneck_weight'] = 1.0 / safe_speed
        return df
