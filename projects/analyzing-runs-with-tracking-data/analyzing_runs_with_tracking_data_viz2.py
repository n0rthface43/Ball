#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extra visualisations for forward runs in the
2023 Champions League final (Manchester City vs Inter).

This script reproduces and extends the original “kode del 2”:
- Grealish final-third forward runs
- Team-level average run + variation (City vs Inter)
- Selected forwards (Lukaku, Lautaro, Haaland)
- All runs for Haaland
- Lukaku vs Haaland (all runs + xGRun-only)
- Possessions with xGRun > 0: runs + passing chain

Data files are NOT part of the public repo (proprietary).
They must exist in the local `data/` folder.
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

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
FIG_DIR = BASE_DIR / "figures"

FIG_DIR.mkdir(exist_ok=True)

EVENTS_PATH = DATA_DIR / "18768058_events.parquet"
RUNS_PATH = DATA_DIR / "18768058_runs.parquet"
STORIES_PATH = DATA_DIR / "18768058_stories.parquet"
TRACKS_PATH = DATA_DIR / "18768058_tracks.parquet"

CITY_TEAM_ID = 1625
JACK_GREALISH = "Jack Grealish"


# ---------------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------------

def load_data():
    """
    Load required parquet files from data/.

    Raises
    ------
    FileNotFoundError
        If one or more files are missing.
    """
    required = {
        "events": EVENTS_PATH,
        "runs": RUNS_PATH,
        "stories": STORIES_PATH,
        "tracks": TRACKS_PATH,
    }

    missing = [name for name, path in required.items() if not path.exists()]
    if missing:
        missing_list = "\n".join(
            f"  - {name}: expected at {required[name]}" for name in missing
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
# HELPER
# ---------------------------------------------------------------------------

def save_and_show(fig: plt.Figure, filename: str) -> None:
    """Save figure to figures/ and show it."""
    out_path = FIG_DIR / filename
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved figure to: {out_path}")
    plt.show()


# ---------------------------------------------------------------------------
# STATS
# ---------------------------------------------------------------------------

def compute_player_run_stats(df_runs: pd.DataFrame, df_stories: pd.DataFrame):
    """
    Reproduce original logic:
    - concat runs + stories
    - keep forward runs (end_x > start_x)
    - compute run_length + run_angle
    - aggregate per player

    Returns
    -------
    player_stats : DataFrame
    df_forward : DataFrame
        All forward runs used for the stats (like original `df`).
    """
    df = pd.concat([df_runs, df_stories], ignore_index=True)

    df = df[df["end_x"] > df["start_x"]].copy()

    df["delta_x"] = df["end_x"] - df["start_x"]
    df["delta_y"] = df["end_y"] - df["start_y"]
    df["run_length"] = np.sqrt(df["delta_x"] ** 2 + df["delta_y"] ** 2)
    df["run_angle"] = np.degrees(np.arctan2(df["delta_y"], df["delta_x"]))

    player_stats = (
        df.groupby(["team_id", "player"])
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

    return player_stats, df


# ---------------------------------------------------------------------------
# VISUALISATIONS
# ---------------------------------------------------------------------------

def plot_grealish_final_third(df_runs: pd.DataFrame, player: str = JACK_GREALISH):
    """Final-third forward runs for Jack Grealish + average run."""
    player_df = df_runs[df_runs["player"] == player]

    df_filtered = player_df[player_df["end_x"] >= 66.6]
    df_filtered = df_filtered[df_filtered["end_x"] > df_filtered["start_x"]]

    if df_filtered.empty:
        print(f"No final-third forward runs found for {player}.")
        return

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

    save_and_show(fig, "grealish_final_third_runs_viz2.png")


def plot_team_patterns(player_stats: pd.DataFrame, city_team_id: int = CITY_TEAM_ID):
    """City vs Inter – average run + variation (original double-pitch)."""
    pitch = Pitch(
        pitch_type="opta",
        pitch_length=100,
        pitch_width=100,
        line_color="#c5c9c7",
        linewidth=1.5,
        goal_type="box",
        pad_top=10,
        corner_arcs=True,
        goal_alpha=1,
        goal_linestyle="--",
        line_alpha=0.8,
    )

    fig, axs = plt.subplots(1, 2, figsize=(25, 12))
    plt.subplots_adjust(wspace=0.1)

    # City
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
        "Manchester City, average run and variation in run direction*",
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
        "Inter Milan, average run and variation in run direction*",
        fontsize=16,
        color="black",
        ha="center",
    )
    axs[1].text(87, -3, "@Henrikschjoth", fontsize=10, color="black")
    axs[1].text(4.5, -2, "* Filtered for only forward runs", fontsize=8, color="black")
    axs[1].text(5.5, -4, "Data from Respovision", fontsize=8, color="black")

    save_and_show(fig, "team_run_patterns_city_vs_inter_viz2.png")

    # Also print std table (like original)
    std_table = player_stats[["player", "team_id", "std_run_angle"]].copy()
    std_table["team"] = std_table["team_id"].map({city_team_id: "Manchester City"}).fillna(
        "Inter"
    )
    std_table["std_run_angle"] = std_table["std_run_angle"].round(2)
    std_table = std_table.sort_values("std_run_angle", ascending=False).reset_index(
        drop=True
    )
    print(std_table[["player", "team", "std_run_angle"]])


def plot_selected_three(player_stats: pd.DataFrame):
    """Lukaku, Lautaro, Haaland – average run + variation on one pitch."""
    selected_players = ["Romelu Lukaku", "Lautaro Martínez", "Erling Haaland"]
    selected = player_stats[player_stats["player"].isin(selected_players)]

    pitch = Pitch(
        pitch_type="opta",
        pitch_length=100,
        pitch_width=100,
        line_color="#c5c9c7",
        linewidth=1.5,
        goal_type="box",
        pad_top=10,
        corner_arcs=True,
        goal_alpha=1,
        goal_linestyle="--",
        line_alpha=0.8,
    )

    fig, ax = plt.subplots(figsize=(12, 8))
    pitch.draw(ax=ax)

    colors = {
        "Romelu Lukaku": "red",
        "Lautaro Martínez": "blue",
        "Erling Haaland": "green",
    }

    for _, row in selected.iterrows():
        player_name = row["player"]
        color = colors[player_name]
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

    save_and_show(fig, "selected_forwards_three_viz2.png")


def plot_haaland_all_runs(df_forward: pd.DataFrame):
    """All forward runs for Erling Haaland."""
    pitch = Pitch(
        pitch_type="opta",
        pitch_length=100,
        pitch_width=100,
        line_color="#c5c9c7",
        linewidth=1.5,
        goal_type="box",
        pad_top=10,
        corner_arcs=True,
        goal_alpha=1,
        goal_linestyle="--",
        line_alpha=0.8,
    )

    erling_runs = df_forward[
        (df_forward["player"] == "Erling Haaland") & (df_forward["end_x"] > df_forward["start_x"])
    ]

    fig, ax = plt.subplots(figsize=(12, 8))
    pitch.draw(ax=ax)

    for _, row in erling_runs.iterrows():
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

    ax.set_title("Champions League Final – All forward runs by Erling Haaland", fontsize=18)
    save_and_show(fig, "all_forward_runs_haaland_viz2.png")


def plot_lukaku_vs_haaland(df_forward: pd.DataFrame, player_stats: pd.DataFrame):
    """Side-by-side all runs + average pattern for Lukaku vs Haaland."""
    selected_players = ["Romelu Lukaku", "Erling Haaland"]
    selected_stats = player_stats[player_stats["player"].isin(selected_players)]

    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    pitch = Pitch(
        pitch_type="opta",
        pitch_length=100,
        pitch_width=100,
        line_color="#c5c9c7",
        linewidth=1.5,
        goal_type="box",
        pad_top=10,
        corner_arcs=True,
        goal_alpha=1,
        goal_linestyle="--",
        line_alpha=0.8,
    )

    colors = {"Romelu Lukaku": "red", "Erling Haaland": "green"}

    for i, player in enumerate(selected_players):
        ax = axes[i]
        pitch.draw(ax=ax)

        stats_player = selected_stats[selected_stats["player"] == player]
        runs_player = df_forward[
            (df_forward["player"] == player) & (df_forward["end_x"] > df_forward["start_x"])
        ]

        # All runs
        for _, run in runs_player.iterrows():
            pitch.arrows(
                run["start_x"],
                run["start_y"],
                run["end_x"],
                run["end_y"],
                width=1.5,
                headwidth=4,
                headlength=4,
                color=colors[player],
                alpha=0.8,
                ax=ax,
            )

        # Average + wedge
        for _, row in stats_player.iterrows():
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
                color=colors[player],
                alpha=0.9,
                ax=ax,
                label=f"Average {player}",
            )

            std_angle_deg = row["std_run_angle"]
            if pd.isna(std_angle_deg) or std_angle_deg == 0:
                std_angle_deg = 5

            wedge = Wedge(
                center=(x, y),
                r=row["avg_run_length"],
                theta1=row["avg_run_angle"] - std_angle_deg,
                theta2=row["avg_run_angle"] + std_angle_deg,
                facecolor=colors[player],
                alpha=0.2,
            )
            ax.add_patch(wedge)

        ax.set_title(f"{player} – Runs and Average Pattern", fontsize=16)

    plt.tight_layout()
    save_and_show(fig, "lukaku_vs_haaland_viz2.png")


