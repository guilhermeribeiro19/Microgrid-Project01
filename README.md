# Microgrid-Project01

**Energy Data Exploration & Visualization**

Microgrid-Project01 is an open-source Python project that focuses on **load and renewable generation analysis**, offering interactive dashboards, reproducible pipelines, and automated reports.

---

## Project Overview

The project analyzes microgrid datasets — typically time-series measurements of load (consumption) and generation (solar PV, wind, etc.) — to uncover energy patterns and insights such as:

- Daily and weekly load vs. generation profiles
- Peak and off-peak behavior
- Renewable utilization and self-consumption rates
- Excess renewable vs. grid import periods
- Key summary statistics and visual narratives

Version 1 (v1) focuses purely on **dataset-only analysis** without weather or pricing data.
Future versions (v2+) will progressively add forecasting, optimization, and blockchain-based energy trading simulations.

---

## Technical Stack

| Component | Technology |
# Microgrid-Project01

**Energy Data Exploration & Visualization**

Microgrid-Project01 is an open-source Python project that focuses on **load and renewable generation analysis**, offering interactive dashboards, reproducible pipelines, and automated reports.

---

## Project Overview

The project analyzes microgrid datasets — typically time-series measurements of load (consumption) and generation (solar PV, wind, etc.) — to uncover energy patterns and insights such as:

- Daily and weekly load vs. generation profiles
- Peak and off-peak behavior
- Renewable utilization and self-consumption rates
- Excess renewable vs. grid import periods
- Key summary statistics and visual narratives

Version 1 (v1) focuses purely on **dataset-only analysis** without weather or pricing data.
Future versions (v2+) will progressively add forecasting, optimization, and blockchain-based energy trading simulations.

---

## Technical Stack

| Component | Technology |
|------------|-------------|
| **Language** | Python 3.12 |
| **Data Handling** | pandas, numpy, pyarrow |
| **Visualization** | plotly (interactive), matplotlib |
| **Testing & Quality** | pytest, ruff, pre-commit |
| **Environment** | GitHub Codespaces |
| **Project Management** | GitHub Projects / Issues |

---
## Data

Step 2: Load sample dataset

Download or place the Kaggle dataset "Microgrid load and generation" CSV into:
`data/raw/microgrid.csv`

## Quickstart

```bash
# Clone repository
git clone https://github.com/<your_username>/Microgrid-Project01.git
cd Microgrid-Project01

# Run pre-commit (optional)
pre-commit install

# Install dependencies
pip install -e .

# Run pipeline
python -m src.cli run --input data/raw/microgrid.csv

```

---

## Outputs

- Interactive charts
- Static figures
- Auto-generated Markdown report

---

## Backlog Ideas

- Weather correlation dashboard
- Time-of-use tariff simulation
- Predictive maintenance anomaly detection
- CO₂ footprint estimation

## Contributions

Contributions are welcome!
You can open issues, suggest features, or create pull requests.
