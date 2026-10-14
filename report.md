# India Connectivity Intelligence 2026

## Executive diagnostic

### Question

What do public regulator and company sources say about India's connectivity scale, the regional footprint of fixed wireless, and the potential role of satellite internet?

### Findings from the monthly TRAI dashboard series

Two TRAI monthly releases provide service-area observations for April–July 2026. The dashboard uses regional annexures so readers can compare reported subscriptions by measure, month, area and provider.

| Measure | April 2026 | July 2026 | Calculated change | Interpretation |
| --- | ---: | ---: | ---: | --- |
| 5G FWA subscriptions | 12.55m | 13.21m | +5.24% | The reported service-area totals grew over this four-month interval. This is a connection count, not unique-user growth. |
| Wireline subscribers | 48.58m | 48.01m | −1.17% | Endpoint comparison is down; the monthly path varies, so it should not be described as a smooth decline. |

In July 2026, the five largest regional 5G FWA totals were Andhra Pradesh (1.12m), Uttar Pradesh (East) (1.05m), Maharashtra (1.02m), Bihar (1.00m) and Tamil Nadu (0.87m). These identify where reported connection stocks were concentrated; they do not show unmet demand, service quality or market attractiveness on their own.

### Broader market context

- TRAI's quarterly series shows internet subscriptions rising from 1,092.79 million at March 2026 to 1,114.17 million at June 2026 (+1.96%); broadband subscriptions rose from 1,065.88 million to 1,087.50 million (+2.03%). [S1, S2]
- TRAI reported June internet subscription density at 129.03 per 100 population in urban areas and 49.07 per 100 in rural areas. These are subscription-density indicators, not unique-person adoption rates. [S1]
- Reliance Industries reported Jio's June 2026 base at 533.3 million customers, around 285 million True5G users, 28.6 million fixed-broadband connections and 14.0 million JioAirFiber home connections. These are company-reported measures with definitions that may differ from TRAI series. [S4]
- TRAI's August 2026 report recorded 13.45 million 5G FWA subscriptions, of which 6.98 million were rural. This is a later, separate monthly release and is not appended to the April–July dashboard extract. [S3]
- Government-reported satellite authorisation and capacity milestones do not demonstrate current retail availability, price, uptake or market share. [S6, S7]

### Business implications

1. **Use FWA to focus regional planning.** Monitor service-area connection trends alongside network capacity, coverage, affordability and service-quality evidence before prioritising investment.
2. **Treat wireline and FWA as distinct infrastructure options.** The data show their reported subscription stocks, but do not establish substitution or causality.
3. **Position satellite as a targeted complement hypothesis.** Test specific remote or hard-to-reach use cases only after confirming authorisation, commercial availability, economics and customer need.
4. **Build the next analysis around outcomes.** Add comparable coverage and quality measures, price plans, and consented customer research before making claims about satisfaction, churn, willingness to pay or lifetime value.

## Method and reproducibility

TRAI PDFs S8 and S9 were parsed into a source-observation extract with metric, period end, service area, provider, value, unit, source ID, PDF page and scope note. Cleaning standardises geography labels, removes duplicate keys and preserves missing values as missing. Provider values and source-reported totals remain separate. The processed fact table has 1,121 observations; `sample_1000.csv` is a reproducible 1,000-row sample.

The dimensional CSVs model period, geography, provider, metric and source. SQLite examples in `sql/` demonstrate staging/cleaning, star-schema table creation and KPI queries using CTEs and window functions. To regenerate the extract and processed CSVs, install `requirements.txt` and run `python analysis/prepare_public_dataset.py`.

## Limitations

The results are descriptive and aggregate. The project contains no customer-level records, customer survey, device-level data, service quality, price comparison, causal experiment or forecast. It does not claim customer satisfaction, churn prediction, willingness to pay or customer lifetime value. Metric definitions and populations vary among TRAI quarterly, TRAI monthly and company disclosures; compare them only with explicit caveats. See [sources.md](sources.md) for provenance and [README.md](README.md) for how to open the interactive dashboard.
