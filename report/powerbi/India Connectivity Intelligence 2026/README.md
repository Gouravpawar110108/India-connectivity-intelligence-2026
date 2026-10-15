# Power BI model draft — India Connectivity Intelligence 2026

This folder contains a **draft design pack**, not a `.pbix` or `.pbip` file. It was generated from the six processed CSV tables in `../../../../data/processed/`.

## Draft contents

- `codex-model-drafts/model-design.json` — proposed star-schema tables, sources, and report pages.
- `codex-model-drafts/data-contract-draft.json` — source and grain requirements.
- `codex-model-drafts/connection-drafts.json` — sanitized relative CSV paths and profiled columns.
- `codex-model-drafts/measure-drafts.json` — proposed DAX expressions and plain-language definitions.
- `codex-model-drafts/power-query-source-drafts.md` — Power Query starting point.

## Proposed table relationships

`DimPeriod`, `DimGeography`, `DimProvider`, `DimMetric`, and `DimSource` each relate one-to-many to `FactConnectivity` on their shared natural key. Configure `DimPeriod[period_end]` as Date and confirm each dimension key is unique before applying relationships.

## Review needed before creating a PBIP

Confirm the KPI definitions and ownership in `measure-drafts.json`. Owners are intentionally unassigned. Verify that `All providers` aggregate rows are the measure basis and must never be added to operator-detail rows. This source is a public monthly snapshot; no RLS role is proposed. The wizard cannot create the native project; create and save a new PBIP in Power BI Desktop, then apply reviewed drafts and validate it there.
