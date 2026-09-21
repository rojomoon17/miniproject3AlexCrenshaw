# miniproject3AlexCrenshaw

Mini Project 3 for INF601 - Advanced Programming in Python.

## The question

**How does movie rating vary by genre, and has any genre's average
rating trended up or down by decade since the 1970s?**

## What it does

- Fetches a sample of 500 movies (title, director, year, genre,
  rating) from the [Practice Hub](https://practice.fhsucyber.com)
  API's `GET /api/v1/datasets/movies` endpoint.
- Loads the results into a Pandas `DataFrame` and derives a `decade`
  column from each movie's release year.
- Prints the row count and mean rating per genre to the console.
- Plots a Matplotlib figure:
  - **Left:** a box plot of the rating distribution for each genre
    (Action, Comedy, Documentary, Drama, Horror, Sci-Fi), so you can
    compare medians and spread at a glance.
  - **Right:** a 2x3 small-multiples grid, one mini line chart per
    genre showing mean rating by decade, so each genre's trend can be
    read on its own instead of six overlapping lines on one chart.
  - Both panels share a reference line at the overall mean rating.
- Saves the figure as a PNG in `charts/`. This folder is generated
  when the script runs and is **not** committed to the repo (see
  `.gitignore`).

**Answer:** across this sample, genre means are close together
(roughly 5.2-5.8) with no genre consistently pulling away, and the
decade lines don't show a steady up or down trend for any genre - they
swing up and down decade to decade instead. The data is Faker-style
synthetic data from the Practice Hub, so the "answer" is really that
there's no strong genre or time signal to find - which is itself a
useful result to be able to show with a DataFrame and a chart.

## Data source

Practice Hub `GET /api/v1/datasets/movies`, authenticated with a
bearer token. You need a `PRACTICE_API_TOKEN` environment variable set
before running the script (see Week 2 material for how to get a
token).

```powershell
$env:PRACTICE_API_TOKEN = "your-token-here"   # PowerShell, current session
```

## Requirements

- Python 3.11+

## Installation

```bash
git clone https://github.com/rojomoon17/miniproject3AlexCrenshaw.git
cd miniproject3AlexCrenshaw
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # macOS/Linux
pip install -r requirements.txt
```

## Running it

```bash
python movie_report.py
```

This prints the fetched row count and mean rating per genre, then
writes `charts/movie_ratings_by_genre.png` (created automatically if
`charts/` doesn't already exist).

## Troubleshooting

If `requests` fails with a `CERTIFICATE_VERIFY_FAILED` error, it's
likely antivirus software (e.g. Avast) doing HTTPS scanning with a
root certificate that isn't in Python's bundled `certifi` trust store
- same issue as in miniproject2. Add an exception for `python.exe` in
your antivirus's HTTPS/SSL scanning settings, or install
`python-certifi-win32` in your venv to use Windows' own certificate
store instead.

## AI Usage

This project was built with Claude Code. Roughly how it was used:

- I asked for a plan before any code was written. Claude asked me to
  pick a data source, then proposed several question/source pairings
  (Practice Hub movies/stocks/people, a data.gov broadband dataset, a
  Kaggle Netflix dataset) with a suggested chart for each; I picked
  the Practice Hub movies option.
- Claude authenticated against the Practice Hub API (reusing the base
  URL and bearer-token pattern from miniproject1's `client.py`) to
  inspect the actual response schema before writing any code, since
  the original plan assumed a `runtime` field that turned out not to
  exist - the real fields are title, director, year, genre, and
  rating. It also discovered the server caps `count` at 500 per
  request through trial and error.
- Claude wrote a plan file (question, data source, DataFrame/groupby
  approach, chart layout, file list) and I approved it before any
  code was written.
- `movie_report.py`, the box-plot-and-decade-trend figure, and the
  color choices were drafted by Claude Code, then run and checked by
  me.
- `requirements.txt` was generated with `pip freeze` in the project's
  venv; Claude then removed a few Windows-only packages
  (`python-certifi-win32` and its dependencies) that were only needed
  locally to work around the antivirus certificate issue above, not
  by the script itself.
- After the first version shipped, I asked Claude to suggest ways to
  make the chart more readable and visually appealing. It proposed a
  ranked list (replace the single overlaid 6-line decade chart with
  small multiples, lighten the box plot styling, add a mean reference
  line, bump figure size/DPI, add a takeaway caption) and I asked for
  all of them. I then asked for two more passes: abbreviating
  "Documentary" to "Docu." so its box plot label stopped crowding its
  neighbors, and showing decade labels on every small-multiple panel
  (not just the bottom row) with a consistent shared y-scale across
  all six. I reviewed each redraw before approving it, and held off on
  committing/pushing until I'd seen the result.
- I then asked for a dark charcoal background with contrasting text
  and a warm color gradient fitting the movie theme, and to restore
  "Documentary" to its full name now that the angled labels had room
  for it. Claude picked a gold-to-rose palette held at equal
  lightness/saturation so every genre reads with similar contrast
  against the dark surface, and flagged the tradeoff itself: a
  purely warm palette sits closer together in hue than the prior
  cross-spectrum one, so it's a little less distinguishable for
  colorblind viewers by color alone - mitigated by every genre
  already being labeled directly (tick labels and panel titles)
  rather than relying on a legend. I also asked for the overall-mean
  reference line and its label in white after noticing they blended
  into the dark background in the first pass.
- This README was drafted by Claude Code and reviewed by me.
