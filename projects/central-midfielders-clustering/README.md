# Clustering & Ranking Central Midfielders

This project groups central midfielders in Europe’s top 5 leagues into stylistic roles using
Wyscout 2024/25 data. The approach focuses on style-of-play metrics rather than outcome/success metrics.

📄 Article:  
https://medium.com/@henrik.schjoth/clustering-and-ranking-central-midfielders-b4ddea2e83e7

---

## Summary of Method

1. **Preprocessing**
   - Filter CMs (RCMF/LCMF), min 900 minutes.
   - Keep only top 5 leagues.
   - Optional: Possession-adjust volume metrics.

2. **Feature Engineering**
   - 25+ playstyle features added:
     pass-direction shares, duel-balance, midfield tilt, carry vs pass ratios, etc.

3. **Feature Selection (Round 1)**
   - Remove correlated features (>0.90).
   - Remove low-variance features (<0.02).
   - PCA → K-means → Random Forest (feature importance).

4. **Final Model (Round 2)**
   - Use selected *important_features*.
   - Apply weighting to key metrics (progression, dribbling, duel balance).
   - New StandardScaler → PCA → K-means.
   - Random Forest to identify what separates clusters.

5. **Ranking Players**
   - Per-cluster ranking using performance metrics (xG, xA, success rates).
   - Style features define roles → outcome metrics define performance.

6. **Robustness Across Seasons**
   - Project 23/24 and 25/26 data into the 24/25 model.
   - Evaluate role stability cluster-by-cluster.

---

## Note on Code vs Article

This repository contains an earlier version of the codebase.  
The Medium article reflects a slightly updated pipeline (feature choices, weights, ordering).  
Therefore, PCA shapes, RF importance values, and some visual outputs may differ from the article.

---

## Run the Project

To run without Wyscout data:

```python
USE_EXAMPLE_DATA = True

central-midfielders-clustering/
│── data/
│── notebooks/
│── viz/
│── README.md
