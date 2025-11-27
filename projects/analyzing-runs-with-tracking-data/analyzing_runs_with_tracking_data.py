#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analyzing forward runs with tracking data from the
2023 Champions League final (Manchester City vs Inter).

The script uses tracking-derived "runs" data and stories/event data
to visualise:
- Final-third forward runs for a single player
- Team-level forward run patterns (avg direction + variation)
- Comparisons between selected forwards
- (Optional) Possessions with xG, showing runs + passing chains

Data files are **not** included in the public repository because they
are proprietary (Respovision / course access). See README for details.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.cm import get_cmap
from matplotlib.patches import Wedge
from mplsoccer import Pitch


# ---------------------------------------------------------------------------
# PATHS & CONFIG
# ---------------------------------------------------------------------------

# Base path = folder where this script lives
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
VIZ_DIR = BASE_DIR / "viz"

# Make sure output folder exists
VIZ_DIR.mkdir(exist_ok=True)

# Data file paths (relative to repo root)
EVENTS_PATH = DATA_DIR / "18768058_events.parquet"
RUNS_PATH = DATA_DIR / "18768058_runs.parquet"
STORIES_PATH = DATA_DIR / "18768058_stories.parquet"
TRACKS_PATH = DATA_DIR / "18768058_tracks.parquet"

CITY_TEAM_ID = 1625
JACK_GREALISH = "Jack Grealish"


