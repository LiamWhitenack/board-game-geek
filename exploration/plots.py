from collections.abc import Iterable
from math import sqrt
from pathlib import Path
from typing import Iterable

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.pylab import savefig, subplots, tight_layout
from matplotlib.pyplot import savefig, subplots, tight_layout
from numpy import histogram_bin_edges, linspace, mean
from pandas import Series

from exploration.themes import EARTH

# Example EARTH theme colors (replace with your actual palette)
EARTH = {
    "accent": "#7f6d5f",  # bar color
    "zero": "#000000",  # edge color
}


# --------------------------------------------------
# Reusable barchart function
# --------------------------------------------------
def barchart(
    x,
    y,
    figsize: tuple[int, int] = (8, 5),
    filename: str = "barchart",
    x_label: str | None = None,
    y_label: str = "Value",
) -> None:

    fig, ax = subplots(figsize=figsize)

    # Use EARTH accent for bars (minimal, clean)
    ax.bar(
        x,
        y,
        color=EARTH["accent"],
        edgecolor=EARTH["zero"],
        linewidth=0.8,
    )

    # --- Minimal styling ---
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if x_label is not None:
        ax.set_xlabel(x_label)

    ax.set_ylabel(y_label)

    # --- Title from filename ---
    clean_name = Path(filename).stem
    title = clean_name.replace("_", " ").replace("-", " ").title()
    # ax.set_title(title, pad=12)

    tight_layout()
    savefig(f"exploration/plots/{clean_name}.png")
    plt.close()


def set_fixed_axis_geometry(axis):
    """
    Force identical axis drawing area across plots.
    Values are [left, bottom, width, height] in figure fraction.
    """
    axis.set_position([0.45, 0.12, 0.62, 0.78])


def barchart(
    x,
    y,
    figsize: tuple[int, int] = (8, 5),
    filename: str = "barchart",
    x_label: str | None = None,
    y_label: str = "Value",
) -> None:

    fig, ax = subplots(figsize=figsize)

    # Use EARTH accent for bars (minimal, clean)
    ax.bar(
        x,
        y,
        color=EARTH["accent"],
        edgecolor=EARTH["zero"],
        linewidth=0.8,
    )

    # --- Minimal styling ---
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if x_label is not None:
        ax.set_xlabel(x_label)

    ax.set_ylabel(y_label)

    # --- Title from filename ---
    clean_name = Path(filename).stem
    title = clean_name.replace("_", " ").replace("-", " ").title()
    # ax.set_title(title, pad=12)

    tight_layout()
    savefig(f"exploration/plots/{clean_name}.png")


def histogram(
    bins: int = 30,
    density: bool = True,
    alpha: float = 0.55,
    figsize: tuple[int, int] = (8, 5),
    filename: str = "histogram",
    x_min: float | None = None,
    **data: dict[str, Iterable[float]],
) -> None:

    if not data:
        raise ValueError("Provide at least one dataset via keyword arguments.")

    fig, ax = subplots(figsize=figsize)

    if x_min is not None:
        ax.set_xlim(left=x_min, right=2025)

    palette = [
        EARTH["density"],
        EARTH["line"],
        EARTH["accent"],
        "#B08968",
        "#588157",
        "#7F5539",
    ]

    combined: list[float] = []
    for values in data.values():
        combined.extend(values)

    edges = histogram_bin_edges(combined, bins=bins)

    for index, (label, values) in enumerate(data.items()):
        color = palette[index % len(palette)]

        ax.hist(
            values,
            bins=edges,
            density=density,
            alpha=alpha,
            color=color,
            edgecolor=EARTH["zero"],
            linewidth=0.8,
            label=label.replace("_", " ").title(),
        )

    # --- Minimal styling ---
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.axvline(0, color=EARTH["zero"], linewidth=1, linestyle="--")

    ax.set_ylabel("Density" if density else "Count")
    ax.legend(frameon=False)

    # --- Make filename the title ---
    clean_name = Path(filename).stem  # remove extension if provided
    title = clean_name.replace("_", " ").replace("-", " ").title()
    # ax.set_title(title, pad=12)

    tight_layout()
    savefig(f"exploration/plots/{clean_name}.png")


def stacked_ci_barchart(
    filename: str,
    means: Series,
    lower_bounds: Series,
    upper_bounds: Series,
    x_label: str = "Rating",
    x_limits: tuple[float, float] | None = None,
):
    lower_bounds = lower_bounds.loc[means.index]
    upper_bounds = upper_bounds.loc[means.index]

    lower_segment = lower_bounds
    middle_segment = means - lower_bounds
    upper_segment = upper_bounds - means

    figure, axis = plt.subplots(figsize=(18, 9))

    axis.barh(means.index, lower_segment, color=EARTH["accent"])
    axis.barh(
        means.index,
        middle_segment,
        left=lower_segment,
        color=EARTH["line"],
        label="Lower CI",
    )
    axis.barh(
        means.index,
        upper_segment,
        left=lower_segment + middle_segment,
        color=EARTH["density"],
        label="Upper CI",
    )

    if x_limits is not None:
        axis.set_xlim(x_limits)

    # axis.set_title(filename.replace("-", " ").replace("_", " "), pad=12)
    axis.set_xlabel(x_label)

    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.grid(axis="x", alpha=0.2)

    axis.legend(frameon=False, loc="center left", bbox_to_anchor=(1, 0.5))

    set_fixed_axis_geometry(axis)
    plt.subplots_adjust(left=0.35)
    plt.savefig(f"exploration/plots/{filename}.png", dpi=300)
    plt.close()


def stacked_ci_barchart_with_current(
    filename: str,
    means: Series,
    lower_bounds: Series,
    upper_bounds: Series,
    current_means: Series,
    x_label: str = "Rating",
    x_limits: tuple[float, float] | None = None,
):
    lower_bounds = lower_bounds.loc[means.index]
    upper_bounds = upper_bounds.loc[means.index]
    current_means = current_means.loc[means.index]

    lower_segment = lower_bounds
    middle_segment = means - lower_bounds
    upper_segment = upper_bounds - means

    figure, axis = plt.subplots(figsize=(18, 9))

    axis.barh(means.index, lower_segment, color=EARTH["accent"])
    axis.barh(
        means.index,
        middle_segment,
        left=lower_segment,
        color=EARTH["line"],
        label="Lower CI",
    )
    axis.barh(
        means.index,
        upper_segment,
        left=lower_segment + middle_segment,
        color=EARTH["density"],
        label="Upper CI",
    )

    axis.scatter(
        current_means,
        means.index,
        color=EARTH["zero"],
        marker="D",
        s=40,
        label="Current Mean",
        zorder=5,
    )

    if x_limits is not None:
        axis.set_xlim(x_limits)

    # axis.set_title(filename.replace("-", " ").replace("_", " "), pad=12)
    axis.set_xlabel(x_label)

    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.grid(axis="x", alpha=0.2)

    axis.legend(frameon=False, loc="center left", bbox_to_anchor=(1, 0.5))

    set_fixed_axis_geometry(axis)
    plt.subplots_adjust(left=0.30)
    plt.savefig(f"exploration/plots/{filename}.png", dpi=300)
    plt.close()
