# Expected Threat – xT Grid Pitch

This project visualizes an Expected Threat (xT) grid on a football pitch using mplsoccer.
The notebook `xT-pitch.ipynb` loads a precomputed xT grid from a CSV file and generates a heatmap with annotated values.

## Project Structure
The project is organized as follows:

```text
projects/
└── expected-threat/
    ├── data/
    │   └── xT_Grid.csv
    ├── notebooks/
    │   └── xT-pitch.ipynb
    └── figures/
        └── xT-pitch_xt-grid.png  (generated when the notebook is executed)



## 
```bash
git clone https://github.com/n0rthface43/Ball.git
cd Ball/projects/expected-threat

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