# ---------------------------------------------------------------------------
# DATA LOADING WITH NICE ERROR MESSAGE
# ---------------------------------------------------------------------------


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load events, runs, stories and tracks from the data/ folder.

    Raises
    ------
    FileNotFoundError
        If one or more required files are missing. The error message
        explains which files are missing and how to fix it.
    """
    required_paths = {
        "events": EVENTS_PATH,
        "runs": RUNS_PATH,
        "stories": STORIES_PATH,
        "tracks": TRACKS_PATH,
    }

    missing = [name for name, path in required_paths.items() if not path.exists()]

    if missing:
        missing_list = "\n".join(
            f"  - {name}: expected at {required_paths[name]}" for name in missing
        )
        raise FileNotFoundError(
            "One or more required data files are missing.\n\n"
            "Expected the following files in the 'data/' folder:\n"
            f"{missing_list}\n\n"
            "Please make sure you have these parquet files locally and that they\n"
            "are named exactly as above. See README.md for more details."
        )

    df_events = pd.read_parquet(EVENTS_PATH)
    df_runs = pd.read_parquet(RUNS_PATH)
    df_stories = pd.read_parquet(STORIES_PATH)
    df_tracks = pd.read_parquet(TRACKS_PATH)

    return df_events, df_runs, df_stories, df_tracks


# ---------------------------------------------------------------------------
# HELPER: SAVE + SHOW FIGURE
# ---------------------------------------------------------------------------


def save_and_show(fig: plt.Figure, filename: str) -> None:
    """
    Save figure to the viz/ folder and show it.

    Parameters
    ----------
    fig : Figure
        Matplotlib figure object.
    filename : str
        File name without path (e.g. "grealish_final_third_runs.png").
    """
    out_path = VIZ_DIR / filename
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved figure to: {out_path}")
    plt.show()


# ---------------------------------------------------------------------------
# VIS 1: GREALISH – FINAL THIRD RUNS
# ---------------------------------------------------------------------------


def plot_player_final_third_runs(df_runs: pd.DataFrame, player: str) -> None:
    """
    Plot all forward runs in the final third for a given player,
    plus their average run.

    Expects columns in df_runs:
    - 'player', 'start_x', 'start_y', 'end_x', 'end_y', 'Target'
    """
    player_df = df_runs[df_runs["player"] == player]

    # Final third and forward-only
    df_filtered = player_df[player_df["end_x"] >= 66.6]
    df_filtered = df_filtered[df_filtered["end_x"] > df_filtered["start_x"]]

    if df_filtered.empty:
        print(f"No final-third forward runs found for {player}.")
        return

    # Average run
    avg_start_x = df_filtered["start_x"].mean()
    avg_start_y = df_filtered["start_y"].mean()
    avg_end_x = df_filtered["end_x"].mean()
    avg_end_y = df_filtered["end_y"].mean()

    plt.style.use("ggplot")
    pitch = Pitch(
        pitch_type="opta",
        pitch_length=100,
        pitch_width=100,
        axis=False,
        label=False,
        line_color="#c5c9c7",
        pad_bottom=5,
        pad_top=10,
        linewidth=1.5,
        linestyle="-",
        goal_type="box",
        goal_alpha=1,
        corner_arcs=True,
        line_alpha=0.8,
        goal_linestyle="--",
    )

    fig, ax = pitch.draw(figsize=(13, 8))

    # Individual runs
    for _, row in df_filtered.iterrows():
        color = "green" if row.get("Target", False) else "deepskyblue"
        pitch.arrows(
            row["start_x"],
            row["start_y"],
            row["end_x"],
            row["end_y"],
            ax=ax,
            color=color,
            width=1.5,
            headwidth=3,
            headlength=3,
            alpha=0.9,
            zorder=2,
            facecolor=color,
            edgecolor="black",
        )

    # Average run
    pitch.arrows(
        avg_start_x,
        avg_start_y,
        avg_end_x,
        avg_end_y,
        ax=ax,
        color="red",
        width=2,
        headwidth=5,
        headlength=5,
        alpha=1.0,
        zorder=3,
        linestyle="-",
        label="Average run",
    )

    legend_elements = [
        plt.Line2D([0], [0], color="green", lw=2, label="Target runs"),
        plt.Line2D([0], [0], color="deepskyblue", lw=2, label="Off target runs"),
        plt.Line2D([0], [0], color="red", lw=2, label="Average run"),
    ]
    ax.legend(
        handles=legend_elements,
        loc="lower right",
        fontsize=10,
        frameon=False,
        bbox_to_anchor=(0.95, 0.07),
    )

    # Text and title
    ax.text(87, -3, "@Henrikschjoth", fontsize=10, color="black")
    ax.text(4.5, -2, "* Filtered for only forward runs", fontsize=8, color="black")
    ax.text(5.5, -4, "Data from Respovision", fontsize=8, color="black")
    ax.text(
        20,
        105,
        f"{player} final third runs* (vs Inter Milan), CL final 2023",
        fontsize=18,
        color="black",
    )

    save_and_show(fig, "grealish_final_third_runs.png")


# ---------------------------------------------------------------------------
# RUN STATS & TEAM PLOTS
# ---------------------------------------------------------------------------


def compute_player_run_stats(df_runs: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Compute average start position, run length, run angle and
    standard deviation of run angle for each player.

    Expects at least:
    - 'team_id', 'player', 'player_id',
      'start_x', 'start_y', 'end_x', 'end_y'

    Returns
    -------
    player_stats : DataFrame
    df_forward : DataFrame
        Subset of df_runs containing only forward runs.
    """
    # Forward runs only
    df_forward = df_runs[df_runs["end_x"] > df_runs["start_x"]].copy()

    df_forward["delta_x"] = df_forward["end_x"] - df_forward["start_x"]
    df_forward["delta_y"] = df_forward["end_y"] - df_forward["start_y"]
    df_forward["run_length"] = np.sqrt(df_forward["delta_x"] ** 2 + df_forward["delta_y"] ** 2)
    df_forward["run_angle"] = np.degrees(np.arctan2(df_forward["delta_y"], df_forward["delta_x"]))

    player_stats = (
        df_forward.groupby(["team_id", "player"])
        .agg(
            avg_start_x=("start_x", "mean"),
            avg_start_y=("start_y", "mean"),
            avg_run_length=("run_length", "mean"),
            avg_run_angle=("run_angle", "mean"),
            std_run_angle=("run_angle", "std"),
            player_id=("player_id", "first"),
        )
        .reset_index()
    )

    return player_stats, df_forward


