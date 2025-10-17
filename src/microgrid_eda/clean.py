import pandas as pd

def standardize(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.lower().strip() for c in df.columns]
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").set_index("timestamp")

    # Resample hourly mean (if data is sub-hourly)
    # Use lowercase 'h' to avoid pandas FutureWarning
    df = df.resample("1h").mean()

    # Drop missing values
    df = df.dropna()
    return df
