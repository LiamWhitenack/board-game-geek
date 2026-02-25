import re

import numpy as np
from pandas import DataFrame, isna


def add_player_group_features(df: DataFrame, column: str) -> DataFrame:
    """
    Convert recommendation strings into generalized group columns.

    Creates:
        - recommended_for_solo (1)
        - recommended_for_duo (2)
        - recommended_for_small_group (3-4)
        - recommended_for_large_group (5-8)
        - recommended_for_very_large_group (9+)
        - recommended_for_even
        - recommended_for_odd
        - recommended_for_valid
    """

    group_cols = [
        "recommended_for_solo",
        "recommended_for_duo",
        "recommended_for_small_group",
        "recommended_for_large_group",
        "recommended_for_very_large_group",
        "recommended_for_even",
        "recommended_for_odd",
    ]

    for col in group_cols:
        df[col] = 0

    df["recommended_for_valid"] = 1

    def extract_players(text):
        if isna(text):
            return None

        text = str(text)

        if text in {"(Undetermined)", "(no votes)"}:
            return None

        numbers = set()

        # Ranges first (to avoid double counting)
        for start, end in re.findall(r"(\d+)[–-](\d+)", text):
            numbers.update(range(int(start), int(end) + 1))

        # Open-ended 4+
        for n in re.findall(r"(\d+)\+", text):
            numbers.update(range(int(n), 100))

        # Exact numbers
        numbers.update(int(n) for n in re.findall(r"\b\d+\b", text))

        return numbers if numbers else None

    for idx, value in df[column].items():
        players = extract_players(value)

        if players is None:
            df.at[idx, "recommended_for_valid"] = 0
            continue

        # ---- Group buckets ----
        if 1 in players:
            df.at[idx, "recommended_for_solo"] = 1

        if 2 in players:
            df.at[idx, "recommended_for_duo"] = 1

        if any(p in players for p in [3, 4]):
            df.at[idx, "recommended_for_small_group"] = 1

        if any(p in players for p in [5, 6, 7, 8]):
            df.at[idx, "recommended_for_large_group"] = 1

        if any(p >= 9 for p in players):
            df.at[idx, "recommended_for_very_large_group"] = 1

        # ---- Even / Odd (ONLY if at least 2 valid counts) ----
        if len(players) >= 2:
            if any(p % 2 == 0 for p in players):
                df.at[idx, "recommended_for_even"] = 1

            if any(p % 2 == 1 for p in players):
                df.at[idx, "recommended_for_odd"] = 1

    return df


def add_best_player_count_features(
    df: DataFrame,
    column: str,
) -> DataFrame:
    """
    Convert recommendation strings into generalized group columns.

    Creates:
        - best_player_count_solo (1)
        - best_player_count_duo (2)
        - best_player_count_small_group (3-4)
        - best_player_count_large_group (5-8)
        - best_player_count_very_large_group (9+)
        - best_player_count_even
        - best_player_count_odd
        - best_player_count_valid
    """

    # Initialize columns
    group_cols = [
        "best_player_count_solo",
        "best_player_count_duo",
        "best_player_count_small_group",
        "best_player_count_large_group",
        "best_player_count_very_large_group",
    ]

    for col in group_cols:
        df[col] = 0

    df["best_player_count_valid"] = 1

    def extract_players(text):
        if isna(text):
            return None

        text = str(text)

        if text in {"(Undetermined)", "(no votes)"}:
            return None

        numbers = set()

        # Exact numbers
        numbers.update(int(n) for n in re.findall(r"\b\d+\b", text))

        # Ranges 3–6
        for start, end in re.findall(r"(\d+)[–-](\d+)", text):
            numbers.update(range(int(start), int(end) + 1))

        # Open-ended 4+
        for n in re.findall(r"(\d+)\+", text):
            numbers.update(range(int(n), 101))

        return numbers if numbers else None

    for idx, value in df[column].items():
        players = extract_players(value)

        if players is None:
            df.at[idx, "best_player_count_valid"] = 0
            continue

        # Assign group flags
        if 1 in players:
            df.at[idx, "best_player_count_solo"] = 1

        if 2 in players:
            df.at[idx, "best_player_count_duo"] = 1

        if any(p in players for p in [3, 4]):
            df.at[idx, "best_player_count_small_group"] = 1

        if any(p in players for p in [5, 6, 7, 8]):
            df.at[idx, "best_player_count_large_group"] = 1

        if any(p >= 9 for p in players):
            df.at[idx, "best_player_count_very_large_group"] = 1

    return df


def decode_language_dependence(long_text: str) -> int:
    return [
        "Extensive use of text - massive conversion needed to be playable",
        "Moderate in-game text - needs crib sheet or paste ups",
        "No necessary in-game text",
        "Some necessary text - easily memorized or small crib sheet",
        "Unplayable in another language",
    ].index(long_text)
