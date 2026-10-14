-- SQLite star schema. Load stg_trai_clean using 01_data_cleaning.sql first.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS dim_period (
    period_end TEXT PRIMARY KEY,
    calendar_year INTEGER NOT NULL,
    calendar_month INTEGER NOT NULL,
    month_label TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_geography (
    geography TEXT PRIMARY KEY,
    geography_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_provider (
    provider TEXT PRIMARY KEY,
    provider_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_metric (
    metric_id TEXT PRIMARY KEY,
    metric_name TEXT NOT NULL,
    default_unit TEXT NOT NULL,
    additive_at_grain INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS dim_source (
    source_id TEXT PRIMARY KEY,
    source_file TEXT NOT NULL,
    source_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_connectivity (
    observation_id INTEGER PRIMARY KEY,
    metric_id TEXT NOT NULL REFERENCES dim_metric(metric_id),
    period_end TEXT NOT NULL REFERENCES dim_period(period_end),
    geography TEXT NOT NULL REFERENCES dim_geography(geography),
    provider TEXT NOT NULL REFERENCES dim_provider(provider),
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    source_id TEXT NOT NULL REFERENCES dim_source(source_id),
    source_page INTEGER NOT NULL,
    scope_note TEXT,
    UNIQUE(metric_id, period_end, geography, provider, source_id, source_page)
);

INSERT OR IGNORE INTO dim_period(period_end, calendar_year, calendar_month, month_label)
SELECT DISTINCT period_end, CAST(strftime('%Y', period_end) AS INTEGER),
       CAST(strftime('%m', period_end) AS INTEGER), strftime('%b %Y', period_end)
FROM stg_trai_clean;

INSERT OR IGNORE INTO dim_geography(geography, geography_type)
SELECT DISTINCT geography,
       CASE WHEN geography = 'India' THEN 'National' ELSE 'TRAI service area' END
FROM stg_trai_clean;

INSERT OR IGNORE INTO dim_provider(provider, provider_type)
SELECT DISTINCT provider,
       CASE WHEN provider = 'All providers' THEN 'Source-reported total' ELSE 'Reported provider or segment' END
FROM stg_trai_clean;

INSERT OR IGNORE INTO dim_metric(metric_id, metric_name, default_unit, additive_at_grain)
SELECT DISTINCT metric_id, REPLACE(metric_id, '_', ' '), unit,
       CASE WHEN metric_id LIKE 'summary_%' OR unit = 'percent' THEN 0 ELSE 1 END
FROM stg_trai_clean;

INSERT OR IGNORE INTO dim_source(source_id, source_file, source_url)
SELECT DISTINCT source_id, source_file, source_url FROM stg_trai_clean;

INSERT OR IGNORE INTO fact_connectivity(
    observation_id, metric_id, period_end, geography, provider, value, unit,
    source_id, source_page, scope_note
)
SELECT ROW_NUMBER() OVER (ORDER BY period_end, metric_id, geography, provider, source_id),
       metric_id, period_end, geography, provider, value, unit, source_id, source_page, scope_note
FROM stg_trai_clean;
