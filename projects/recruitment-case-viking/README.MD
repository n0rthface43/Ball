This project contains the code and workflow used for a recruitment case for Viking FK.  
The notebook demonstrates how to merge multiple league exports from Wyscout into a single, structured dataset ready for further analysis.

---

## File structure:
recruitment-case-viking/
│
├── notebook.ipynb # Notebook with preprocessing and merging of files
│
├── data/
│ ├── raw/ # Put Wyscout files here (not included in repo)
│ └── processed/ # Output generated automatically
│
└── viz/ # Space for visualisations
---

## ⚠️ Wyscout data not included

Due to licensing restrictions, raw Wyscout data cannot be uploaded to GitHub.  
To run the notebook, you must:

1. Have access to Wyscout  
2. Export the required league files  
3. Place them inside:

projects/recruitment-case-viking/data/raw/
```
projects/recruitment-case-viking/data/raw/
```
Install requirements
```
pip install -r requirements.txt
```
```
jupyter notebook notebook.ipynb
```
