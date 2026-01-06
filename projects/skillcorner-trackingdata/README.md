# Exploring Tracking Data from SkillCorner and Pitch Control 

This project contains notebooks for pitch control analysis based on SkillCorner tracking data.
The main focus is implementing and visualising pitch control models, including frame-by-frame
analysis and optional video generation.

📄 Article:  
https://medium.com/@henrik.schjoth/relevant-pitch-control-and-scoring-threat-exploring-time-and-space-7fb967805811

---

## 📁 Project structure
skillcorner-trackingdata/
│
├── pitch-control_RPC_RSV.ipynb # Main pitch control notebook
├── README.md # Project documentation
├── .gitignore # Ignores local data and generated outputs
│
├── data/ # Local tracking data (NOT included in repo)
├── resources/ # Supporting files / references
└── viz/ # Generated figures (ignored)

---

## Main notebook

### `pitch-control_RPC_RSV.ipynb`

This notebook:
- Implements a pitch control model using tracking data
- Generates spatial pitch control visualisations
- Optionally produces video outputs (heavy runtime)

---

## ⚠️ Data not included

Tracking data is **not included** in this repository due to size and licensing restrictions.

To run the notebook, place your local SkillCorner data inside:

---
projects/skillcorner-trackingdata/data/
