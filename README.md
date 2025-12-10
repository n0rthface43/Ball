# Ball - Football Analytics Blog and Code Repository

Welcome to the **Ball** repository! This GitHub repository is designed to share my work in football analytics, including articles, Jupyter Notebooks with custom metrics, and visualizations.

##  Contents

- ## Projects and Analysis  
| Project | Date | Links |
|----------|------|--------| 
|**Clustering Center Midfielders with Machine Learning** | 22-11-2025 | [📝 Article](https://medium.com/@henrik.schjoth/clustering-and-ranking-central-midfielders-b4ddea2e83e7) <br> [📄 Code](./projects/central-midfielders-clustering/notebook_clustering_cm.ipynb) |
|**Who is the next Lamine Yamal? Using data to identify similar undervalued profiles** | 09-11-2025 | [📝 Article](https://medium.com/@henrik.schjoth/who-is-the-next-lamine-yamal-using-data-to-identify-similar-undervalued-profiles-c22eb068dd64) <br> |
| **Data vs reality - A Legia Warsaw casestudy of how change in style affects scouting** | 11-09-2025 | [📝 Article](https://medium.com/@henrik.schjoth/data-vs-reality-how-a-change-in-style-affects-scouting-at-legia-warsaw-e1fb721871ba) <br> |
| **Clustering Wingers with Machine Learning** | 02-05-2025 | [📝 Article](https://medium.com/@henrik.schjoth/clustering-wingers-using-machine-learning-b067d2e26685) <br> |
| **Web Scraping - Creating a Pipeline** | 15-03-2025 | [📝 Article](https://medium.com/@henrik.schjoth/scraping-fbref-creating-a-pipeline-f5c9c23ba9da) |
| **Player Ratings - Fullback/Wingback (Progressor Role)** | 10-02-2025 | [📝 Article](https://medium.com/@henrik.schjoth/from-dataframe-to-player-ratings-5c05e4073e91) <br> |
| **Expected Threat Analysis** | 30-01-2025 | [📝 Article](https://medium.com/@henrik.schjoth/expected-threat-and-winning-7596715647d2) <br> [📄 Code](./projects/expected-threat/notebooks/xT-pitch.ipynb) |
| **Analyzing Runs Using Tracking Data** | 20-01-2025 | [📝 Article](https://medium.com/@henrik.schjoth/using-tracking-data-analyzing-runs-6eda008c6d49) <br> [📄 Code](./projects/analyzing-runs-with-tracking-data/analyzing_runs_with_tracking_data.py) |
| **Albert Grønbaæk - Danish Dynamite** | 13-01-2025 (originally feb 2024) | [📝 Article](https://medium.com/@henrik.schjoth/danish-dynamite-albert-gr%C3%B8nb%C3%A6k-d19c09959d74) |


##  Blog
You can find full articles and explanations on [my Medium profile](https://medium.com/@henrik.schjoth).

## 🔧 Tools & Data

**Python libraries**
- `pandas` / `numpy` – data processing and manipulation  
- `scikit-learn` – clustering and machine learning  
- `mplsoccer` – pitch plotting and football visualizations  
- `matplotlib` / `seaborn` – plots and charts  
- `statsbombpy` – loading StatsBomb event data (for some xT work)  
- `jupyter` – interactive analysis

**Data sources**
- Wyscout event & aggregated data – player ratings and clustering  
- FBref – stats for Albert Grønbaæk & possession data  
- Respovision tracking data – analyzing runs  
- StatsBomb open data – some xT experiments

`requirements.txt` is a combined list of dependencies used across all projects in this repository.
Some projects only use a subset of these libraries.

## Get Started
To run the notebooks, clone this repository and install the required Python packages:

```bash 
git clone https://github.com/n0rthface43/Ball.git
cd Ball
pip install -r requirements.txt
```

Then navigate to one of the project folders, for example:
```bash
cd projects/central-midfielders-clustering
# or cd projects/expected-threat
```