def plot_team_run_patterns(player_stats: pd.DataFrame, city_team_id: int) -> None:
    """
    Plot average run and variation in run direction for both teams.
    One pitch for Manchester City, one for Inter.
    """
    pitch = Pitch(
        pitch_type="opta",
        pitch_length=100,
        pitch_width=100,
        axis=False,
        label=False,
        line_color="#c5c9c7",
        pad_bottom=5,
        pad_top=10,
        linewidth=1.5,
        linestyle="-",
        goal_type="box",
        goal_alpha=1,
        corner_arcs=True,
        line_alpha=0.8,
        goal_linestyle="--",
    )


    fig, axs = plt.subplots(1, 2, figsize=(25, 12))
    plt.subplots_adjust(wspace=0.1)

    # Manchester City
    city_players = player_stats[player_stats["team_id"] == city_team_id]
    pitch.draw(ax=axs[0])

    for _, row in city_players.iterrows():
        color = "lightblue"
        x = row["avg_start_x"]
        y = row["avg_start_y"]
        dx = row["avg_run_length"] * np.cos(np.radians(row["avg_run_angle"]))
        dy = row["avg_run_length"] * np.sin(np.radians(row["avg_run_angle"]))

        pitch.arrows(
            x,
            y,
            x + dx,
            y + dy,
            width=2,
            headwidth=5,
            headlength=5,
            color=color,
            alpha=0.9,
            ax=axs[0],
        )

        std_angle_deg = row["std_run_angle"]
        if pd.isna(std_angle_deg) or std_angle_deg == 0:
            std_angle_deg = 5

        wedge = Wedge(
            center=(x, y),
            r=row["avg_run_length"],
            theta1=row["avg_run_angle"] - std_angle_deg,
            theta2=row["avg_run_angle"] + std_angle_deg,
            facecolor=color,
            alpha=0.2,
        )
        axs[0].add_patch(wedge)

        axs[0].text(
            x,
            y - 2,
            row["player"],
            fontsize=8,
            ha="center",
            va="top",
            color="black",
        )

    axs[0].text(
        50,
        103,
        "Manchester City – average run and variation in run direction*",
        fontsize=16,
        color="black",
        ha="center",
    )
    axs[0].text(87, -3, "@Henrikschjoth", fontsize=10, color="black")
    axs[0].text(4.5, -2, "* Filtered for only forward runs", fontsize=8, color="black")
    axs[0].text(5.5, -4, "Data from Respovision", fontsize=8, color="black")

    # Inter
    inter_players = player_stats[player_stats["team_id"] != city_team_id]
    pitch.draw(ax=axs[1])

    for _, row in inter_players.iterrows():
        color = "red"
        x = row["avg_start_x"]
        y = row["avg_start_y"]
        dx = row["avg_run_length"] * np.cos(np.radians(row["avg_run_angle"]))
        dy = row["avg_run_length"] * np.sin(np.radians(row["avg_run_angle"]))

        pitch.arrows(
            x,
            y,
            x + dx,
            y + dy,
            width=2,
            headwidth=5,
            headlength=5,
            color=color,
            alpha=0.7,
            ax=axs[1],
        )

        std_angle_deg = row["std_run_angle"]
        if pd.isna(std_angle_deg) or std_angle_deg == 0:
            std_angle_deg = 5

        wedge = Wedge(
            center=(x, y),
            r=row["avg_run_length"],
            theta1=row["avg_run_angle"] - std_angle_deg,
            theta2=row["avg_run_angle"] + std_angle_deg,
            facecolor=color,
            alpha=0.2,
        )
        axs[1].add_patch(wedge)

        axs[1].text(
            x,
            y - 2,
            row["player"],
            fontsize=8,
            ha="center",
            va="top",
            color="black",
        )

    axs[1].text(
        50,
        103,
        "Inter Milan – average run and variation in run direction*",
        fontsize=16,
        color="black",
        ha="center",
    )
    axs[1].text(87, -3, "@Henrikschjoth", fontsize=10, color="black")
    axs[1].text(4.5, -2, "* Filtered for only forward runs", fontsize=8, color="black")
    axs[1].text(5.5, -4, "Data from Respovision", fontsize=8, color="black")

    save_and_show(fig, "team_run_patterns_city_vs_inter.png")

    # Also print std table to console
    std_table = player_stats[["player", "team_id", "std_run_angle"]].copy()
    std_table["team"] = std_table["team_id"].map(
        {city_team_id: "Manchester City"}
    ).fillna("Inter")
    std_table["std_run_angle"] = std_table["std_run_angle"].round(2)
    std_table = std_table.sort_values("std_run_angle", ascending=False).reset_index(
        drop=True
    )
    print(std_table[["player", "team", "std_run_angle"]])


