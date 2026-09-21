"""
Name:    Alex Crenshaw
Class:   INF601 - Advanced Programming in Python
Project: Mini Project 3 - Movie Ratings by Genre

Question: How does movie rating vary by genre, and has any genre's
average rating trended up or down by decade since the 1970s?

Fetches a sample of movies from the Practice Hub API, loads it into a
Pandas DataFrame, and plots a box plot of rating-by-genre alongside a
decade-by-decade trend line per genre. Saves the figure as a PNG in
charts/.
"""

import os

import pandas as pd
import requests
import matplotlib.pyplot as plt

API_BASE = "https://practice.fhsucyber.com"
API_TOKEN = os.environ.get("PRACTICE_API_TOKEN")
SAMPLE_SIZE = 500  # server max per request
CHARTS_DIR = "charts"
CHART_DPI = 170

# Fixed genre -> color mapping (validated categorical palette, first six
# slots) so a genre's color stays the same in both subplots.
GENRE_COLORS = {
    "Action": "#2a78d6",       # blue
    "Comedy": "#eb6834",       # orange
    "Documentary": "#1baf7a",  # aqua
    "Drama": "#eda100",        # yellow
    "Horror": "#e87ba4",       # magenta
    "Sci-Fi": "#008300",       # green
}

CHART_SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"


def fetch_movies(sample_size=SAMPLE_SIZE):
    """Fetch a sample of movies from the Practice Hub API and return the
    raw list of row dicts."""
    if not API_TOKEN:
        raise SystemExit(
            "PRACTICE_API_TOKEN is not set. Set it to your Practice Hub "
            "API token before running this script."
        )

    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {"count": sample_size}
    try:
        resp = requests.get(
            f"{API_BASE}/api/v1/datasets/movies", headers=headers, params=params
        )
        resp.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise SystemExit(f"Could not fetch movie data from the Practice Hub - {err}")

    return resp.json()["rows"]


