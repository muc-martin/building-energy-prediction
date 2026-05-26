# Building PV Power Prediction (Black-box ML)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/muc-martin/building-energy-prediction/blob/main/pv_ml_intro.ipynb)

This repo provides a Colab-ready jupyter notebook to explore a simple black-box ML model (Linear Regression) that predicts PV power from weather data. It includes:
- `pv_ml_intro.ipynb` — the guided notebook (top level)
- `data/*.csv` — ready-to-use CSVs with the full history for four selected sites
- `tools/import_dataset.py` — simple script to regenerate the site-level CSVs from the raw dataset

## Quick start (Colab)
1. Click the badge above to open the notebook in Colab.
2. Run all cells.

## Local setup
To run the notebook or helper scripts on your machine install the Python dependencies with:
```bash
python -m pip install -r requirements.txt
```
You can optionally add `jupyterlab` if you want to edit the notebook outside of Colab.

## Data source
- Dryad dataset: Lin et al. (2024). "A high-resolution three-year dataset supporting rooftop photovoltaics (PV) generation analytics." DOI: `10.5061/dryad.m37pvmd99` (dataset page: https://datadryad.org/dataset/doi%3A10.5061/dryad.m37pvmd99).
- Peer-reviewed article: Lin, Z., Zhou, Q., Wang, Z., et al. (2025). "A high-resolution three-year dataset supporting rooftop photovoltaics (PV) generation analytics." Scientific Data 12, 63. DOI: `10.1038/s41597-025-04397-y` (article: https://www.nature.com/articles/s41597-025-04397-y).

## Re-generate datasets (optional)
To regenerate the CSVs locally, first download and extract the original dataset into this repository folder so that the `Dataset/` tree is available. Then run:
```bash
python tools/import_dataset.py
```
It writes four site-level CSVs under `data/` (`SQ8.csv`, `SQ10.csv`, `SQ19.csv`, `Tower A.csv`) using the full available time range and hourly resampling. Columns include:
- `time` (timestamp)
- `power` (measured PV power)
- Weather features: `irradiance`, `temp`, `rh`, `slp`, `vis`, `wind_speed`, `wind_direction`
