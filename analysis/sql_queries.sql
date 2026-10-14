-- Assumes market_indicators is loaded from data/market_indicators.csv.
-- Each row is an observation with source_id, period, unit, and scope notes.

-- March-to-June growth in the TRAI quarterly performance series.
SELECT
    current.metric,
    current.unit,
    previous.value AS march_value,
    current.value AS june_value,
    ROUND(current.value - previous.value, 2) AS absolute_change,
    ROUND((current.value - previous.value) / previous.value * 100, 2) AS growth_percent
FROM market_indicators AS current
JOIN market_indicators AS previous
  ON previous.metric = current.metric
WHERE current.period = '2026-06-30'
  AND previous.period = '2026-03-31'
  AND current.metric IN ('internet_subscribers', 'broadband_subscribers');

-- Rural and urban internet subscription density. These are subscriptions per 100,
-- not unique-person adoption rates.
SELECT
    MAX(CASE WHEN metric = 'urban_internet_subscribers_per_100_population' THEN value END) AS urban_per_100,
    MAX(CASE WHEN metric = 'rural_internet_subscribers_per_100_population' THEN value END) AS rural_per_100
FROM market_indicators
WHERE period = '2026-06-30';

-- August 2026 rural share of 5G fixed wireless access subscriptions.
SELECT
    rural.value AS rural_5g_fwa_million,
    total.value AS all_5g_fwa_million,
    ROUND(rural.value / total.value * 100, 2) AS rural_share_percent
FROM market_indicators AS rural
JOIN market_indicators AS total
  ON total.metric = 'fwa_5g_subscribers'
 AND total.period = rural.period
WHERE rural.metric = 'fwa_5g_subscribers_rural'
  AND rural.period = '2026-08-31';

-- Do not join company metrics to TRAI values as if they share a definition.
-- Keep company-reported Jio KPIs and regulator subscription counts in separate views.
