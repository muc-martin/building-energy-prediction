from __future__ import annotations

import glob
import os
from pathlib import Path
from typing import Iterable

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]


def _normalize_col(name: str) -> str:
    # Lowercase, drop unit suffix in parentheses, trim and underscore
    base = name.split("(")[0]
    return base.strip().lower().replace(" ", "_")


def build_meteorology() -> pd.DataFrame:
    """Load and merge all meteorological CSVs as in import.ipynb.

    Folders scanned (under the Dryad dataset tree):
    - Irradiance, Rainfall, Relative Humidity, Sea Level Pressure, Temperature, Visibility, Wind

    Returns a wide hourly DataFrame indexed by time with normalized column names.
    Drops the rainfall column to match the original notebook logic.
    """
    base_path = BASE_DIR / "Dataset" / "Dataset" / "Time series dataset" / "Meteorological dataset"
    met_folders = [
        "Irradiance",
        "Rainfall",
        "Relative Humidity",
        "Sea Level Pressure",
        "Temperature",
        "Visibility",
        "Wind",
    ]

    frames: list[pd.DataFrame] = []
    for item in met_folders:
        folder_path = base_path / item
        csvs = glob.glob(os.path.join(str(folder_path), "*.csv"))
        if not csvs:
            continue
        loc_frames: list[pd.DataFrame] = []
        for csv in csvs:
            df = pd.read_csv(csv, parse_dates=True, index_col="Time")
            # Hourly resample like the notebook
            df = df.resample("h").first()
            # Normalize column names
            df.columns = [_normalize_col(c) for c in df.columns]
            loc_frames.append(df)
        # Stack all years for this variable vertically
        frames.append(pd.concat(loc_frames))

    if not frames:
        raise FileNotFoundError(
            f"No meteorology CSVs found under: {base_path} — ensure the Dryad dataset is extracted."
        )

    met = pd.concat(frames, axis=1)
    # Notebook logic dropped rainfall entirely
    met = met.drop(columns=["rainfall"], errors="ignore")
    # Tidy index
    met = met.sort_index()
    return met


def process_sites(met: pd.DataFrame, selected_locs: Iterable[str]) -> None:
    """Build per-site CSVs joined with meteorology, following the notebook logic.

    - Reads only the power column from each site file
    - Hourly mean for power
    - Inner-join with meteorology and drop missing rows
    - Writes to data/<site>.csv
    """
    pv_base = (
        BASE_DIR
        / "Dataset"
        / "Dataset"
        / "Time series dataset"
        / "PV generation dataset"
        / "PV stations without panel level optimizer"
        / "Site level dataset"
    )
    csvs = glob.glob(os.path.join(str(pv_base), "*.csv"))

    out_dir = BASE_DIR / "data"
    out_dir.mkdir(parents=True, exist_ok=True)

    selected = set(selected_locs)
    for csv in csvs:
        name = Path(csv).stem
        if name not in selected:
            print(f"{name} not in selected_locs")
            continue

        df = pd.read_csv(csv, usecols=["Time", "power(W)"], parse_dates=True, index_col="Time")
        # Use 'power_w' to retain units in the column name
        df.columns = ["power"]
        df = df.resample("h").mean()

        joined = df.join(met, how="inner")
        joined = joined.dropna()

        # Write with an explicit 'time' column
        joined.index.name = "time"
        out_path = out_dir / f"{name}.csv"
        joined.reset_index().to_csv(out_path, index=False)
        print(f"Wrote: {out_path.relative_to(BASE_DIR)}")


def main() -> None:
    met = build_meteorology()
    # Same default subset as in the notebook
    selected_locs = ["SQ8", "SQ10", "SQ19", "Tower A"]
    process_sites(met, selected_locs)


if __name__ == "__main__":
    main()
