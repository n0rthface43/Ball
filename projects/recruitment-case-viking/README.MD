This project contains the code and workflow used for a recruitment case for Viking FK.
The notebook demonstrates how to merge multiple league exports from Wyscout into a single, structured dataset ready for further analysis.

File structure:
recruitment-case-viking/
│
├── notebook.ipynb                 # notebook with preprocessing and merging of files
│
├── data/
│   ├── raw/                       # Put wyscout file here (Not included in repo)
│   └── processed/                 # Output genererated automatically
│
└── viz/                           # space for vizualisations


Due to licensing restrictions, raw Wyscout data cannot be uploaded to GitHub.
To run the notebook, you must:

Have access to Wyscout
Export the required league files
Place them inside:
'''
projects/recruitment-case-viking/data/raw/
'''
Install requirements
'''
pip install -r requirements.txt
'''
'''
jupyter notebook notebook.ipynb
'''