def build_dataframe(rows):
    """Load the raw rows into a DataFrame and add a `decade` column
    derived from `year`."""
    df = pd.DataFrame(rows)
    df["decade"] = (df["year"] // 10) * 10
    return df


def plot_ratings_by_genre(df):
    """Build a figure with a box plot of rating distribution per genre
    on the left, and a small-multiples grid of one mean-rating-by-decade
    line per genre on the right (small multiples instead of one overlaid
    6-line chart, since 6 crossing lines were hard to trace by color
    alone). Both panels share a reference line at the overall mean
    rating. Saves the figure as a PNG in charts/."""
    genre_order = (
        df.groupby("genre")["rating"].median().sort_values().index.tolist()
    )
    colors = [GENRE_COLORS[g] for g in genre_order]
    genre_counts = df.groupby("genre")["rating"].size()
    overall_mean = df["rating"].mean()

    decade_means = (
        df.groupby(["decade", "genre"])["rating"].mean().unstack("genre")
    )
    decade_means = decade_means[genre_order]
    y_min = min(1, decade_means.min().min() - 0.3)
    y_max = max(10, decade_means.max().max() + 0.3)

    fig = plt.figure(figsize=(15, 7.5))
    fig.patch.set_facecolor(CHART_SURFACE)
    outer = fig.add_gridspec(
        2,
        2,
        width_ratios=[1, 1.4],
        height_ratios=[0.08, 1],
        left=0.06,
        right=0.98,
        top=0.88,
        bottom=0.15,
        wspace=0.28,
        hspace=0.12,
    )

    # --- Left: rating distribution per genre (spans both header + body rows) ---
    ax_box = fig.add_subplot(outer[:, 0])
    ax_box.set_facecolor(CHART_SURFACE)
    box_data = [df.loc[df["genre"] == g, "rating"] for g in genre_order]
    genre_labels = {"Documentary": "Docu."}
    bp = ax_box.boxplot(
        box_data,
        tick_labels=[
            f"{genre_labels.get(g, g)} (n={genre_counts[g]})" for g in genre_order
        ],
        patch_artist=True,
        medianprops={"color": INK_PRIMARY, "linewidth": 1.5},
        whiskerprops={"color": INK_MUTED},
        capprops={"color": INK_MUTED},
        flierprops={"markeredgecolor": INK_MUTED, "markersize": 4},
    )
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)
        patch.set_edgecolor(INK_MUTED)
        patch.set_linewidth(1)

    ax_box.axhline(overall_mean, color=INK_MUTED, linewidth=1, zorder=0)
    ax_box.annotate(
        f"overall mean ({overall_mean:.2f})",
        xy=(0.01, overall_mean),
        xycoords=("axes fraction", "data"),
        xytext=(0, 4),
        textcoords="offset points",
        color=INK_MUTED,
        fontsize=8,
    )

    ax_box.set_title("Rating Distribution by Genre", color=INK_PRIMARY)
    ax_box.set_ylabel("Rating", color=INK_PRIMARY)
    ax_box.tick_params(axis="x", colors=INK_PRIMARY, rotation=20, labelsize=9)
    for label in ax_box.get_xticklabels():
        label.set_ha("right")
    ax_box.tick_params(axis="y", colors=INK_PRIMARY)
    ax_box.grid(axis="y", color=GRIDLINE, zorder=-1)
    ax_box.set_axisbelow(True)
    for spine in ax_box.spines.values():
        spine.set_color(GRIDLINE)

    # --- Right: small multiples, one mean-rating-by-decade line per genre ---
    header_ax = fig.add_subplot(outer[0, 1])
    header_ax.axis("off")
    header_ax.text(
        0.5, 0, "Mean Rating by Decade", color=INK_PRIMARY, fontsize=12, ha="center", va="bottom"
    )

    inner = outer[1, 1].subgridspec(2, 3, wspace=0.2, hspace=0.9)
    decades = decade_means.index
    for i, genre in enumerate(genre_order):
        ax = fig.add_subplot(inner[i // 3, i % 3])
        ax.set_facecolor(CHART_SURFACE)
        ax.axhline(overall_mean, color=INK_MUTED, linewidth=1, zorder=0)
        ax.plot(
            decades,
            decade_means[genre],
            marker="o",
            markersize=4,
            linewidth=2,
            color=GENRE_COLORS[genre],
            zorder=2,
        )
        ax.set_ylim(y_min, y_max)
        ax.set_yticks(range(2, 11, 2))
        ax.set_title(genre, color=INK_PRIMARY, fontsize=10)
        ax.grid(color=GRIDLINE, zorder=-1)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_color(GRIDLINE)

        # Every panel shares the same y-scale (1-10) and shows its own
        # decade (year) labels, so panels can be read and compared
        # independently rather than only via the bottom row/left column.
        ax.tick_params(axis="y", colors=INK_PRIMARY, labelsize=8)
        ax.set_xticks(decades)
        ax.tick_params(axis="x", colors=INK_PRIMARY, labelsize=7, rotation=45)

    fig.suptitle(
        "Movie Ratings by Genre (Practice Hub sample, n={})".format(len(df)),
        color=INK_PRIMARY,
        fontsize=14,
        y=0.97,
    )
    fig.text(
        0.5,
        0.015,
        "No genre or decade holds a consistent edge - ratings swing around "
        "the overall mean ({:.2f}) rather than trending up or down.".format(
            overall_mean
        ),
        color=INK_MUTED,
        fontsize=9,
        ha="center",
    )

    os.makedirs(CHARTS_DIR, exist_ok=True)
    out_path = os.path.join(CHARTS_DIR, "movie_ratings_by_genre.png")
    fig.savefig(out_path, dpi=CHART_DPI, facecolor=fig.get_facecolor())
    plt.close(fig)
    return out_path


def main():
    rows = fetch_movies()
    df = build_dataframe(rows)

    print(f"Fetched {len(df)} movies from the Practice Hub.")
    print("Mean rating by genre:")
    print(df.groupby("genre")["rating"].mean().sort_values(ascending=False).round(2))

    out_path = plot_ratings_by_genre(df)
    print(f"Saved chart to {out_path}")


if __name__ == "__main__":
    main()
