-- SQLite staging and cleaning layer for the official TRAI extracts.
-- Import data/raw/trai_monthly_extracted_observations.csv to stg_trai_observations first.
-- Keep blanks NULL. A reported numeric zero is an observed zero, not a missing value.

DROP TABLE IF EXISTS stg_trai_observations;
CREATE TABLE stg_trai_observations (
    metric_id TEXT,
    period_end TEXT,
    geography TEXT,
    provider TEXT,
    value REAL,
    unit TEXT,
    source_id TEXT,
    source_file TEXT,
    source_page INTEGER,
    source_url TEXT,
    scope_note TEXT
);

DROP TABLE IF EXISTS stg_trai_clean;
CREATE TABLE stg_trai_clean AS
WITH normalized AS (
    SELECT
        NULLIF(TRIM(metric_id), '') AS metric_id,
        date(period_end) AS period_end,
        CASE
            WHEN TRIM(geography) IN ('J & K', 'Jammu & Kashmir') THEN 'Jammu & Kashmir'
            WHEN TRIM(geography) = 'U.P.(E)' THEN 'Uttar Pradesh (East)'
            WHEN TRIM(geography) IN ('U.P.(W)', 'U.P.(W )') THEN 'Uttar Pradesh (West)'
            ELSE NULLIF(TRIM(geography), '')
        END AS geography,
        CASE WHEN LOWER(TRIM(provider)) = 'total' THEN 'All providers'
             ELSE NULLIF(TRIM(provider), '') END AS provider,
        CAST(value AS REAL) AS value,
        NULLIF(TRIM(unit), '') AS unit,
        NULLIF(TRIM(source_id), '') AS source_id,
        NULLIF(TRIM(source_file), '') AS source_file,
        CAST(source_page AS INTEGER) AS source_page,
        NULLIF(TRIM(source_url), '') AS source_url,
        NULLIF(TRIM(scope_note), '') AS scope_note,
        ROW_NUMBER() OVER (
            PARTITION BY metric_id, date(period_end), TRIM(geography), TRIM(provider), source_id, source_page
            ORDER BY source_file
        ) AS duplicate_rank
    FROM stg_trai_observations
)
SELECT metric_id, period_end, geography, provider, value, unit,
       source_id, source_file, source_page, source_url, scope_note
FROM normalized
WHERE duplicate_rank = 1
  AND metric_id IS NOT NULL
  AND period_end IS NOT NULL
  AND geography IS NOT NULL
  AND provider IS NOT NULL
  AND value IS NOT NULL;

-- Review missing values and duplicates; do not silently convert nulls to zero.
SELECT metric_id, COUNT(*) AS rows, SUM(CASE WHEN value IS NULL THEN 1 ELSE 0 END) AS null_values
FROM stg_trai_observations
GROUP BY metric_id
ORDER BY metric_id;
