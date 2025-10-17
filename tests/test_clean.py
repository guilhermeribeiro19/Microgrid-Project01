import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from microgrid_eda.clean import standardize

@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    data = {
        'TimeStamp': [
            '2023-01-01 12:00:00',
            '2023-01-01 12:30:00',  # Test sub-hourly data
            '2023-01-01 13:00:00',
            '2023-01-01 13:30:00'
        ],
        'Consumption ': [10.5, 11.0, 12.5, 13.0],  # Note the space in column name
        'SOLAR': [5.0, 5.5, 6.0, np.nan]  # Include some missing data
    }
    return pd.DataFrame(data)

def test_standardize_column_names(sample_df):
    """Test if column names are properly standardized to lowercase."""
    cleaned = standardize(sample_df)
    expected_columns = {'consumption', 'solar'}
    assert set(cleaned.columns) == expected_columns, "Column names should be lowercase and stripped"

def test_timestamp_conversion(sample_df):
    """Test if timestamp is properly converted and set as index."""
    cleaned = standardize(sample_df)
    assert isinstance(cleaned.index, pd.DatetimeIndex), "Index should be DatetimeIndex"
    assert cleaned.index.name == 'timestamp', "Index name should be 'timestamp'"

def test_hourly_resampling(sample_df):
    """Test if data is properly resampled to hourly frequency."""
    cleaned = standardize(sample_df)
    # Check if we have hourly frequency (use lowercase 'h')
    assert cleaned.index.freq == pd.Timedelta('1h'), "Data should be resampled to hourly frequency"
    # Check if values are averaged correctly
    expected_consumption = pd.Series([(10.5 + 11.0)/2, (12.5 + 13.0)/2], name='consumption')
    # Use equality check tolerant to index alignment
    assert cleaned['consumption'].reset_index(drop=True).equals(expected_consumption), "Hourly values should be averaged correctly"

def test_missing_values_handling(sample_df):
    """Test if missing values are properly handled."""
    cleaned = standardize(sample_df)
    assert cleaned.isna().sum().sum() == 0, "There should be no missing values in cleaned data"
    assert len(cleaned) == 2, "After resampling to hourly and dropping NA, should have 2 complete hours"

def test_sorting(sample_df):
    """Test if data is properly sorted by timestamp."""
    # Add an out-of-order row to the sample data
    sample_df.loc[len(sample_df)] = ['2023-01-01 11:00:00', 9.0, 4.0]
    cleaned = standardize(sample_df)
    assert cleaned.index.is_monotonic_increasing, "Index should be sorted in ascending order"
