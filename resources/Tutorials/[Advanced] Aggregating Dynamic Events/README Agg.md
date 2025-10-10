# 🧮 Dynamic Events Aggregation

This notebook demonstrates how to aggregate **event-level match data** into **player-match level metrics** using the `DynamicEventAggregator`.

## 🎯 Goal
Transform raw dynamic event data (each row = individual event in a match) into summarized player-level statistics — e.g., total off-ball runs, line-breaking passes, and defensive engagements per player per match.

## ⚙️ Workflow Overview
1. **Load Event Data**
   - Pulls `dynamic_events` for a given match from local files or the SkillCorner API.
2. **Initialize Aggregator**
   - Uses the `DynamicEventAggregator` class to handle grouping, filtering, and metric computation.
3. **Generate Standard Aggregates**
   - Predefined aggregates such as (non-exhaustive):
     - `off_ball_runs`: Aggregates of counts, threat and splits by phase
     - `line_breaking_passes`
     - `defensive_engagements` : Aggregates across all on-ball engagements
     - `pressing`: Specific focus on pressing onball engagements
4. **Create Custom Aggregates (Optional)**
   - Enables you to create custom contexts and metrics to compute tailored KPIs (e.g., progressive carries, etc.).
5. **Export Aggregated Output**
   - Produces one row per **player–match** combination, with hundreds of derived performance features (≈800+ columns).

## 🧰 Requirements
- Python 3.9+
- Libraries:  
  ```bash
  pip install numpy pandas skillcorner
