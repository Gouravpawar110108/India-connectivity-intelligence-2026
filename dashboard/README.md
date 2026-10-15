# India Connectivity Intelligence dashboard

`index.html` is a source-backed, static browser dashboard powered by `../data/processed/dashboard_data.json`. The portfolio snapshot uses four reviewed KPIs, followed by controls for measure, reporting period, TRAI service area and provider or reported group.

## Portfolio KPIs

- **5G FWA subscriptions:** July 2026 TRAI `All providers` service-area totals.
- **5G FWA month-over-month growth:** July total compared with June total, calculated from the same published service-area aggregate rows.
- **Wireline subscribers:** July 2026 TRAI `All providers` service-area totals.
- **Source observations:** number of records in the dashboard data extract.

The separate four-month finding compares April with July 2026. The subscription totals are connection stocks, not unique people. Aggregate values must not be added to provider detail. Measures that have only India-level observations do not show a service-area comparison.

## Explore and download

The charts show a zero-based monthly comparison and the top five service areas when service-area data are available. Open **Inspect selected-period source rows** to review the records behind the current selection. **Download current rows CSV** exports the same measure, period, area and provider filters displayed in the detail table, including source IDs, filenames, page references, URLs and scope notes.

## Run locally

From the repository root, start a local web server:

```powershell
python -m http.server 8000
```

Open `http://localhost:8000/dashboard/`. The JSON file is fetched by the page, so opening `index.html` directly as a `file://` URL will not load the data. GitHub Pages can host the folder as a static site when enabled for the repository.

## Source and limitations

The April–July monthly series is extracted from the two official TRAI reports linked in [../sources.md](../sources.md). Provider coverage differs by measure; top-five provider rows are not a complete-market census. The charts are descriptive and do not measure service quality, causality, customer preference, churn or forecasts. The repository includes Power BI/Tableau-ready CSVs and a Power BI model draft, but no native `.pbix` or Tableau workbook.
