# Placeholder for agent 1 dataset loading utilities

import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    if path.endswith('.csv'):
        return pd.read_csv(path)
    elif path.endswith('.parquet'):
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported data format: {path}")
