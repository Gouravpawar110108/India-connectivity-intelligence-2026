from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "market_indicators.csv"
OUT = ROOT / "analysis" / "derived_metrics.csv"
JSON_OUT = ROOT / "analysis" / "derived_metrics.json"

df = pd.read_csv(DATA)
df["value"] = pd.to_numeric(df["value"], errors="raise")
if df["source_id"].isna().any():
    raise ValueError("Every observation must have a source id.")

def value(metric, period):
    rows = df[(df["metric"] == metric) & (df["period"] == period)]
    if len(rows) != 1:
        raise ValueError(f"Expected one row for {metric} / {period}; found {len(rows)}")
    return float(rows.iloc[0]["value"])

internet_mar = value("internet_subscribers", "2026-03-31")
internet_jun = value("internet_subscribers", "2026-06-30")
broadband_mar = value("broadband_subscribers", "2026-03-31")
broadband_jun = value("broadband_subscribers", "2026-06-30")
urban_density = value("urban_internet_subscribers_per_100_population", "2026-06-30")
rural_density = value("rural_internet_subscribers_per_100_population", "2026-06-30")
fwa_total = value("fwa_5g_subscribers", "2026-08-31")
fwa_rural = value("fwa_5g_subscribers_rural", "2026-08-31")
fwa_urban = value("fwa_5g_subscribers_urban", "2026-08-31")
jio_broadband = value("jio_broadband_subscribers", "2026-08-31")
broadband_with_m2m = value("broadband_subscribers_with_m2m", "2026-08-31")

metrics = [
    {
        "metric": "internet_subscriber_growth_mar_to_jun_2026",
        "value": round((internet_jun - internet_mar) / internet_mar * 100, 2),
        "unit": "percent",
        "formula": "(June subscribers - March subscribers) / March subscribers * 100",
        "scope": "TRAI quarterly performance indicators series"
    },
    {
        "metric": "internet_subscriber_change_mar_to_jun_2026",
        "value": round(internet_jun - internet_mar, 2),
        "unit": "million",
        "formula": "June subscribers - March subscribers",
        "scope": "TRAI quarterly performance indicators series"
    },
    {
        "metric": "broadband_subscriber_growth_mar_to_jun_2026",
        "value": round((broadband_jun - broadband_mar) / broadband_mar * 100, 2),
        "unit": "percent",
        "formula": "(June subscribers - March subscribers) / March subscribers * 100",
        "scope": "TRAI quarterly performance indicators series"
    },
    {
        "metric": "broadband_subscriber_change_mar_to_jun_2026",
        "value": round(broadband_jun - broadband_mar, 2),
        "unit": "million",
        "formula": "June subscribers - March subscribers",
        "scope": "TRAI quarterly performance indicators series"
    },
    {
        "metric": "urban_rural_internet_subscriber_density_gap_jun_2026",
        "value": round(urban_density - rural_density, 2),
        "unit": "subscriptions_per_100_population",
        "formula": "Urban subscriptions per 100 - rural subscriptions per 100",
        "scope": "Density of subscriptions, not unique people"
    },
    {
        "metric": "urban_to_rural_internet_subscriber_density_ratio_jun_2026",
        "value": round(urban_density / rural_density, 2),
        "unit": "ratio",
        "formula": "Urban subscriptions per 100 / rural subscriptions per 100",
        "scope": "Density ratio; not an individual-level access ratio"
    },
    {
        "metric": "rural_share_of_5g_fwa_aug_2026",
        "value": round(fwa_rural / fwa_total * 100, 2),
        "unit": "percent",
        "formula": "Rural 5G FWA subscriptions / total 5G FWA subscriptions * 100",
        "scope": "TRAI monthly subscription series"
    },
    {
        "metric": "jio_share_of_broadband_subscriptions_aug_2026",
        "value": round(jio_broadband / broadband_with_m2m * 100, 2),
        "unit": "percent",
        "formula": "Jio wired and wireless broadband subscriptions / total broadband subscriptions with M2M * 100",
        "scope": "Cross-checks the TRAI reported share; denominator includes M2M"
    }
]

if abs(fwa_rural + fwa_urban - fwa_total) > 0.001:
    raise ValueError("Urban and rural 5G FWA subscriptions do not reconcile to total.")
if round(jio_broadband / broadband_with_m2m * 100, 2) != 48.86:
    raise ValueError("Calculated Jio share does not match the reported rounded share.")

pd.DataFrame(metrics).to_csv(OUT, index=False)
JSON_OUT.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
print(pd.DataFrame(metrics).to_string(index=False))