# ---------------------------------------------------------------------------
# SELECTED PLAYERS
# ---------------------------------------------------------------------------


def plot_selected_players_patterns(player_stats: pd.DataFrame) -> None:
    """
    Plot average run and variation for a set of key forwards.
    """
    selected_players = ["Romelu Lukaku", "Lautaro Martínez", "Erling Haaland"]
    selected_player_stats = player_stats[player_stats["player"].isin(selected_players)]
    pitch = Pitch(
        pitch_type="opta",
        pitch_length=100,
        pitch_width=100,
        axis=False,
        label=False,
        line_color="#c5c9c7",
        pad_bottom=5,
        pad_top=10,
        linewidth=1.5,
        linestyle="-",
        goal_type="box",
        goal_alpha=1,
        corner_arcs=True,
        line_alpha=0.8,
        goal_linestyle="--",
    )


    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    pitch.draw(ax=ax)

    colors = {
        "Romelu Lukaku": "red",
        "Lautaro Martínez": "blue",
        "Erling Haaland": "green",
    }

    for _, row in selected_player_stats.iterrows():
        player_name = row["player"]
        color = colors.get(player_name, "black")
        x = row["avg_start_x"]
        y = row["avg_start_y"]
        dx = row["avg_run_length"] * np.cos(np.radians(row["avg_run_angle"]))
        dy = row["avg_run_length"] * np.sin(np.radians(row["avg_run_angle"]))

        pitch.arrows(
            x,
            y,
            x + dx,
            y + dy,
            width=2,
            headwidth=5,
            headlength=5,
            color=color,
            alpha=0.9,
            ax=ax,
            label=player_name,
        )

        std_angle_deg = row["std_run_angle"]
        if pd.isna(std_angle_deg) or std_angle_deg == 0:
            std_angle_deg = 5

        wedge = Wedge(
            center=(x, y),
            r=row["avg_run_length"],
            theta1=row["avg_run_angle"] - std_angle_deg,
            theta2=row["avg_run_angle"] + std_angle_deg,
            facecolor=color,
            alpha=0.2,
        )
        ax.add_patch(wedge)

    ax.set_title("Champions League Final – forward running patterns", fontsize=18)
    ax.legend(fontsize=12, loc="upper right")

    save_and_show(fig, "selected_forwards_patterns.png")


def plot_player_all_runs(df_runs: pd.DataFrame, player: str) -> None:
    """
    Plot all forward runs for a given player.
    """
    pitch = Pitch(
        pitch_type="opta",
        pitch_length=100,
        pitch_width=100,
        axis=False,
        label=False,
        line_color="#c5c9c7",
        pad_bottom=5,
        pad_top=10,
        linewidth=1.5,
        linestyle="-",
        goal_type="box",
        goal_alpha=1,
        corner_arcs=True,
        line_alpha=0.8,
        goal_linestyle="--",
    )



    player_runs = df_runs[
        (df_runs["player"] == player) & (df_runs["end_x"] > df_runs["start_x"])
    ]

    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    pitch.draw(ax=ax)

    for _, row in player_runs.iterrows():
        pitch.arrows(
            row["start_x"],
            row["start_y"],
            row["end_x"],
            row["end_y"],
            width=1.5,
            headwidth=4,
            headlength=4,
            color="green",
            alpha=0.8,
            ax=ax,
        )

    ax.set_title(f"Champions League Final – all runs by {player}", fontsize=18)

    filename = f"all_forward_runs_{player.replace(' ', '_').lower()}.png"
    save_and_show(fig, filename)


# ---------------------------------------------------------------------------
# OPTIONAL: POSSESSION RUNS + PASSING CHAINS (XG)
# ---------------------------------------------------------------------------


