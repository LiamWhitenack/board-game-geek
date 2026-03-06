import numpy as np
import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt
from pandas import Series, read_csv
from sqlalchemy import and_, select

from exploration.plots import (
    barchart,
    histogram,
    stacked_ci_barchart,
    stacked_ci_barchart_with_current,
)
from exploration.utils import add_player_group_features, decode_language_dependence
from sql.game import Game
from sql.session import session

games = (
    session.execute(
        select(Game).where(
            and_(
                Game.bayesaverage > 0.1,
                Game.averageweight > 0.0,
                Game.rank_all.is_not(None),
            )
        )
    )
    .scalars()
    .all()
)

games_2025 = [game for game in games if game.year_published == 2025]
df_all = pd.DataFrame([g.__dict__ for g in games]).set_index("name")
df_2025 = df_all[df_all["year_published"] == 2025]
df_others = df_all[df_all["year_published"] != 2025]
df_2000 = df_all[(df_all["year_published"] > 2000) & (df_all["year_published"] < 2026)]

top_games = sorted(games, key=lambda g: g.rank_all)[:25]

data = [(g.average, *g.confidence_interval_t()) for g in reversed(top_games)]

index = [f"{g.name} ({g.rank_all})" for g in reversed(top_games)]

mean, mean_lower_ci, mean_upper_ci = (
    Series(values, index=index) for values in zip(*data)
)
stacked_ci_barchart(
    "Top-25-Games-Ratings-Confidence-Interval",
    means=mean,
    lower_bounds=mean_lower_ci,
    upper_bounds=mean_upper_ci,
)
top_games = sorted(games_2025, key=lambda g: g.rank_all)[:25]

data = [(g.average, *g.confidence_interval_t()) for g in reversed(top_games)]

index = {g.name: f"{g.name} ({i})" for i, g in enumerate(top_games, start=1)}

mean, mean_lower_ci, mean_upper_ci = (
    Series(values, index=list(reversed(index.values()))) for values in zip(*data)
)
stacked_ci_barchart(
    "Top-25-Games-of-2025-Ratings-Confidence-Interval",
    means=mean,
    lower_bounds=mean_lower_ci,
    upper_bounds=mean_upper_ci,
    x_limits=(0, 10),
)
temp = read_csv("boardgames_ranks-2026-03-04.csv", index_col="id")
print(
    len(
        [
            None
            for g in games_2025
            if g.confidence_interval_t()[0]
            <= temp["average"][g.id]
            <= g.confidence_interval_t()[1]
        ]
    ),
    len(games_2025),
)

temp = temp[temp["rank"] < 10000]
updated_ranks = temp.set_index("name")["average"].to_dict()
stacked_ci_barchart_with_current(
    "Top-25-Games-of-2025-Ratings-Confidence-Interval-Updated",
    means=mean,
    lower_bounds=mean_lower_ci,
    upper_bounds=mean_upper_ci,
    current_means=Series(
        {
            index[k]: v
            for k, v in updated_ranks.items()
            if k in {g.name for g in top_games}
        }
    ),
    x_limits=(0, 10),
)
histogram(
    years_published=[year for year in df_all["year_published"] if year > 2000],
    filename="Board-Games-Published-Per-Year-(Since-2000)",
    bins=25,
    x_min=2001,
)
barchart(
    y_label="Mean Ratings",
    x_label="Year",
    y=df_2000[["year_published", "average"]]
    .groupby("year_published")
    .mean()["average"],
    x=df_2000[["year_published", "average"]].groupby("year_published").mean().index,
    filename="Mean-Rating-By-Year-(Since-2000)",
)
histogram(
    games_from_2025=df_2025["average"].to_list(),
    other_years=df_all["average"].to_list(),
    filename="2025-Ratings-Histogram",
)