def plot_lukaku_haaland_xg_runs(df_forward: pd.DataFrame, player_stats: pd.DataFrame):
    """Same som over, men kun for xGRun > 0."""
    if "xGRun" not in df_forward.columns:
        print("Column 'xGRun' not found – skipping xG-only plots.")
        return

    xg_run = df_forward[df_forward["xGRun"] > 0]
    if xg_run.empty:
        print("No rows with xGRun > 0 – skipping xG-only plots.")
        return

    selected_players = ["Romelu Lukaku", "Erling Haaland"]
    selected_stats = player_stats[player_stats["player"].isin(selected_players)]

    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    pitch = Pitch(
        pitch_type="opta",
        pitch_length=100,
        pitch_width=100,
        line_color="#c5c9c7",
        linewidth=1.5,
        goal_type="box",
        pad_top=10,
        corner_arcs=True,
        goal_alpha=1,
        goal_linestyle="--",
        line_alpha=0.8,
    )

    colors = {"Romelu Lukaku": "red", "Erling Haaland": "green"}

    for i, player in enumerate(selected_players):
        ax = axes[i]
        pitch.draw(ax=ax)

        stats_player = selected_stats[selected_stats["player"] == player]
        runs_player = xg_run[
            (xg_run["player"] == player) & (xg_run["end_x"] > xg_run["start_x"])
        ]

        for _, run in runs_player.iterrows():
            pitch.arrows(
                run["start_x"],
                run["start_y"],
                run["end_x"],
                run["end_y"],
                width=1.5,
                headwidth=4,
                headlength=4,
                color=colors[player],
                alpha=0.8,
                ax=ax,
            )

        for _, row in stats_player.iterrows():
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
                color=colors[player],
                alpha=0.9,
                ax=ax,
                label=f"Average {player}",
            )

            std_angle_deg = row["std_run_angle"]
            if pd.isna(std_angle_deg) or std_angle_deg == 0:
                std_angle_deg = 5

            wedge = Wedge(
                center=(x, y),
                r=row["avg_run_length"],
                theta1=row["avg_run_angle"] - std_angle_deg,
                theta2=row["avg_run_angle"] + std_angle_deg,
                facecolor=colors[player],
                alpha=0.2,
            )
            ax.add_patch(wedge)

        ax.text(
            50,
            105,
            f"{player} – Runs and variation in direction (xG only)",
            fontsize=16,
            ha="center",
            va="center",
            color="black",
        )
        ax.text(87, -3, "@Henrikschjoth", fontsize=10, color="black")
        ax.text(4.5, -2, "* Filtered for only forward runs", fontsize=8, color="black")
        ax.text(5.5, -4, "Data from Respovision", fontsize=8, color="black")

    plt.tight_layout()
    save_and_show(fig, "lukaku_haaland_xg_runs_viz2.png")


