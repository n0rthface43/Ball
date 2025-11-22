# Clustering & Ranking Central Midfielders

This project identifies style-based roles for central midfielders in Europe's top 5 leagues
using Wyscout 2024/25 data.

- 📄 Article: [Clustering and Ranking Central Midfielders](https://medium.com/@henrik.schjoth/clustering-and-ranking-central-midfielders-b4ddea2e83e7)
- 📊 Data source: Wyscout event & aggregated data (not included in this repo)
- 🎯 Goal: Group CMs by style and then rank players within each group.

## Methodology (short)

1. Preprocess Wyscout data (filter CMs, min 900 minutes).
2. Create style features (pass direction shares, midfield tilt, duel balance, etc.).
3. Remove highly correlated & low-variance features.
4. PCA → K-means clustering → Random Forest for feature importance.
5. Refine with feature weighting + new PCA/K-means.
6. Rank players *within* each role using outcome metrics (xG, xA, success rates).
7. Check model robustnes across seasons

Full description in the article.

## How to run

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

jupyter lab
# open notebooks/cm_clustering_24_25_clean.ipynb
