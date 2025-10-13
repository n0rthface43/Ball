import pandas as pd
import numpy as np


# Helper function to count pass opportunities
def count_pass_opportunities(x):
    sorted_intervals = sorted(
        x[["frame_start", "frame_end"]].values.tolist(), key=lambda y: y[0]
    )
    merged_intervals = []
    prev_end = -float("inf")  # To track the end of the last interval

    for start, end in sorted_intervals:
        if start > prev_end:
            merged_intervals.append((start, end))  # New non-overlapping interval
            prev_end = end
        else:
            prev_end = max(prev_end, end)  # Merge with the current interval

    return len(merged_intervals)


# Helper function to get th sum of a value in pass opportunities
def metric_sum_pass_opportunities(x, column="xthreat"):
    """
    Sum values from a specific column (e.g., pass_distance) across non-overlapping intervals.

    Args:
        x (pd.DataFrame): Data for a specific context.
        column (str): The name of the column to sum (default: 'pass_distance').

    Returns:
        float: The sum of the specified column for non-overlapping intervals.
    """
    # Sort intervals by the start of each frame
    sorted_intervals = sorted(
        x[["frame_start", "frame_end", column]].values.tolist(), key=lambda y: y[0]
    )
    merged_intervals = []
    prev_end = -float("inf")  # To track the end of the last interval
    total_sum = 0  # Initialize the sum

    for start, end, value in sorted_intervals:
        if start > prev_end:
            # If no overlap, add the value to the total sum
            merged_intervals.append((start, end))
            total_sum += value
            prev_end = end
        else:
            # If there's overlap, just update the end of the merged interval and add the value
            prev_end = max(prev_end, end)
            total_sum += value

    return total_sum


