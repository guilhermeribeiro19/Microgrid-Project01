
import pandas as pd
from pathlib import Path

from microgrid_eda.io import load_raw_data, save_processed_data


def test_load_and_save(tmp_path: Path):
	csv = tmp_path / "microgrid.csv"
	csv.write_text("index,Consumption,Solar,Wind\n2020-01-01T00:00:00,10.0,0.0,5.0\n")

	df = load_raw_data(csv, timestamp_col="index")
	assert isinstance(df.index, pd.DatetimeIndex)
	assert list(df.columns) == ["Consumption", "Solar", "Wind"]

	out_csv = tmp_path / "out.csv"
	save_processed_data(df, out_csv, fmt="csv")
	assert out_csv.exists()
