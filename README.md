# India Connectivity Intelligence 2026

An evidence-led view of India's connectivity market, regional fixed-wireless access (FWA), wireline infrastructure and operator-reported indicators. This repository combines regulator source documents, a traceable data extract, SQL examples, an interactive browser dashboard and an executive report.

**Evidence cut-off:** 14 October 2026.<br>
**Current monthly dashboard series:** April–July 2026.
**Primary sources:** Telecom Regulatory Authority of India (TRAI), Department of Telecommunications, Press Information Bureau and Reliance Industries Limited. See [sources.md](sources.md).

## Executive takeaways

- TRAI's published regional 5G FWA totals increased from **12.55 million in April** to **13.21 million in July 2026**, a calculated **5.24%** increase across the four-month window. This is growth in reported subscriptions, not unique people.
- In July, the largest reported regional 5G FWA totals were **Andhra Pradesh (1.12m), Uttar Pradesh (East) (1.05m), Maharashtra (1.02m), Bihar (1.00m) and Tamil Nadu (0.87m)**.
- TRAI's monthly annexures show wireline totals of **48.58m in April** and **48.01m in July**. The monthly series is not monotonic; use the filters and source notes to inspect each month rather than treating the endpoints as a trend forecast.
- FWA and wireline figures describe subscriptions/connections. Subscription density and company-reported customer counts elsewhere in the report use different definitions and must not be merged as if they share a common denominator.

These are descriptive findings from published regulator tables. They do not establish consumer preference, service quality, profitability, causal impact or future demand.

## Explore the project

| Folder or file | What it contains |
| --- | --- |
| [dashboard/](dashboard/) | Portfolio-ready interactive HTML dashboard with four approved KPI cards, measure/month/area/provider filters, source-row detail and CSV download. Open through GitHub Pages or a local web server. |
| [report.md](report.md) | Executive diagnostic and business interpretation. |
| [report/India_Connectivity_Intelligence_2026.pdf](report/India_Connectivity_Intelligence_2026.pdf) | Designed PDF report from the broader public-source research edition. |
| [Power BI model draft](report/powerbi/India%20Connectivity%20Intelligence%202026/README.md) | Draft semantic model, source contract, Power Query starting point and KPI definitions for review. |
| [data/raw/](data/raw/) | Official TRAI PDF releases, extracted source observations and deterministic 1,000-row sample. |
| [data/processed/](data/processed/) | Cleaned fact table, dimensional CSVs and dashboard JSON payload. |
| [sql/](sql/) | SQLite staging/cleaning, star-schema DDL and business KPI queries. |
| [visuals/data_model_erd.png](visuals/data_model_erd.png) | Star-schema relationship diagram. |
| [visuals/dashboard_walkthrough.gif](visuals/dashboard_walkthrough.gif) | 10-second sequence illustrating different dashboard filter states. |
| [linkedin/linkedin_post.md](linkedin/linkedin_post.md) | Copy-ready LinkedIn post draft. |

## Data and method

The monthly extract was built from two official TRAI reports. The May release supplies April and May annexure values; the July release supplies June and July values. The parser records source release, source page, period, metric, geography, provider, unit and scope note for each observation. `data/raw/trai_monthly_extracted_observations.csv` preserves extracted rows; `data/processed/fact_connectivity.csv` is the cleaned analytical fact table. The sample contains 1,000 records selected reproducibly with seed `2026`.

The dimensional model separates period, geography, provider, metric and source. The SQLite SQL files demonstrate one implementation path. Source-reported aggregates are retained as aggregate rows alongside provider detail. **Never add a `provider = All providers` total to its underlying operator rows.** Missing cells remain missing; they are not changed to zero.

### Main calculated KPI

`(July 2026 5G FWA total − April 2026 5G FWA total) / April 2026 total × 100 = 5.24%`.

Regional values are summed from TRAI's published `All providers` service-area totals. The sum reconciles to the national total in the source release for each month. Rebuild the extract and dimensional CSVs with:

```powershell
python -m pip install -r requirements.txt
python analysis/prepare_public_dataset.py
```

## Open the dashboard

The dashboard loads a JSON file, so use a local static web server from the repository root instead of opening the HTML as a `file://` URL:

```powershell
python -m http.server 8000
```

Then visit `http://localhost:8000/dashboard/`. The dashboard opens on the July 2026 portfolio snapshot and includes a source-backed monthly comparison, top service-area bars, selectable measures and a filtered observation table with CSV download. GitHub Pages can also host the repository as a static site.

## Power BI / Tableau workbook

This release includes an interactive, source-backed HTML dashboard, Power BI/Tableau-ready CSVs, and a Power BI model design draft with proposed relationships and DAX measures. It does **not** include a native `.pbix` or Tableau workbook. The connected Power BI model wizard produces reviewable drafts; a person must create and save a new PBIP in Power BI Desktop before these drafts can be applied and validated. Review the proposed definitions and ownership notes in the [Power BI model draft](report/powerbi/India%20Connectivity%20Intelligence%202026/README.md). Use [visuals/data_model_erd.png](visuals/data_model_erd.png) as the relationship guide.

## Caveats

- TRAI service-area subscription counts are connection stocks, not unique individuals.
- Provider detail coverage varies by metric; top-five provider ranking tables are not a full-market census.
- UBR is reported only for the provider named in the source.
- Monthly tables and quarterly performance indicators may have different scope and definitions. Do not combine them without reconciling the measure.
- Satellite authorisations or policy milestones do not prove retail availability, pricing, uptake or market share.
- No customer-level data, survey responses, satisfaction measures, churn model or causal analysis is included.

See [sources.md](sources.md) and [report.md](report.md) for provenance and interpretation. The project is analytical research, not investment advice.