def plot_possession_runs_with_chain(
    xg_runs: pd.DataFrame,
    df_stories: pd.DataFrame,
    visualize_passing_chain: bool = True,
) -> None:
    """
    For each possession with xG, plot all runs and optionally the passing chain.

    Expects:
    - xg_runs: subset of runs with at least 'possession_id',
               'start_x', 'start_y', 'end_x', 'end_y',
               'Target', 'time_start', 'time_end', 'team_name'
    - df_stories: stories/events with 'possession_id', 'possession_team_id',
                  'team_id', 'start_x', 'start_y', 'end_x', 'end_y'
    """
    for possession_id, df_runs_pos in xg_runs.groupby("possession_id"):
        df_possession = df_stories[
            (df_stories["possession_id"] == possession_id)
            & (df_stories["possession_team_id"] == df_stories["team_id"])
        ]

        # Keep only last run per player in the possession
        df_runs_pos = df_runs_pos.drop_duplicates(subset="player", keep="last")

        fig, ax = plt.subplots(figsize=(10, 7))
        pitch = Pitch(
            pitch_type="opta",
            goal_type="box",
            pitch_color="w",
            linewidth=1,
            spot_scale=0,
            line_color="k",
            line_zorder=1,
        )
        pitch.draw(ax=ax)

        cmap = get_cmap("Set1")
        colors = list(cmap.colors)
        counter = 0

        # Plot runs
        for _, row in df_runs_pos.iterrows():
            color = colors[counter]
            pitch.arrows(
                row["start_x"],
                row["start_y"],
                row["end_x"],
                row["end_y"],
                width=1.8,
                headwidth=3,
                headlength=3,
                headaxislength=2,
                color=color,
                edgecolor="k" if row.get("Target", False) else color,
                linewidth=1 if row.get("Target", False) else 0,
                alpha=0.8,
                zorder=3,
                label=row["player"],
                ax=ax,
            )

            counter += 1
            if counter >= len(colors):
                counter = 0

        # Passing chain
        if visualize_passing_chain and not df_possession.empty:
            mask_in_pitch = df_possession["end_x"].between(1, 100)
            pitch.arrows(
                df_possession[mask_in_pitch]["start_x"],
                df_possession[mask_in_pitch]["start_y"],
                df_possession[mask_in_pitch]["end_x"],
                df_possession[mask_in_pitch]["end_y"],
                width=1,
                headwidth=5,
                alpha=0.5,
                ls="--",
                zorder=2,
                headlength=5,
                color="grey",
                ax=ax,
                label="completed passes",
            )

        possession_start_time = df_runs_pos["time_start"].min()[0:5]
        possession_end_time = df_runs_pos["time_end"].max()[0:5]
        team_name = df_runs_pos.iloc[0]["team_name"]

        ax.set_title(
            f"{team_name} runs in possession from {possession_start_time} to {possession_end_time}"
        )
        ax.legend(
            bbox_to_anchor=(0, 0),
            loc="upper left",
            fontsize="small",
            framealpha=0.0,
            ncol=1,
        )

        filename = f"possession_{team_name.replace(' ', '_').lower()}_{possession_id}.png"
        save_and_show(fig, filename)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------


def main() -> None:
    # Load data or show a clear error if files are missing
    df_events, df_runs, df_stories, df_tracks = load_data()

    # 1) Grealish – final third
    plot_player_final_third_runs(df_runs, JACK_GREALISH)

    # 2) Player run stats + team plots
    player_stats, df_forward = compute_player_run_stats(df_runs)
    plot_team_run_patterns(player_stats, CITY_TEAM_ID)

    # 3) Selected forwards
    plot_selected_players_patterns(player_stats)
    plot_player_all_runs(df_forward, "Erling Haaland")

    # 4) Possessions with xG (optional, only if column exists)
    if "xGRun" in df_forward.columns:
        xg_runs = df_forward[df_forward["xGRun"] > 0]
        if not xg_runs.empty:
            plot_possession_runs_with_chain(xg_runs, df_stories)
        else:
            print("No runs with xGRun > 0 found – skipping possession visualisation.")
    else:
        print("Column 'xGRun' not found in runs data – skipping xG possession plots.")


if __name__ == "__main__":
    main()
