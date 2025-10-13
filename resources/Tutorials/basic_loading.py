import pandas as pd

match_id = 1886347

# Dynamic Events
de_match = pd.read_csv(f"../../data/matches/{match_id}/{match_id}_dynamic_events.csv")

# Phases of Play
pop_match = pd.read_csv(f"../../data/matches/{match_id}/{match_id}_dynamic_events.csv")

#
tracking_data = pd.read_json(
    f"../data/matches/{match_id}/{match_id}_tracking_extrapolated.jsonl", lines=True
)