def plot_possessions_with_runs_and_passing_chain(
    df_forward: pd.DataFrame, df_stories: pd.DataFrame
):
    """
    For each possession with xGRun > 0:
    - plot last run per player
    - optionally overlay passing chain.

    Matches the spirit av original `for possession_id, df_runs in xG_run.groupby(...)`.
    """
    if "xGRun" not in df_forward.columns:
        print("Column 'xGRun' not found – skipping possession plots.")
        return

    xg_run = df_forward[df_forward["xGRun"] > 0]
    if xg_run.empty:
        print("No rows with xGRun > 0 – skipping possession plots.")
        return

    visualize_passing_chain = True

    for possession_id, df_runs_pos in xg_run.groupby("possession_id"):
        df_possession = df_stories[
            (df_stories["possession_id"] == possession_id)
            & (df_stories["possession_team_id"] == df_stories["team_id"])
        ]

        df_runs_pos = df_runs_pos.drop_duplicates(subset="player", keep="last")

        fig, ax = plt.subplots(figsize=(10, 7))
        pitch = Pitch(
            pitch_type="opta",
            goal_type="box",
            pitch_color="w",
            linewidth=1,
            line_color="k",
            line_zorder=1,
        )
        pitch.draw(ax=ax)

        cmap = get_cmap("Set1")
        colors = list(cmap.colors)
        counter = 0

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

        filename = (
            f"possession_runs_{team_name.replace(' ', '_').lower()}_{possession_id}_viz2.png"
        )
        save_and_show(fig, filename)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    df_events, df_runs, df_stories, df_tracks = load_data()

    # Stats (matching original logic)
    player_stats, df_forward = compute_player_run_stats(df_runs, df_stories)

    # Visuals
    plot_grealish_final_third(df_runs, JACK_GREALISH)
    plot_team_patterns(player_stats, CITY_TEAM_ID)
    plot_selected_three(player_stats)
    plot_haaland_all_runs(df_forward)
    plot_lukaku_vs_haaland(df_forward, player_stats)
    plot_lukaku_haaland_xg_runs(df_forward, player_stats)
    plot_possessions_with_runs_and_passing_chain(df_forward, df_stories)


if __name__ == "__main__":
    main()
