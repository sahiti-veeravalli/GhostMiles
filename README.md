# GhostMiles — Genuine Data Edition

## What changed

This version **does not bundle fake ride records**.

On startup it queries the **official City of Chicago Data Portal** for the 2026 Taxi Trips dataset. The source is public and currently contains millions of trip rows.

Source:
https://data.cityofchicago.org/Transportation/Taxi-Trips-2026/94nw-re7c

## The actual analytics problem

A public trip record tells us where a taxi's previous trip ended and where its next reported trip began. GhostMiles pairs those consecutive trips by `taxi_id` and calculates the straight-line distance between:

`previous drop-off centroid → next pickup centroid`

That produces **estimated deadhead miles**.

Important: this is **not claimed to be observed GPS movement**. The app explicitly labels it as an estimate because the public dataset does not expose the complete trajectory between trips.

This makes the project defensible in an interview.

## Why this is useful for a Rapido Data Analyst application

The workflow maps to the JD:

- SQL-style consecutive-trip/window analysis
- KPI tracking
- spatial/temporal analysis
- root-cause exploration
- business recommendation
- intervention simulation
- exportable evidence
- transparent assumptions

## Run

```bash
cd GhostMiles_Genuine
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The first load needs internet access because the app fetches live public data.

## Suggested resume wording

**GhostMiles — Mobility Capacity Analytics**
Built a data analytics platform using public City of Chicago trip data to estimate deadhead movement between consecutive taxi trips, identify spatial/temporal waste patterns, and model driver-repositioning scenarios; implemented window-style trip sequencing, geospatial distance calculations, KPI analysis and interactive decision dashboards.

## What NOT to claim

Do not say:
- "I used Rapido's data."
- "I tracked drivers' GPS."
- "These are actual empty miles."

Say:
- "I used public City of Chicago trip data."
- "I inferred estimated deadhead from consecutive trip endpoints."
- "The scenario model quantifies potential savings under explicit assumptions."

This distinction is important.
