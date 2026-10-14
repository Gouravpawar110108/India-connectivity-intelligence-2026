-- 1) 5G FWA national trend. Sum regional all-provider totals only.
WITH monthly_total AS (
    SELECT period_end, SUM(value) AS subscriptions
    FROM fact_connectivity
    WHERE metric_id = 'fwa_5g_all_provider_total'
      AND provider = 'All providers'
    GROUP BY period_end
), trend AS (
    SELECT period_end, subscriptions,
           LAG(subscriptions) OVER (ORDER BY period_end) AS prior_subscriptions
    FROM monthly_total
)
SELECT period_end, subscriptions,
       subscriptions - prior_subscriptions AS net_change,
       ROUND(100.0 * (subscriptions - prior_subscriptions) / NULLIF(prior_subscriptions, 0), 2) AS growth_pct
FROM trend
ORDER BY period_end;

-- 2) Top 10 TRAI service areas by 5G FWA subscriptions in the latest month.
WITH latest_period AS (
    SELECT MAX(period_end) AS period_end
    FROM fact_connectivity
    WHERE metric_id = 'fwa_5g_all_provider_total'
      AND provider = 'All providers'
)
SELECT f.geography, f.value AS subscriptions, f.period_end
FROM fact_connectivity AS f
JOIN latest_period AS p USING (period_end)
WHERE f.metric_id = 'fwa_5g_all_provider_total'
  AND f.provider = 'All providers'
ORDER BY f.value DESC
LIMIT 10;

-- 3) Wireline provider shares in a selected service area and period.
-- The denominator is TRAI's reported area total; never add the All providers row to provider rows.
WITH provider_rows AS (
    SELECT geography, period_end, provider, value
    FROM fact_connectivity
    WHERE metric_id = 'wireline_subscriber_base'
      AND provider <> 'All providers'
      AND geography = 'Andhra Pradesh'
      AND period_end = '2026-07-31'
), reported_total AS (
    SELECT geography, period_end, value AS total_value
    FROM fact_connectivity
    WHERE metric_id = 'wireline_subscriber_base'
      AND provider = 'All providers'
      AND geography = 'Andhra Pradesh'
      AND period_end = '2026-07-31'
)
SELECT p.provider, p.value AS subscriptions,
       ROUND(100.0 * p.value / NULLIF(t.total_value, 0), 2) AS reported_total_share_pct
FROM provider_rows AS p
JOIN reported_total AS t USING (geography, period_end)
ORDER BY p.value DESC;

-- 4) Period-over-period wireline total movement.
WITH monthly_total AS (
    SELECT period_end, SUM(value) AS subscriptions
    FROM fact_connectivity
    WHERE metric_id = 'wireline_subscriber_base'
      AND provider = 'All providers'
    GROUP BY period_end
), compare_periods AS (
    SELECT period_end, subscriptions,
           LAG(subscriptions) OVER (ORDER BY period_end) AS prior_subscriptions
    FROM monthly_total
)
SELECT period_end, subscriptions, prior_subscriptions,
       subscriptions - prior_subscriptions AS net_change,
       ROUND(100.0 * (subscriptions - prior_subscriptions) / NULLIF(prior_subscriptions, 0), 2) AS growth_pct
FROM compare_periods
ORDER BY period_end;

-- 5) UBR counts by area and period (Jio only in TRAI's cited reports).
SELECT period_end, geography, value AS subscriptions
FROM fact_connectivity
WHERE metric_id = 'fwa_ubr_subscriber_base'
  AND provider = 'Reliance Jio'
ORDER BY period_end, subscriptions DESC;
