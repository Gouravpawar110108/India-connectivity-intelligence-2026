"""Extract a reproducible public-data star schema from TRAI PDF tables."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

AREA_ORDER = [
    "Andhra Pradesh", "Assam", "Bihar", "Delhi", "Gujarat", "Haryana",
    "Himachal Pradesh", "Jammu & Kashmir", "Karnataka", "Kerala", "Kolkata",
    "Madhya Pradesh", "Maharashtra", "Mumbai", "North East", "Odisha", "Punjab",
    "Rajasthan", "Tamil Nadu", "Uttar Pradesh (East)", "Uttar Pradesh (West)",
    "West Bengal",
]

DOCS = [
    {
        "file": "TRAI_Telecom_Subscription_May_2026.pdf",
        "source_id": "S8",
        "source_url": "https://trai.gov.in/sites/default/files/2026-06/PR_No78of2026_0.pdf",
        "pages": {"summary": 0, "broadband_mix": 1, "provider_mix": 2,
                  "wireline": 18, "fwa_5g": 23, "fwa_ubr": 24},
        "latest_month": "May-26",
    },
    {
        "file": "TRAI_Telecom_Subscription_July_2026.pdf",
        "source_id": "S9",
        "source_url": "https://trai.gov.in/sites/default/files/2026-08/PR_No116of2026_0.pdf",
        "pages": {"summary": 0, "broadband_mix": 1, "provider_mix": 2,
                  "wireline": 18, "fwa_5g": 23, "fwa_ubr": 24},
        "latest_month": "Jul-26",
    },
]

METRIC_DEFS = {
    "wireline_subscriber_base": ("Wireline telephone subscriber base", "subscriptions"),
    "fwa_5g_subscriber_base": ("5G fixed-wireless subscriber base", "subscriptions"),
    "fwa_5g_all_provider_total": ("TRAI-reported total 5G FWA subscriptions", "subscriptions"),
    "fwa_ubr_subscriber_base": ("UBR fixed-wireless subscriber base", "subscriptions"),
    "broadband_top_provider_base": ("Broadband subscriber base for listed top providers", "million_subscriptions"),
    "broadband_segment_subscriptions": ("Broadband subscriptions by access segment", "million_subscriptions"),
    "broadband_top5_share": ("Top-five provider market share for the named broadband segment", "percent"),
    "trai_summary_metric": ("TRAI monthly release summary measure; see source label", "source_reported_unit"),
}

def clean_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()

def number(value: object) -> float | None:
    text = clean_text(value).replace(",", "")
    if not text:
        return None
    if text.endswith("%"):
        try:
            return float(text[:-1])
        except ValueError:
            return None
    try:
        return float(text)
    except ValueError:
        return None

def month_end(label: str) -> str:
    match = re.fullmatch(r"([A-Za-z]+)-?(\d{2})", clean_text(label))
    if not match:
        match = re.fullmatch(r"([A-Za-z]+)[-\n ]+(\d{2})", clean_text(label))
    if not match:
        raise ValueError(f"Unrecognised month label: {label!r}")
    return pd.Timestamp(f"{match.group(1)} 1 20{match.group(2)}").to_period("M").end_time.date().isoformat()

def row_numbers(row: list[object]) -> list[float]:
    return [v for cell in row if (v := number(cell)) is not None]

def add_record(rows: list[dict], *, metric: str, period: str, geography: str,
               provider: str, value: float, unit: str, source: dict,
               page: int, definition: str = "") -> None:
    rows.append({
        "metric_id": metric,
        "period_end": period,
        "geography": geography,
        "provider": provider,
        "value": value,
        "unit": unit,
        "source_id": source["source_id"],
        "source_file": source["file"],
        "source_page": page + 1,
        "source_url": source["source_url"],
        "scope_note": definition,
    })

def extract_wireline(pdf, source: dict, rows: list[dict]) -> None:
    page_idx = source["pages"]["wireline"]
    tables = pdf.pages[page_idx].extract_tables()
    table = next(
        t for t in tables
        if any("Service Area" in clean_text(cell) for row in t[:4] for cell in row if cell)
        and any("BSNL" in clean_text(cell) for row in t[:4] for cell in row if cell)
    )
    header_idx = next(i for i, row in enumerate(table[:4]
                      ) if any("Service Area" in clean_text(cell) for cell in row if cell)
                        and any("BSNL" in clean_text(cell) for cell in row if cell))
    headers, periods = table[header_idx], table[header_idx + 1]
    # The first 10 paired columns are named operators; the final pair is the TRAI area total.
    for record in table[header_idx + 2:]:
        area = clean_text(record[0]) if record else ""
        if area in {"", "Total", "Net Addition", "Rural Subscribers", "Service Area"}:
            continue
        for col in range(1, 23, 2):
            provider = clean_text(headers[col]) or "All providers"
            if provider.lower() == "net":
                continue
            if col == 21 or provider.lower() == "total":
                provider = "All providers"
            for offset in (0, 1):
                value = number(record[col + offset]) if col + offset < len(record) else None
                month = clean_text(periods[col + offset]) if col + offset < len(periods) else ""
                if value is not None and month:
                    add_record(rows, metric="wireline_subscriber_base", period=month_end(month),
                               geography=area, provider=provider, value=value,
                               unit="subscriptions", source=source, page=page_idx,
                               definition="TRAI monthly annexure; area-by-provider stock at period end.")

def extract_fwa(pdf, source: dict, rows: list[dict]) -> None:
    page_idx = source["pages"]["fwa_5g"]
    table = pdf.pages[page_idx].extract_tables()[0]
    period_header = table[3]
    # Across the merged cells the six non-empty values on each area row are
    # Airtel June/May, Jio June/May, and TRAI total June/May (or June/July).
    periods = [clean_text(period_header[i]) for i in (3, 6, 9, 12, 15, 16)]
    data_rows = []
    for row in table[6:]:
        values = row_numbers(row)
        if len(values) >= 6:
            data_rows.append(values[:6])
    for area, values in zip(AREA_ORDER, data_rows[:22]):
        for i, provider in enumerate(("Bharti Airtel", "Reliance Jio", "All providers")):
            for j in range(2):
                value = values[i * 2 + j]
                month = periods[i * 2 + j]
                is_total = provider == "All providers"
                add_record(rows, metric="fwa_5g_all_provider_total" if is_total else "fwa_5g_subscriber_base",
                           period=month_end(month), geography=area, provider=provider,
                           value=value, unit="subscriptions", source=source, page=page_idx,
                           definition=("TRAI-reported all-provider area total; do not add to provider rows."
                                       if is_total else "TRAI monthly 5G FWA subscriber base."))

def extract_ubr(pdf, source: dict, rows: list[dict]) -> None:
    page_idx = source["pages"]["fwa_ubr"]
    table = pdf.pages[page_idx].extract_tables()[0]
    period_header = table[2]
    periods = [clean_text(period_header[i]) for i in (4, 7)]
    data_rows = []
    for row in table[3:]:
        values = row_numbers(row)
        if len(values) >= 2:
            data_rows.append(values[:2])
    for area, values in zip(AREA_ORDER, data_rows[:22]):
        for month, value in zip(periods, values):
            add_record(rows, metric="fwa_ubr_subscriber_base", period=month_end(month),
                       geography=area, provider="Reliance Jio", value=value,
                       unit="subscriptions", source=source, page=page_idx,
                       definition="TRAI notes that only Reliance Jio reported UBR FWA subscriptions.")

def extract_broadband_tables(pdf, source: dict, rows: list[dict]) -> None:
    mix_idx = source["pages"]["broadband_mix"]
    table = pdf.pages[mix_idx].extract_tables()[0]
    # Fixed-wired, fixed-wireless, mobile-wireless and total records; both months are in the table.
    for row in table:
        label = clean_text(" ".join(str(c or "") for c in row[:4])).lower()
        metric_name = None
        if "fixed wired access" in label:
            metric_name = "Fixed wired access"
        elif "fixed wireless access" in label:
            metric_name = "Fixed wireless access"
        elif "mobile wireless access" in label:
            metric_name = "Mobile wireless access"
        elif "total broadband subscriptions" in label:
            metric_name = "Total broadband subscriptions"
        if not metric_name:
            continue
        vals = [number(c) for c in row]
        vals = [v for v in vals if v is not None]
        if len(vals) < 2:
            continue
        # Use header columns to distinguish the two observations from the growth-rate column.
        numeric_cells = [(i, number(c)) for i, c in enumerate(row) if number(c) is not None]
        period_cols = [i for i, c in enumerate(table[3]) if clean_text(c)]
        for col, value in numeric_cells:
            if col not in period_cols or value is None:
                continue
            month = clean_text(table[3][col]).replace("\n", " ")
            try:
                date = month_end(month.replace(" 2026", "-26"))
            except ValueError:
                continue
            add_record(rows, metric="broadband_segment_subscriptions", period=date,
                       geography="India", provider=metric_name, value=value,
                       unit="million_subscriptions", source=source, page=mix_idx,
                       definition="TRAI broadband category totals; report definition includes M2M unless noted.")

    provider_idx = source["pages"]["provider_mix"]
    provider_tables = pdf.pages[provider_idx].extract_tables()
    metrics = ["broadband_top_provider_base", "broadband_top_provider_base"]
    segments = ["Fixed wired access", "Fixed wireless and mobile access"]
    for table_index, metric in enumerate(metrics):
        if table_index >= len(provider_tables):
            continue
        table = provider_tables[table_index]
        if not table or "Service Provider" not in clean_text(table[0][1]):
            continue
        segment = segments[table_index]
        for row in table[1:6]:
            provider = clean_text(row[1])
            value = next((number(c) for c in reversed(row[2:]) if number(c) is not None), None)
            if not provider or value is None:
                continue
            add_record(rows, metric=metric, period=month_end(source["latest_month"]),
                       geography="India", provider=f"{provider} ({segment})", value=value,
                       unit="million_subscriptions", source=source, page=provider_idx,
                       definition="TRAI lists these top-five providers; this table is not the full market." )

    all_provider_tables = pdf.pages[mix_idx].extract_tables()
    if len(all_provider_tables) >= 5:
        table = all_provider_tables[4]
        for row in table[1:6]:
            provider = clean_text(row[1])
            value = next((number(c) for c in reversed(row[2:]) if number(c) is not None), None)
            if provider and value is not None:
                add_record(rows, metric="broadband_top_provider_base",
                           period=month_end(source["latest_month"]), geography="India",
                           provider=f"{provider} (Wired and wireless)", value=value,
                           unit="million_subscriptions", source=source, page=mix_idx,
                           definition="TRAI top-five wired and wireless broadband list; not the full market." )

def extract_summary(pdf, source: dict, rows: list[dict]) -> None:
    page_idx = source["pages"]["summary"]
    tables = pdf.pages[page_idx].extract_tables()
    if not tables:
        return
    period = month_end(source["latest_month"])
    for row_index, row in enumerate(tables[0][3:], start=1):
        label = clean_text(" ".join(str(c or "") for c in row[:3]))
        if not label:
            continue
        for col, cell in enumerate(row):
            value = number(cell)
            if value is None or col < 3:
                continue
            if 3 <= col <= 5:
                segment = "Wireless"
            elif 6 <= col <= 8:
                segment = "Wireline"
            else:
                segment = "Total"
            suffix = "percent" if "%" in clean_text(cell) or "rate" in label.lower() or "share" in label.lower() or "density" in label.lower() else "million"
            add_record(rows, metric=f"summary_{row_index:02d}_{re.sub(r'[^a-z0-9]+','_',label.lower()).strip('_')}_{segment.lower()}",
                       period=period, geography="India", provider=segment, value=value,
                       unit=suffix, source=source, page=page_idx,
                       definition=f"TRAI summary table: {label}; {segment} column.")

def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    for source in DOCS:
        pdf_path = RAW / source["file"]
        if not pdf_path.exists() or pdf_path.stat().st_size < 50_000:
            raise FileNotFoundError(f"Missing official TRAI source PDF: {pdf_path}")
        with pdfplumber.open(pdf_path) as pdf:
            extract_wireline(pdf, source, rows)
            extract_fwa(pdf, source, rows)
            extract_ubr(pdf, source, rows)
            extract_broadband_tables(pdf, source, rows)
            extract_summary(pdf, source, rows)

    raw = pd.DataFrame(rows)
    if raw.empty:
        raise ValueError("No data records were extracted.")
    raw["period_end"] = pd.to_datetime(raw["period_end"])
    # Preserve the uncleaned table extraction before applying the dimension mappings.
    raw_path = RAW / "trai_monthly_extracted_observations.csv"
    raw.to_csv(raw_path, index=False)

    facts = raw.copy()
    facts["geography"] = facts["geography"].replace({
        "J & K": "Jammu & Kashmir", "Jammu & Kashmir": "Jammu & Kashmir",
        "U.P.(E)": "Uttar Pradesh (East)", "U.P.(W)": "Uttar Pradesh (West)",
        "U.P.(W )": "Uttar Pradesh (West)",
    })
    facts["provider"] = facts["provider"].replace({"Total": "All providers"})
    facts["source_id"] = facts["source_id"].astype(str)
    facts["value"] = pd.to_numeric(facts["value"], errors="coerce")
    facts = facts.dropna(subset=["value", "period_end"])
    facts = facts.drop_duplicates(subset=["metric_id", "period_end", "geography", "provider", "source_id", "source_page"])
    facts.insert(0, "observation_id", range(1, len(facts) + 1))
    facts["period_end"] = facts["period_end"].dt.date.astype(str)
    facts.to_csv(PROCESSED / "fact_connectivity.csv", index=False)
    facts.to_json(PROCESSED / "dashboard_data.json", orient="records", indent=2)

    periods = facts[["period_end"]].drop_duplicates().sort_values("period_end").reset_index(drop=True)
    periods.insert(0, "period_key", range(1, len(periods) + 1))
    periods.to_csv(PROCESSED / "dim_period.csv", index=False)
    areas = sorted(set(facts["geography"]))
    pd.DataFrame({"geography_key": range(1, len(areas) + 1), "geography": areas,
                  "geography_type": ["National" if a == "India" else "TRAI service area" for a in areas]})\
        .to_csv(PROCESSED / "dim_geography.csv", index=False)
    providers = sorted(set(facts["provider"]))
    pd.DataFrame({"provider_key": range(1, len(providers) + 1), "provider": providers})\
        .to_csv(PROCESSED / "dim_provider.csv", index=False)
    metric_ids = sorted(set(facts["metric_id"]))
    metric_rows = []
    for metric in metric_ids:
        desc, default_unit = METRIC_DEFS.get(metric, (metric.replace("_", " ").title(), "source_reported_unit"))
        metric_rows.append({"metric_key": len(metric_rows) + 1, "metric_id": metric,
                            "metric_name": desc, "default_unit": default_unit})
    pd.DataFrame(metric_rows).to_csv(PROCESSED / "dim_metric.csv", index=False)
    source_rows = facts[["source_id", "source_file", "source_url"]].drop_duplicates().sort_values("source_id")
    source_rows.insert(0, "source_key", range(1, len(source_rows) + 1))
    source_rows.to_csv(PROCESSED / "dim_source.csv", index=False)

    sample = facts.sample(n=min(1000, len(facts)), random_state=2026).sort_values("observation_id")
    sample.to_csv(RAW / "sample_1000.csv", index=False)
    print(f"Extracted {len(raw):,} source records; cleaned fact rows: {len(facts):,}; sample rows: {len(sample):,}.")
    if len(sample) < 1000:
        print("Note: fewer than 1,000 valid source records were available; the sample contains all available rows.")
    print(f"Wrote: {raw_path}")

if __name__ == "__main__":
    main()
