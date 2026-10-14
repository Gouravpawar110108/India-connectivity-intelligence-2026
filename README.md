# India Connectivity Intelligence 2026

An evidence-led portfolio report on India's connectivity market, Jio's published operating position, and the conditions under which satellite internet could complement terrestrial networks.

This is the public-source edition of the project, with an evidence cut-off of 14 October 2026. It includes a report, official source register, regulator/company observations, and reproducible market calculations.

## Key findings

- In TRAI's quarterly performance series, internet subscriptions increased from 1,092.79 million at March 2026 to 1,114.17 million at June 2026, a calculated 1.96% rise. Broadband subscriptions increased from 1,065.88 million to 1,087.50 million, a calculated 2.03% rise. [S1, S2]
- TRAI reported 129.03 urban and 49.07 rural internet subscriptions per 100 population at June 2026. These are subscription-density measures and can include multiple subscriptions per person; they are not unique-person adoption rates. [S1]
- Reliance Industries reported Jio's Q1 FY2026-27 customer base at 533.3 million, with about 285 million True5G users, 28.6 million fixed-broadband connections, and 14.0 million JioAirFiber home connections. [S4]
- In the TRAI August 2026 subscription series, 5G fixed wireless access subscriptions totalled 13.45 million, including 6.98 million rural subscriptions. The same report's 538.03 million Jio broadband total includes mobile broadband and is not a home-broadband count. [S3]
- Government-reported authorisations and satellite-capacity approvals establish regulatory milestones for Starlink, but do not establish current consumer availability, price, commercial uptake, or market share. [S6, S7]

## Business question

How can Jio strengthen customer growth and retention while satellite internet creates potential new connectivity options for underserved areas of India?

## Method

The report uses official TRAI, DoT, PIB, and RIL publications. Python calculations use explicit source values and formulas. Regulator indicators, company-reported measures, policy targets, and derived metrics remain labelled separately.

## Files

### Quick links

- [report.md](report.md) - concise, shareable report summary
- [sources.md](sources.md) - official-source list
- [data/nav-snapshot.csv](data/nav-snapshot.csv) - compact headline-indicator snapshot
- [report/India_Connectivity_Intelligence_2026.pdf](report/India_Connectivity_Intelligence_2026.pdf) - full publication-ready report

- report/India_Connectivity_Intelligence_2026.pdf - publication-ready report
- report/India_Connectivity_Intelligence_2026.md - editable report text
- data/market_indicators.csv - public observations with provenance and scope
- analysis/market_analysis.py - reproducible calculations
- analysis/derived_metrics.csv - calculated output
- analysis/sql_queries.sql - example KPI queries
- references/sources.md - source register
- linkedin/linkedin_post.md - LinkedIn copy with a repository-link placeholder
- dashboard/README.md - suggested Power BI structure and definition rules
- PROJECT_LOG.md - completed work and open items
- PUBLISHING.md - exact GitHub and LinkedIn posting steps

## Evidence limitations

This release contains no customer survey, customer-level data, synthetic customer records, or third-party market estimates. It therefore does not claim measured customer satisfaction, willingness to pay, customer segments, churn prediction, or customer lifetime value. It also does not include a Power BI .pbix dashboard, a GitHub push, or a LinkedIn publication.

TRAI and company measures may use different populations, definitions, and reporting periods. In particular, do not combine the quarterly performance series with the August monthly subscription series without reconciling definitions. See the source register and report for details.

## Reproduce the calculations

Use Python 3.10+ with the packages in requirements.txt.

    python -m pip install -r requirements.txt
    python analysis/market_analysis.py

To build the PDF:

    python report/build_report.py

## Publishing

The folder is structured for a GitHub repository. See PUBLISHING.md for the exact GitHub push steps and LinkedIn PDF-document posting steps. No external account was written to during this task.
