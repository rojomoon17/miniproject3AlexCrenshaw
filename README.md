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

If `requests` fails with a `CERTIFICATE_VERIFY_FAILED` error, it could be
antivirus software (e.g. Avast) doing HTTPS scanning with a
root certificate that isn't in Python's bundled `certifi` trust store
- same issue as in miniproject2. Add an exception for `python.exe` in
your antivirus's HTTPS/SSL scanning settings, or install
`python-certifi-win32` in your venv to use Windows' own certificate
store instead.

## AI Usage

This project was built with Claude Code.

- Drafted the implementation plan (question, data source, DataFrame/chart design, file list).
- Queried the Practice Hub API to determine the `movies` schema and the 500-row request cap.
- Wrote `movie_report.py`: data fetch, DataFrame/groupby logic, and the box-plot + small-multiples chart.
- Generated `requirements.txt` via `pip freeze`, then removed Windows-only packages unrelated to the script.
- Redesigned the chart in three passes: (1) small-multiples decade grid, lighter box plot styling, mean reference line, larger figure/DPI, takeaway caption; (2) per-panel decade labels with a shared y-scale, genre label abbreviation and its later reversal; (3) dark charcoal theme, warm gold-to-rose genre palette, white mean-reference line/label.
- Wrote all git commits and this README.

## What I Did

- Chose the data source and question from options Claude proposed.
- Reviewed and approved the plan before any code was written.
- Created the `miniproject3AlexCrenshaw` GitHub repo and set my local `PRACTICE_API_TOKEN`.
- Directed every design revision by specific instruction (listed above under AI Usage) and reviewed each chart render before approving it.
- Approved every commit and push individually; nothing was committed or pushed without my go-ahead.
- I did not hand-edit any file directly - all code, chart, and text changes were made by Claude Code per my instructions.
