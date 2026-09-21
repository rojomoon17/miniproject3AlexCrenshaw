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
CHART_DPI = 150

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
    """Build a two-panel figure: a box plot of rating distribution per
    genre, and a line chart of mean rating by decade per genre. Saves
    the figure as a PNG in charts/."""
    genre_order = (
        df.groupby("genre")["rating"].median().sort_values().index.tolist()
    )
    colors = [GENRE_COLORS[g] for g in genre_order]

    decade_means = (
        df.groupby(["decade", "genre"])["rating"].mean().unstack("genre")
    )
    decade_means = decade_means[genre_order]

    fig, (ax_box, ax_trend) = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor(CHART_SURFACE)

    # --- Left: rating distribution per genre ---
    ax_box.set_facecolor(CHART_SURFACE)
    box_data = [df.loc[df["genre"] == g, "rating"] for g in genre_order]
    bp = ax_box.boxplot(
        box_data,
        tick_labels=genre_order,
        patch_artist=True,
        medianprops={"color": INK_PRIMARY, "linewidth": 1.5},
        whiskerprops={"color": INK_MUTED},
        capprops={"color": INK_MUTED},
        flierprops={"markeredgecolor": INK_MUTED, "markersize": 4},
    )
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)
        patch.set_edgecolor(INK_PRIMARY)

    ax_box.set_title("Rating Distribution by Genre", color=INK_PRIMARY)
    ax_box.set_xlabel("Genre", color=INK_PRIMARY)
    ax_box.set_ylabel("Rating", color=INK_PRIMARY)
    ax_box.tick_params(axis="x", rotation=30, colors=INK_PRIMARY)
    ax_box.tick_params(axis="y", colors=INK_PRIMARY)
    ax_box.grid(axis="y", color=GRIDLINE, zorder=0)
    ax_box.set_axisbelow(True)
    for spine in ax_box.spines.values():
        spine.set_color(GRIDLINE)

    # --- Right: mean rating by decade, one line per genre ---
    ax_trend.set_facecolor(CHART_SURFACE)
    for genre in genre_order:
        ax_trend.plot(
            decade_means.index,
            decade_means[genre],
            marker="o",
            markersize=5,
            linewidth=2,
            color=GENRE_COLORS[genre],
            label=genre,
        )

    ax_trend.set_title("Mean Rating by Decade", color=INK_PRIMARY)
    ax_trend.set_xlabel("Decade", color=INK_PRIMARY)
    ax_trend.set_ylabel("Mean Rating", color=INK_PRIMARY)
    ax_trend.tick_params(colors=INK_PRIMARY)
    ax_trend.grid(color=GRIDLINE, zorder=0)
    ax_trend.set_axisbelow(True)
    for spine in ax_trend.spines.values():
        spine.set_color(GRIDLINE)
    ax_trend.legend(frameon=False, labelcolor=INK_PRIMARY, fontsize=9)

    fig.suptitle(
        "Movie Ratings by Genre (Practice Hub sample, n={})".format(len(df)),
        color=INK_PRIMARY,
        fontsize=13,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.95])

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
