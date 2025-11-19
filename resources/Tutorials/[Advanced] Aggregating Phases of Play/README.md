# 🧮 Phases of Play Aggregation

This notebook demonstrates how to aggregate **phase of play team-level match data** into **team metrics** using the `PhasesOfPlayAggregator.py`.

## 🎯 Goal
Transform raw PoP  data into some simple team level aggregates to get time spent in phase, count of phases, and link them to outcomes

## ⚙️ Workflow Overview
1. **Load Event Data**
   - Pulls `phases_of_play` for a given match from local files or the SkillCorner API.
2. **Initialize Aggregator**
   - Uses the `PhasesOfPlayAggregator` class to handle grouping, filtering, and metric computation.
3. **Generate Standard Aggregates**
   - Run Predefined aggregates such as (non-exhaustive):
     - `count_`: Aggregates of phase counts
     - `time_` : Aggregates of time spent in phase
     - `into_` : Aggregates of phase types linked with second
   - Run for each possession type
   - Merge
4. **Example of Visualization**
   - Enables you to create custom contexts and metrics to compute tailored KPIs (e.g., progressive carries, etc.).

## 🧰 Requirements
- Python 3.9+
- Libraries:  
  ```bash
  pip install numpy pandas skillcorner
