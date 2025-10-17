import pytest
import pandas as pd
from pathlib import Path
from microgrid_eda.io import load_dataset

def test_load_dataset_with_string_path():
    """Test loading dataset using a string path."""
    df = load_dataset("data/raw/microgrid.csv")
    assert isinstance(df, pd.DataFrame), "Should return a pandas DataFrame"
    assert len(df) > 0, "DataFrame should not be empty"

def test_load_dataset_with_path_object():
    """Test loading dataset using a Path object."""
    path = Path("data/raw/microgrid.csv")
    df = load_dataset(path)
    assert isinstance(df, pd.DataFrame), "Should return a pandas DataFrame"
    assert len(df) > 0, "DataFrame should not be empty"

def test_dataset_structure():
    """Test if loaded dataset has the expected structure."""
    df = load_dataset("data/raw/microgrid.csv")

    # Check expected columns exist
    expected_columns = {'index', 'Consumption', 'Solar', 'Wind'}
    assert set(df.columns) == expected_columns, "DataFrame should have expected columns"

    # Check data types
    assert pd.api.types.is_float_dtype(df['Consumption']), "Consumption should be float"
    assert pd.api.types.is_float_dtype(df['Solar']), "Solar should be float"
    assert pd.api.types.is_float_dtype(df['Wind']), "Wind should be float"
