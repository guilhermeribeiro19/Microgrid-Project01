import pandas as pd
from pathlib import Path

def load_dataset(path: str | Path) -> pd.DataFrame:

    df = pd.read_csv(path)
    return df
