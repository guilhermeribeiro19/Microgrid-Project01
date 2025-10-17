
from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

logger = logging.getLogger(__name__)

# expected measurement columns (timestamp handled separately)
EXPECTED_MEASUREMENT_COLUMNS = ("Consumption", "Solar", "Wind")


def _ensure_path(pathlike: Path | str) -> Path:
    p = Path(pathlike)
    return p.expanduser().resolve()


def validate_schema(
    df: pd.DataFrame,
    required_measurements: Iterable[str] = EXPECTED_MEASUREMENT_COLUMNS,
    timestamp_col: str = "index",
) -> None:
    """Validate that the DataFrame has required measurement columns and a timestamp.

    Raises:
        ValueError: if required columns or timestamp are missing.
    """
    missing = set(required_measurements) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required measurement columns: {sorted(missing)}")

    if timestamp_col not in df.columns and not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError(
            f"Timestamp column '{timestamp_col}' not found and index is not DatetimeIndex."
        )


def load_raw_data(
    filepath: Path | str,
    timestamp_col: str = "index",
    required_measurements: Optional[Iterable[str]] = None,
    parse_dates: bool = True,
    usecols: Optional[Iterable[str]] = None,
    dtype: Optional[dict] = None,
    low_memory: bool = False,
) -> pd.DataFrame:
    """Load raw microgrid CSV data into a DataFrame and validate schema.

    Args:
        filepath: path to CSV file
        timestamp_col: name of column containing timestamp (will be parsed + set as index)
        required_measurements: iterable of required measurement column names
        parse_dates: whether to parse the timestamp column as datetime
        usecols: optional list of columns to read
        dtype: optional dtype mapping for read_csv
        low_memory: passed to pandas.read_csv

    Returns:
        pd.DataFrame with timestamp set as DatetimeIndex when possible

    Raises:
        FileNotFoundError: if file does not exist
        ValueError: if required columns are missing or timestamp can't be parsed
    """
    p = _ensure_path(filepath)
    if not p.exists():
        raise FileNotFoundError(f"Data file not found: {p}")

    if required_measurements is None:
        required_measurements = EXPECTED_MEASUREMENT_COLUMNS

    read_kwargs = {"low_memory": low_memory}
    if usecols is not None:
        read_kwargs["usecols"] = list(usecols)
    if dtype is not None:
        read_kwargs["dtype"] = dtype

    logger.info("Loading data from %s", p)
    try:
        df = pd.read_csv(p, **read_kwargs)
    except Exception as exc:
        logger.exception("Failed to read CSV %s", p)
        raise

    # If timestamp column exists, parse and set as index
    if timestamp_col in df.columns:
        if parse_dates:
            df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors="coerce")
        df = df.set_index(timestamp_col)
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError(f"Parsed timestamp column '{timestamp_col}' is not datetime-like")
    else:
        if not isinstance(df.index, pd.DatetimeIndex):
            logger.warning(
                "No timestamp column '%s' found and index is not DatetimeIndex; downstream code may fail",
                timestamp_col,
            )

    validate_schema(df, required_measurements=required_measurements, timestamp_col=timestamp_col)

    logger.info("Loaded %d rows; columns: %s", len(df), list(df.columns))
    return df


def save_processed_data(
    df: pd.DataFrame,
    output_path: Path | str,
    fmt: str = "csv",
    index: bool = True,
    fail_on_missing: bool = False,
) -> None:
    """Save processed DataFrame to disk (csv or parquet).

    Args:
        df: DataFrame to save
        output_path: destination path
        fmt: 'csv' or 'parquet'
        index: whether to write index
        fail_on_missing: if True, raise when df has missing values
    """
    out = _ensure_path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    if fail_on_missing and df.isna().any().any():
        raise ValueError("DataFrame contains missing values; set fail_on_missing=False to allow saving")

    logger.info("Saving processed data to %s (format=%s)", out, fmt)
    try:
        if fmt.lower() == "csv":
            df.to_csv(out, index=index)
        elif fmt.lower() in ("parquet", "pq"):
            df.to_parquet(out, index=index)
        else:
            raise ValueError("Unsupported format: %r" % fmt)
    except Exception:
        logger.exception("Failed to save processed data to %s", out)
        raise

    logger.info("Saved %d rows to %s", len(df), out)
