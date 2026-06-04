import pandas as pd

def get_stats(df: pd.DataFrame):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "column_names": list(df.columns)
    }