class DynamicEventAggregator:
    """
    A class to process and aggregate dynamic event data for different context and metric groups.
    """

    def __init__(self, df, custom_context_groups=None, custom_metric_groups=None):
        """
        Initialize the aggregator with event data and optional grouped contexts and metrics.

        Args:
            df (pd.DataFrame): The DataFrame containing event data.
            custom_context_groups (dict, optional): User-defined grouped contexts.
            custom_metric_groups (dict, optional): User-defined grouped metrics.
        """
        self.df = df
        self.context_groups = self._define_context_groups(custom_context_groups)
        self.metric_groups = self._define_metric_groups(custom_metric_groups)

    def _define_context_groups(self, custom_context_groups):
        """
        Define grouped filtering conditions for different event contexts.

        Args:
            custom_context_groups (dict, optional): Additional user-defined context groups.

        Returns:
            dict: A dictionary where keys are group names, and values are context dictionaries.
        """
        default_context_groups = {
            "off_ball_runs": {
                "off_ball_runs": (self.df["event_type"] == "off_ball_run"),
                "off_ball_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "off_ball_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "off_ball_runs_in_build_up": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "off_ball_runs_in_transition": (
                    (self.df["event_type"] == "off_ball_run")
                    & (
                        self.df["team_in_possession_phase_type"].isin(
                            ["transition", "quick_break"]
                        )
                    )
                ),
                "cross_receiver": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "cross_receiver")
                ),
                "cross_receiver_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "cross_receiver")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "runs_in_behind": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "behind")
                ),
                "runs_in_behind_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "behind")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "runs_in_behind_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "behind")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "runs_in_behind_in_transition": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "behind")
                    & (
                        self.df["team_in_possession_phase_type"].isin(
                            ["transition", "quick_break"]
                        )
                    )
                ),
                "runs_ahead_of_the_ball": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "run_ahead_of_the_ball")
                ),
                "runs_ahead_of_the_ball_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "run_ahead_of_the_ball")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "runs_ahead_of_the_ball_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "run_ahead_of_the_ball")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "runs_ahead_of_the_ball_in_transition": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "run_ahead_of_the_ball")
                    & (
                        self.df["team_in_possession_phase_type"].isin(
                            ["transition", "quick_break"]
                        )
                    )
                ),
                "support_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "support")
                ),
                "support_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "support")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "support_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "support")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "support_runs_in_transition": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "support")
                    & (
                        self.df["team_in_possession_phase_type"].isin(
                            ["transition", "quick_break"]
                        )
                    )
                ),
                "overlap_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "overlap")
                ),
                "overlap_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "overlap")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "overlap_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "overlap")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "overlap_runs_in_transition": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "overlap")
                    & (
                        self.df["team_in_possession_phase_type"].isin(
                            ["transition", "quick_break"]
                        )
                    )
                ),
                "underlap_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "underlap")
                ),
                "underlap_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "underlap")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "coming_short_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "coming_short")
                ),
                "coming_short_runs_in_build_up": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "coming_short")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "coming_short_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "coming_short")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "coming_short_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "coming_short")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "pulling_half_space_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_half_space")
                ),
                "pulling_half_space_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_half_space")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "pulling_half_space_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_half_space")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "pulling_wide_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_wide")
                ),
                "pulling_wide_runs_in_build_up": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_wide")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "pulling_wide_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_wide")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "pulling_wide_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_wide")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "dropping_off_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "dropping_off")
                ),
                "dropping_off_runs_in_build_up": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "dropping_off")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "dropping_off_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "dropping_off")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
            },
            "line_breaking_options": {
                "passing_option": ((self.df["event_type"] == "passing_option")),
                "passing_option_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "passing_option_in_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "passing_option_in_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "through_first_line": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                ),
                "through_first_line_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "through_first_line_in_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "through_first_line_in_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "around_first_line": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                ),
                "around_first_line_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "around_first_line_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "around_first_line_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "through_second_last_line": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                ),
                "through_second_last_line_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "through_second_last_line_in_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "through_second_last_line_in_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "around_second_last_line": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                ),
                "around_second_last_line_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "around_second_last_line_in_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "around_second_last_line_in_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "through_last_line": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                ),
                "through_last_line_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "through_last_line_in_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "through_last_line_in_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "around_last_line": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                ),
                "around_last_line_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "around_last_line_in_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "around_last_line_in_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
            },
            "passes_to_off_ball_runs": {
                "off_ball_runs": (self.df["event_type"] == "off_ball_run"),
                "off_ball_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "off_ball_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "off_ball_runs_in_build_up": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "off_ball_runs_in_transition": (
                    (self.df["event_type"] == "off_ball_run")
                    & (
                        self.df["team_in_possession_phase_type"].isin(
                            ["transition", "quick_break"]
                        )
                    )
                ),
                "cross_receiver": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "cross_receiver")
                ),
                "cross_receiver_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "cross_receiver")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "runs_in_behind": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "behind")
                ),
                "runs_in_behind_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "behind")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "runs_in_behind_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "behind")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "runs_in_behind_in_transition": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "behind")
                    & (
                        self.df["team_in_possession_phase_type"].isin(
                            ["transition", "quick_break"]
                        )
                    )
                ),
                "runs_ahead_of_the_ball": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "run_ahead_of_the_ball")
                ),
                "runs_ahead_of_the_ball_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "run_ahead_of_the_ball")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "runs_ahead_of_the_ball_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "run_ahead_of_the_ball")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "runs_ahead_of_the_ball_in_transition": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "run_ahead_of_the_ball")
                    & (
                        self.df["team_in_possession_phase_type"].isin(
                            ["transition", "quick_break"]
                        )
                    )
                ),
                "support_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "support")
                ),
                "support_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "support")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "support_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "support")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "support_runs_in_transition": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "support")
                    & (
                        self.df["team_in_possession_phase_type"].isin(
                            ["transition", "quick_break"]
                        )
                    )
                ),
                "overlap_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "overlap")
                ),
                "overlap_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "overlap")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "overlap_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "overlap")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "overlap_runs_in_transition": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "overlap")
                    & (
                        self.df["team_in_possession_phase_type"].isin(
                            ["transition", "quick_break"]
                        )
                    )
                ),
                "underlap_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "underlap")
                ),
                "underlap_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "underlap")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "coming_short_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "coming_short")
                ),
                "coming_short_runs_in_build_up": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "coming_short")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "coming_short_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "coming_short")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "coming_short_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "coming_short")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "pulling_half_space_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_half_space")
                ),
                "pulling_half_space_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_half_space")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "pulling_half_space_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_half_space")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "pulling_wide_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_wide")
                ),
                "pulling_wide_runs_in_build_up": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_wide")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "pulling_wide_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_wide")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "pulling_wide_runs_in_finish": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "pulling_wide")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "dropping_off_runs": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "dropping_off")
                ),
                "dropping_off_runs_in_build_up": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "dropping_off")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "dropping_off_runs_in_create": (
                    (self.df["event_type"] == "off_ball_run")
                    & (self.df["event_subtype"] == "dropping_off")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
            },
            "line_breaking_passes": {
                "passing_option": ((self.df["event_type"] == "passing_option")),
                "passing_option_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "passing_option_in_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "passing_option_in_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "through_first_line": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                ),
                "through_first_line_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "through_first_line_in_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "through_first_line_in_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "around_first_line": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                ),
                "around_first_line_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "around_first_line_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "around_first_line_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "first")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "through_second_last_line": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                ),
                "through_second_last_line_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "through_second_last_line_in_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "through_second_last_line_in_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "around_second_last_line": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                ),
                "around_second_last_line_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "around_second_last_line_in_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "around_second_last_line_in_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "second_last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "through_last_line": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                ),
                "through_last_line_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "through_last_line_in_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "through_last_line_in_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "through")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "around_last_line": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                ),
                "around_last_line_in_build_up": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "around_last_line_in_create": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "around_last_line_in_finish": (
                    (self.df["event_type"] == "passing_option")
                    & (self.df["furthest_line_break"] == "last")
                    & (self.df["furthest_line_break_type"] == "around")
                    & (self.df["interplayer_distance_range"] != "long")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
            },
            "possessions": {
                "all_possessions": (self.df["event_type"] == "player_possession"),
                "possessions_in_build_up": (
                    (self.df["event_type"] == "player_possession")
                    & (self.df["team_in_possession_phase_type"] == "build_up")
                ),
                "possessions_in_create": (
                    (self.df["event_type"] == "player_possession")
                    & (self.df["team_in_possession_phase_type"] == "create")
                ),
                "possessions_in_finish": (
                    (self.df["event_type"] == "player_possession")
                    & (self.df["team_in_possession_phase_type"] == "finish")
                ),
                "possessions_in_transition": (
                    (self.df["event_type"] == "player_possession")
                    & (
                        self.df["team_in_possession_phase_type"].isin(
                            ["transition", "quick_break"]
                        )
                    )
                ),
                "possession_retentions": (
                    (self.df["event_type"] == "player_possession")
                    & (self.df.end_type == "pass")
                    & (self.df.pass_outcome == "successful")
                ),
            },
            "on_ball_engagements": {
                "on_ball_engagements": (self.df["event_type"] == "on_ball_engagement"),
                "pressing": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "pressing")
                ),
                "pressure": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "pressure")
                ),
                "counter_press": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "counter_press")
                ),
                "recovery_press": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "recovery_press")
                ),
                "other": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "other")
                ),
                "isolated_engagement": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["n_player_targeted_teammates_within_5m_start"] == 0)
                    & (self.df["n_player_targeted_opponents_within_5m_start"] == 0)
                ),
                "on_ball_engagements_organised": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (
                        self.df["team_out_of_possession_phase_type"].isin(
                            ["low_block", "medium_block", "high_block"]
                        )
                    )
                ),
                "on_ball_engagements_in_transition": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (
                        self.df["team_out_of_possession_phase_type"].isin(
                            ["defending_transition", "defending_quick_break"]
                        )
                    )
                ),
            },
            "pressing_engagements": {
                "on_ball_engagements": (self.df["event_type"] == "on_ball_engagement"),
                "pressing": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "pressing")
                ),
                "pressing_in_high_block": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "pressing")
                    & (self.df["team_out_of_possession_phase_type"] == "high_block")
                ),
                "pressing_in_medium_block": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "pressing")
                    & (self.df["team_out_of_possession_phase_type"] == "medium_block")
                ),
                "isolated_pressing": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "pressing")
                    & (self.df["n_player_targeted_teammates_within_5m_start"] == 0)
                    & (self.df["n_player_targeted_opponents_within_5m_start"] == 0)
                ),
            },
            "pressure_engagements": {
                "on_ball_engagements": (self.df["event_type"] == "on_ball_engagement"),
                "pressure": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "pressure")
                ),
                "pressure_in_medium_block": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "pressure")
                    & (self.df["team_out_of_possession_phase_type"] == "medium_block")
                ),
                "pressure_in_low_block": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "pressure")
                    & (self.df["team_out_of_possession_phase_type"] == "low_block")
                ),
                "isolated_pressure": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "pressure")
                    & (self.df["n_player_targeted_teammates_within_5m_start"] == 0)
                    & (self.df["n_player_targeted_opponents_within_5m_start"] == 0)
                ),
            },
            "counter_press_engagements": {
                "on_ball_engagements": (self.df["event_type"] == "on_ball_engagement"),
                "counter_press": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "counter_press")
                ),
                "counter_press_in_high_block": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "counter_press")
                    & (self.df["team_out_of_possession_phase_type"] == "high_block")
                ),
                "counter_press_in_medium_block": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "counter_press")
                    & (self.df["team_out_of_possession_phase_type"] == "medium_block")
                ),
                "isolated_counter_press": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "counter_press")
                    & (self.df["n_player_targeted_teammates_within_5m_start"] == 0)
                    & (self.df["n_player_targeted_opponents_within_5m_start"] == 0)
                ),
            },
            "recovery_press_engagements": {
                "on_ball_engagements": (self.df["event_type"] == "on_ball_engagement"),
                "recovery_press": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "recovery_press")
                ),
                "recovery_press_in_high_block": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "recovery_press")
                    & (self.df["team_out_of_possession_phase_type"] == "high_block")
                ),
                "recovery_press_in_medium_block": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "recovery_press")
                    & (self.df["team_out_of_possession_phase_type"] == "medium_block")
                ),
                "recovery_press_in_low_block": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "recovery_press")
                    & (self.df["team_out_of_possession_phase_type"] == "low_block")
                ),
                "recovery_press_in_transition": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "recovery_press")
                    & (
                        self.df["team_out_of_possession_phase_type"].isin(
                            ["defending_transition", "defending_quick_break"]
                        )
                    )
                ),
                "isolated_recovery_press": (
                    (self.df["event_type"] == "on_ball_engagement")
                    & (self.df["event_subtype"] == "recovery_press")
                    & (self.df["n_player_targeted_teammates_within_5m_start"] == 0)
                    & (self.df["n_player_targeted_opponents_within_5m_start"] == 0)
                ),
            },
        }

        return {**default_context_groups, **(custom_context_groups or {})}

    def _define_metric_groups(self, custom_metric_groups):
        """
        Define shared metrics for each aggregation type.

        Args:
            custom_metric_groups (dict, optional): Additional user-defined metric groups.

        Returns:
            dict: A dictionary where keys are group names, and values are shared metric functions.
        """
        default_metric_groups = {
            "off_ball_runs": {
                "count": lambda x: len(x),
                "count_targeted": lambda x: len(x[x["targeted"] == True]),
                "count_received": lambda x: len(
                    x[(x["targeted"] == True) & (x["received"] == True)]
                ),
                "xthreat": lambda x: x["xthreat"].sum(),
                "xthreat_targeted": lambda x: x[x["targeted"] == True]["xthreat"].sum(),
                "xthreat_received": lambda x: x[
                    (x["targeted"] == True) & (x["received"] == True)
                ]["xthreat"].sum(),
                "xpass_completion": lambda x: x["xpass_completion"].sum(),
                "xpass_completion_targeted": lambda x: x[x["targeted"] == True][
                    "xpass_completion"
                ].sum(),
                "xpass_completion_received": lambda x: x[
                    (x["targeted"] == True) & (x["received"] == True)
                ]["xpass_completion"].sum(),
                "count_dangerous": lambda x: len(x[x["dangerous"] == True]),
                "count_dangerous_targeted": lambda x: len(
                    x[(x["targeted"] == True) & (x["dangerous"] == True)]
                ),
                "count_dangerous_received": lambda x: len(
                    x[
                        (x["targeted"] == True)
                        & (x["received"] == True)
                        & (x["dangerous"] == True)
                    ]
                ),
                "count_difficult": lambda x: len(x[x["difficult_pass_target"] == True]),
                "count_difficult_targeted": lambda x: len(
                    x[(x["targeted"] == True) & (x["difficult_pass_target"] == True)]
                ),
                "count_difficult_received": lambda x: len(
                    x[
                        (x["targeted"] == True)
                        & (x["received"] == True)
                        & (x["difficult_pass_target"] == True)
                    ]
                ),
                "avg_speed_avg": lambda x: x["speed_avg"].mean(),
                "count_hsr": lambda x: len(x[x["speed_avg_band"] == "hsr"]),
                "count_sprint": lambda x: len(x[x["speed_avg_band"] == "sprinting"]),
                "avg_distance_covered": lambda x: x["distance_covered"].mean(),
                "count_center_channel": lambda x: len(x[x["channel_end"] == "center"]),
                "count_wide_channel": lambda x: len(
                    x[x["channel_end"].isin(["wide_right", "wide_left"])]
                ),
            },
            "line_breaking_options": {
                "count": lambda x: len(x),
                "count_targeted": lambda x: len(x[x["targeted"] == True]),
                "count_received": lambda x: len(
                    x[(x["targeted"] == True) & (x["received"] == True)]
                ),
                "xthreat": lambda x: x["xthreat"].sum(),
                "xthreat_targeted": lambda x: x[x["targeted"] == True]["xthreat"].sum(),
                "xthreat_received": lambda x: x[
                    (x["targeted"] == True) & (x["received"] == True)
                ]["xthreat"].sum(),
                "xpass_completion": lambda x: x["xpass_completion"].sum(),
                "xpass_completion_targeted": lambda x: x[x["targeted"] == True][
                    "xpass_completion"
                ].sum(),
                "xpass_completion_received": lambda x: x[
                    (x["targeted"] == True) & (x["received"] == True)
                ]["xpass_completion"].sum(),
                "count_dangerous": lambda x: len(x[x["dangerous"] == True]),
                "count_dangerous_targeted": lambda x: len(
                    x[(x["targeted"] == True) & (x["dangerous"] == True)]
                ),
                "count_dangerous_received": lambda x: len(
                    x[
                        (x["targeted"] == True)
                        & (x["received"] == True)
                        & (x["dangerous"] == True)
                    ]
                ),
                "count_difficult": lambda x: len(x[x["difficult_pass_target"] == True]),
                "count_difficult_targeted": lambda x: len(
                    x[(x["targeted"] == True) & (x["difficult_pass_target"] == True)]
                ),
                "count_difficult_received": lambda x: len(
                    x[
                        (x["targeted"] == True)
                        & (x["received"] == True)
                        & (x["difficult_pass_target"] == True)
                    ]
                ),
                "count_center_channel": lambda x: len(x[x["channel_end"] == "center"]),
                "count_wide_channel": lambda x: len(
                    x[x["channel_end"].isin(["wide_right", "wide_left"])]
                ),
            },
            "passes_to_off_ball_runs": {
                "count_options_by_teammates": lambda x: len(x),
                "count_pass_opportunities": lambda x: count_pass_opportunities(x),
                "count_pass_attempts": lambda x: len(x[x["targeted"] == True]),
                "count_completed_passes": lambda x: len(
                    x[(x["targeted"] == True) & (x["received"] == True)]
                ),
                "xthreat_pass_opportunities": lambda x: metric_sum_pass_opportunities(
                    x, "xthreat"
                ),
                "xthreat_pass_attempts": lambda x: x[x["targeted"] == True][
                    "xthreat"
                ].sum(),
                "xthreat_completed_passes": lambda x: x[
                    (x["targeted"] == True) & (x["received"] == True)
                ]["xthreat"].sum(),
                "xpass_completion_pass_opportunities": lambda x: metric_sum_pass_opportunities(
                    x, "xpass_completion"
                ),
                "xpass_completion_pass_attempts": lambda x: x[x["targeted"] == True][
                    "xpass_completion"
                ].sum(),
                "xpass_completion_completed_passes": lambda x: x[
                    (x["targeted"] == True) & (x["received"] == True)
                ]["xpass_completion"].sum(),
                "count_dangerous_pass_opportunities": lambda x: count_pass_opportunities(
                    x[x["dangerous"] == True]
                ),
                "count_dangerous_pass_attempts": lambda x: len(
                    x[(x["targeted"] == True) & (x["dangerous"] == True)]
                ),
                "count_dangerous_completed_passes": lambda x: len(
                    x[
                        (x["targeted"] == True)
                        & (x["received"] == True)
                        & (x["dangerous"] == True)
                    ]
                ),
                "count_difficult_pass_opportunities": lambda x: count_pass_opportunities(
                    x[x["difficult_pass_target"] == True]
                ),
                "count_difficult_pass_attempts": lambda x: len(
                    x[(x["targeted"] == True) & (x["difficult_pass_target"] == True)]
                ),
                "count_difficult_completed_passes": lambda x: len(
                    x[
                        (x["targeted"] == True)
                        & (x["received"] == True)
                        & (x["difficult_pass_target"] == True)
                    ]
                ),
            },
            "line_breaking_passes": {
                "count_options_by_teammates": lambda x: len(x),
                "count_pass_opportunities": lambda x: count_pass_opportunities(x),
                "count_pass_attempts": lambda x: len(x[x["targeted"] == True]),
                "count_completed_passes": lambda x: len(
                    x[(x["targeted"] == True) & (x["received"] == True)]
                ),
                "xthreat_pass_opportunities": lambda x: metric_sum_pass_opportunities(
                    x, "xthreat"
                ),
                "xthreat_pass_attempts": lambda x: x[x["targeted"] == True][
                    "xthreat"
                ].sum(),
                "xthreat_completed_passes": lambda x: x[
                    (x["targeted"] == True) & (x["received"] == True)
                ]["xthreat"].sum(),
                "xpass_completion_pass_opportunities": lambda x: metric_sum_pass_opportunities(
                    x, "xpass_completion"
                ),
                "xpass_completion_pass_attempts": lambda x: x[x["targeted"] == True][
                    "xpass_completion"
                ].sum(),
                "xpass_completion_completed_passes": lambda x: x[
                    (x["targeted"] == True) & (x["received"] == True)
                ]["xpass_completion"].sum(),
                "count_dangerous_pass_opportunities": lambda x: count_pass_opportunities(
                    x[x["dangerous"] == True]
                ),
                "count_dangerous_pass_attempts": lambda x: len(
                    x[(x["targeted"] == True) & (x["dangerous"] == True)]
                ),
                "count_dangerous_completed_passes": lambda x: len(
                    x[
                        (x["targeted"] == True)
                        & (x["received"] == True)
                        & (x["dangerous"] == True)
                    ]
                ),
                "count_difficult_pass_opportunities": lambda x: count_pass_opportunities(
                    x[x["difficult_pass_target"] == True]
                ),
                "count_difficult_pass_attempts": lambda x: len(
                    x[(x["targeted"] == True) & (x["difficult_pass_target"] == True)]
                ),
                "count_difficult_completed_passes": lambda x: len(
                    x[
                        (x["targeted"] == True)
                        & (x["received"] == True)
                        & (x["difficult_pass_target"] == True)
                    ]
                ),
            },
            "possessions": {
                "count": lambda x: len(x),
                "count_one_touch_passes": lambda x: len(
                    x[(x["one_touch"] == True) & (x["end_type"] == "pass")]
                ),
                "quick_passes": lambda x: len(x[(x["quick_pass"] == True)]),
                "received_in_tight_space": lambda x: len(
                    x[(x["separation_start"] <= 2)]
                ),
                "received_in_open_space": lambda x: len(
                    x[(x["separation_start"] >= 6)]
                ),
                "8m_carry": lambda x: len(
                    x[(x["carry"] == True) & (x["distance_covered"] >= 8)]
                ),
                "8m_carry_at_speed": lambda x: len(
                    x[
                        (x["carry"] == True)
                        & (x["distance_covered"] >= 8)
                        & (x["speed_avg"] >= 15)
                    ]
                ),
                "forward_momentum": lambda x: len(x[(x["forward_momentum"] == True)]),
            },
            "on_ball_engagements": {
                "count": lambda x: len(x),
                "count_direct_disruption": lambda x: len(
                    x[(x["end_type"] == "direct_disruption")]
                ),
                "count_direct_regain": lambda x: len(
                    x[(x["end_type"] == "direct_regain")]
                ),
                "count_indirect_disruption": lambda x: len(
                    x[(x["end_type"] == "indirect_disruption")]
                ),
                "count_indirect_regain": lambda x: len(
                    x[(x["end_type"] == "indirect_regain")]
                ),
                "avg_speed_difference": lambda x: x["speed_difference"].mean(),
                "count_goal_side_end": lambda x: len(x[(x["goal_side_end"] == True)]),
                "count_not_goal_side_start": lambda x: len(
                    x[(x["goal_side_start"] == False)]
                ),
                "count_got_goal_side": lambda x: len(
                    x[(x["goal_side_end"] == True) & (x["goal_side_start"] == False)]
                ),
                "count_got_close": lambda x: len(
                    x[
                        (x["interplayer_distance_end"] <= 1.5)
                        & (x["interplayer_distance_start"] >= 3)
                    ]
                ),
                "count_start_close": lambda x: len(
                    x[(x["close_at_player_possession_start"] == True)]
                ),
                "count_beaten_by_possession": lambda x: len(
                    x[(x["beaten_by_possession"] == True)]
                ),
                "count_beaten_by_movement": lambda x: len(
                    x[(x["beaten_by_movement"] == True)]
                ),
                "count_affected_line_break": lambda x: len(
                    x[(x["affected_line_break_id"].isna() == False)]
                ),
                "count_possession_danger": lambda x: len(
                    x[(x["possession_danger"] == True)]
                ),
                "count_stop_possession_danger": lambda x: len(
                    x[(x["stop_possession_danger"] == True)]
                ),
                "count_reduce_possession_danger": lambda x: len(
                    x[(x["reduce_possession_danger"] == True)]
                ),
                "count_force_backward": lambda x: len(x[(x["force_backward"] == True)]),
                "count_above_hsr": lambda x: len(x[(x["speed_avg"] >= 20)]),
                "count_consecutive": lambda x: len(
                    x[(x["consecutive_on_ball_engagements"] == True)]
                ),
                "count_pressing_chain": lambda x: len(x[(x["pressing_chain"] == True)]),
                "count_trajectory_forward": lambda x: len(
                    x[(x["trajectory_direction"] == "forward")]
                ),
            },
            "pressing_engagements": {
                "count": lambda x: len(x),
                "count_direct_disruption": lambda x: len(
                    x[(x["end_type"] == "direct_disruption")]
                ),
                "count_direct_regain": lambda x: len(
                    x[(x["end_type"] == "direct_regain")]
                ),
                "count_indirect_disruption": lambda x: len(
                    x[(x["end_type"] == "indirect_disruption")]
                ),
                "count_indirect_regain": lambda x: len(
                    x[(x["end_type"] == "indirect_regain")]
                ),
                "avg_speed_difference": lambda x: x["speed_difference"].mean(),
                "count_goal_side_end": lambda x: len(x[(x["goal_side_end"] == True)]),
                "count_got_goal_side": lambda x: len(
                    x[(x["goal_side_end"] == True) & (x["goal_side_start"] == False)]
                ),
                "count_got_close": lambda x: len(
                    x[
                        (x["interplayer_distance_end"] <= 1.5)
                        & (x["interplayer_distance_start"] >= 3)
                    ]
                ),
                "count_start_close": lambda x: len(
                    x[(x["close_at_player_possession_start"] == True)]
                ),
                "count_beaten_by_possession": lambda x: len(
                    x[(x["beaten_by_possession"] == True)]
                ),
                "count_beaten_by_movement": lambda x: len(
                    x[(x["beaten_by_movement"] == True)]
                ),
                "count_affected_line_break": lambda x: len(
                    x[(x["affected_line_break_id"].isna() == False)]
                ),
                "count_stop_possession_danger": lambda x: len(
                    x[(x["stop_possession_danger"] == True)]
                ),
                "count_reduce_possession_danger": lambda x: len(
                    x[(x["reduce_possession_danger"] == True)]
                ),
                "count_force_backward": lambda x: len(x[(x["force_backward"] == True)]),
                "count_above_hsr": lambda x: len(x[(x["speed_avg"] >= 20)]),
                "count_consecutive": lambda x: len(
                    x[(x["consecutive_on_ball_engagements"] == True)]
                ),
                "count_trajectory_forward": lambda x: len(
                    x[(x["trajectory_direction"] == "forward")]
                ),
            },
            "pressure_engagements": {
                "count": lambda x: len(x),
                "count_direct_disruption": lambda x: len(
                    x[(x["end_type"] == "direct_disruption")]
                ),
                "count_direct_regain": lambda x: len(
                    x[(x["end_type"] == "direct_regain")]
                ),
                "count_indirect_disruption": lambda x: len(
                    x[(x["end_type"] == "indirect_disruption")]
                ),
                "count_indirect_regain": lambda x: len(
                    x[(x["end_type"] == "indirect_regain")]
                ),
                "avg_speed_difference": lambda x: x["speed_difference"].mean(),
                "count_goal_side_end": lambda x: len(x[(x["goal_side_end"] == True)]),
                "count_got_goal_side": lambda x: len(
                    x[(x["goal_side_end"] == True) & (x["goal_side_start"] == False)]
                ),
                "count_got_close": lambda x: len(
                    x[
                        (x["interplayer_distance_end"] <= 1.5)
                        & (x["interplayer_distance_start"] >= 3)
                    ]
                ),
                "count_start_close": lambda x: len(
                    x[(x["close_at_player_possession_start"] == True)]
                ),
                "count_beaten_by_possession": lambda x: len(
                    x[(x["beaten_by_possession"] == True)]
                ),
                "count_beaten_by_movement": lambda x: len(
                    x[(x["beaten_by_movement"] == True)]
                ),
                "count_affected_line_break": lambda x: len(
                    x[(x["affected_line_break_id"].isna() == False)]
                ),
                "count_stop_possession_danger": lambda x: len(
                    x[(x["stop_possession_danger"] == True)]
                ),
                "count_reduce_possession_danger": lambda x: len(
                    x[(x["reduce_possession_danger"] == True)]
                ),
                "count_force_backward": lambda x: len(x[(x["force_backward"] == True)]),
                "count_above_hsr": lambda x: len(x[(x["speed_avg"] >= 20)]),
                "count_consecutive": lambda x: len(
                    x[(x["consecutive_on_ball_engagements"] == True)]
                ),
                "count_trajectory_forward": lambda x: len(
                    x[(x["trajectory_direction"] == "forward")]
                ),
            },
            "counter_press_engagements": {
                "count": lambda x: len(x),
                "count_direct_disruption": lambda x: len(
                    x[(x["end_type"] == "direct_disruption")]
                ),
                "count_direct_regain": lambda x: len(
                    x[(x["end_type"] == "direct_regain")]
                ),
                "count_indirect_disruption": lambda x: len(
                    x[(x["end_type"] == "indirect_disruption")]
                ),
                "count_indirect_regain": lambda x: len(
                    x[(x["end_type"] == "indirect_regain")]
                ),
                "avg_speed_difference": lambda x: x["speed_difference"].mean(),
                "count_goal_side_end": lambda x: len(x[(x["goal_side_end"] == True)]),
                "count_got_goal_side": lambda x: len(
                    x[(x["goal_side_end"] == True) & (x["goal_side_start"] == False)]
                ),
                "count_got_close": lambda x: len(
                    x[
                        (x["interplayer_distance_end"] <= 1.5)
                        & (x["interplayer_distance_start"] >= 3)
                    ]
                ),
                "count_start_close": lambda x: len(
                    x[(x["close_at_player_possession_start"] == True)]
                ),
                "count_beaten_by_possession": lambda x: len(
                    x[(x["beaten_by_possession"] == True)]
                ),
                "count_beaten_by_movement": lambda x: len(
                    x[(x["beaten_by_movement"] == True)]
                ),
                "count_affected_line_break": lambda x: len(
                    x[(x["affected_line_break_id"].isna() == False)]
                ),
                "count_stop_possession_danger": lambda x: len(
                    x[(x["stop_possession_danger"] == True)]
                ),
                "count_reduce_possession_danger": lambda x: len(
                    x[(x["reduce_possession_danger"] == True)]
                ),
                "count_force_backward": lambda x: len(x[(x["force_backward"] == True)]),
                "count_above_hsr": lambda x: len(x[(x["speed_avg"] >= 20)]),
                "count_consecutive": lambda x: len(
                    x[(x["consecutive_on_ball_engagements"] == True)]
                ),
                "count_trajectory_forward": lambda x: len(
                    x[(x["trajectory_direction"] == "forward")]
                ),
            },
            "recovery_press_engagements": {
                "count": lambda x: len(x),
                "count_direct_disruption": lambda x: len(
                    x[(x["end_type"] == "direct_disruption")]
                ),
                "count_direct_regain": lambda x: len(
                    x[(x["end_type"] == "direct_regain")]
                ),
                "count_indirect_disruption": lambda x: len(
                    x[(x["end_type"] == "indirect_disruption")]
                ),
                "count_indirect_regain": lambda x: len(
                    x[(x["end_type"] == "indirect_regain")]
                ),
                "avg_speed_difference": lambda x: x["speed_difference"].mean(),
                "count_goal_side_end": lambda x: len(x[(x["goal_side_end"] == True)]),
                "count_got_goal_side": lambda x: len(
                    x[(x["goal_side_end"] == True) & (x["goal_side_start"] == False)]
                ),
                "count_got_close": lambda x: len(
                    x[
                        (x["interplayer_distance_end"] <= 1.5)
                        & (x["interplayer_distance_start"] >= 3)
                    ]
                ),
                "count_start_close": lambda x: len(
                    x[(x["close_at_player_possession_start"] == True)]
                ),
                "count_beaten_by_possession": lambda x: len(
                    x[(x["beaten_by_possession"] == True)]
                ),
                "count_beaten_by_movement": lambda x: len(
                    x[(x["beaten_by_movement"] == True)]
                ),
                "count_affected_line_break": lambda x: len(
                    x[(x["affected_line_break_id"].isna() == False)]
                ),
                "count_stop_possession_danger": lambda x: len(
                    x[(x["stop_possession_danger"] == True)]
                ),
                "count_reduce_possession_danger": lambda x: len(
                    x[(x["reduce_possession_danger"] == True)]
                ),
                "count_force_backward": lambda x: len(x[(x["force_backward"] == True)]),
                "count_above_hsr": lambda x: len(x[(x["speed_avg"] >= 20)]),
                "count_consecutive": lambda x: len(
                    x[(x["consecutive_on_ball_engagements"] == True)]
                ),
                "avg_distance_covered": lambda x: x["distance_covered"].mean(),
            },
        }
        return {**default_metric_groups, **(custom_metric_groups or {})}

    def generate_aggregates(self, group_by, aggregate_type):
        """
        Generate aggregated event statistics based on the specified context and metric group.

        Args:
            group_by (list of str): Columns to group data by (e.g., ['player_id', 'player_name', 'context']).
            aggregate_type (str): The type of aggregation (e.g., 'option', 'passing').

        Returns:
            pd.DataFrame: Aggregated statistics for the specified type.
        """
        if aggregate_type not in self.context_groups:
            raise ValueError(
                f"Invalid aggregate_type '{aggregate_type}'. Choose from {list(self.context_groups.keys())}"
            )

        contexts = self.context_groups[aggregate_type]
        metrics = self.metric_groups.get(aggregate_type, {})

        context_df_list = []

        for name, condition in contexts.items():
            subset = self.df[condition].copy()
            subset["context"] = name
            context_df_list.append(subset)

        if not context_df_list:
            return pd.DataFrame()

        context_df = pd.concat(context_df_list, ignore_index=True)

        # Apply shared metrics across all contexts in the group
        aggregated_df = (
            context_df.groupby(group_by + ["context"])
            .apply(
                lambda x: pd.Series(
                    {metric_name: func(x) for metric_name, func in metrics.items()}
                )
            )
            .reset_index()
        )

        aggregated_df = aggregated_df.set_index(group_by + ["context"]).unstack(
            ["context"]
        )
        aggregated_df.columns = ["{}_{}".format(m, c) for m, c in aggregated_df.columns]
        aggregated_df = aggregated_df.reset_index()

        metric_columns = []
        for context in contexts.keys():
            for metric in metrics.keys():
                if "{}_{}".format(metric, context) not in aggregated_df.columns:
                    aggregated_df[metric + "_" + context] = np.nan
                metric_columns.append(metric + "_" + context)

        aggregated_df = aggregated_df[group_by + metric_columns]

        return aggregated_df
