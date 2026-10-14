# Interactive connectivity dashboard

`index.html` is a working, static browser dashboard backed by `../data/processed/dashboard_data.json`. It includes filters for measure, reporting period, TRAI service area and provider, with subscription summaries, month-over-month comparisons, four-period trends and service-area rankings.

## Run locally

From the repository root, start a local web server:

```powershell
python -m http.server 8000
```

Open `http://localhost:8000/dashboard/`. The JSON file is fetched by the page, so opening `index.html` directly from disk may show a data-loading message. GitHub Pages also works as a static host.

## Definitions and safeguards

- The current monthly series covers April–July 2026 and is extracted from the two linked TRAI reports listed on the page and in [../sources.md](../sources.md).
- Provider details and source-reported aggregate totals are distinct series. Where an aggregate exists, “All providers” uses the published total and does not add operator rows to it.
- Counts are reported subscriptions/connections, not unique individuals.
- The charts are descriptive and do not imply service quality, causality, customer preference or forecast.

`../visuals/dashboard_walkthrough.gif` is a ten-second visual sequence illustrating different filter states using the source-backed dashboard values. It is a walkthrough animation, not a screen recording of live user input. This repository does not contain a native Power BI `.pbix` or Tableau workbook; the processed CSVs are ready to import into either tool.
