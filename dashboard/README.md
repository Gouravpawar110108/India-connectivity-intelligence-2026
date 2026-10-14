# Power BI dashboard plan

No Power BI dashboard file is included in this release. The figures and definitions here are a dashboard specification, not a claim that a .pbix has been built.

## Recommended pages

1. Market overview: March-June 2026 internet and broadband counts, growth, wireless ARPU, and reporting dates.
2. Connectivity opportunity: urban/rural internet subscription density and the August 2026 5G FWA split.
3. Jio operating position: company-reported Q1 FY27 customer base, 5G users, ARPU, churn, fixed broadband, and AirFiber.
4. Regulation and service readiness: documented Starlink authorisation milestones and the unverified commercial-availability items.
5. Evidence and definitions: source register, metric definitions, dates, and limits.

## Modeling rules

- Keep TRAI observations, RIL company-reported KPIs, policy targets, and calculated measures in separate tables or clearly separated categories.
- Preserve source_id, publication date, observation period, unit, and scope note for every record.
- Do not blend the August monthly broadband series (which reports with/without M2M) into the March-June quarterly performance series without reconciling definitions.
- Do not use subscriber density per 100 population as unique-person adoption.
- Do not present Jio's total broadband subscriber count as fixed-home broadband; the TRAI provider count includes mobile broadband.
- No survey responses or synthetic customer records are supplied. Customer segmentation, satisfaction, willingness-to-pay, and customer-level churn pages should remain out of the report until appropriate data exists.

## Suggested interactions

Use a period selector for quarterly market measures, a source-type selector for regulator versus company measures, and an August 2026 provider view. Include source notes in tooltips and page footers. Never imply that filters change source definitions.
