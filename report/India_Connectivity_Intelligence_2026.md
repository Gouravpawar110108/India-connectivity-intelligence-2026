# India Connectivity Intelligence 2026

## Market evidence, Jio's operating position, and conditional satellite use cases

**Prepared by Gourav Pawar**  
BBA-BIA student, LNCT Bhopal  
Evidence cut-off: 14 October 2026

---

## Executive summary

India's internet market kept expanding in the latest official quarterly series. From March to June 2026, total internet subscriptions rose by 21.38 million, or 1.96%; broadband subscriptions rose by 21.62 million, or 2.03%. These are subscription counts, not unique people. [S1, S2]

The national totals hide a large urban-rural difference in subscription density. At June 2026, TRAI reported 129.03 urban and 49.07 rural internet subscriptions per 100 population. That is a 79.96-subscription gap. Because people and businesses can hold more than one subscription, this is an account-density indicator rather than a direct estimate of people without internet. [S1]

Jio has a large mobile and home-connectivity base. For the quarter ended June 2026, Reliance reported 533.3 million Jio customers, about 285 million True5G users, 28.6 million fixed-broadband connections and 14.0 million JioAirFiber home connections. These are company-reported measures and should not be treated as identical to TRAI subscriber definitions. [S4]

Satellite connectivity is a potential complement where terrestrial service is absent, unreliable, or costly to extend. Government sources record Starlink's DoT Unified License and an IN-SPACe Gen1 capacity approval. The reviewed official material did not establish current retail availability or India pricing; the interactive Starlink availability map did not expose a readable country status in this review. A licence or capacity approval alone is not proof of commercial launch or customer uptake. [S6, S7]

**Decision implication:** Use public data to identify where to investigate, not to claim which customers are dissatisfied or ready to switch. Jio can measure fixed-broadband quality and retention by service type and location. Any Starlink market estimate should wait for verified availability, price, performance, installation, and support terms. Customer recommendations need primary research.

## 1. Question and scope

This report asks: How can Reliance Jio strengthen customer growth and retention while satellite internet creates potential connectivity options for underserved areas of India?

The analysis covers official market measures, Jio's latest published operating metrics, the August 2026 connectivity mix, Starlink's recorded regulatory milestones, and a practical evidence plan. It does not claim to be a customer survey or a complete customer analytics study.

The report keeps four evidence types separate:

- **Regulator observations:** TRAI counts, definitions, and periods.
- **Company-reported observations:** Jio and RIL operating metrics.
- **Derived measures:** arithmetic calculated from the cited source values in Python.
- **Strategic hypotheses:** recommendations that need customer, coverage, and price validation.

## 2. Market momentum and monetisation

TRAI's annual indicators recorded 1,092.79 million internet subscriptions and 1,065.88 million broadband subscriptions at March 2026. The quarterly performance report for June 2026 recorded 1,114.17 million internet subscriptions and 1,087.50 million broadband subscriptions. The calculated March-to-June increases are 21.38 million (1.96%) and 21.62 million (2.03%), respectively. [S1, S2]

Wireless-service ARPU was INR 180.73 per month as a 2025-26 financial-year average. The April-June 2026 quarterly report recorded INR 187.12 per month. These values have different reporting periods; they are context, not a customer price or a directly comparable Jio offer. TRAI calculates ARPU from net subscriber revenue and average subscribers under its stated methodology. [S1, S2]

TRAI's FY2025-26 report also recorded annual broadband subscription growth of 12.90%. Growth indicates continued market expansion, but does not explain what caused it or prove that every location has reliable or affordable service. [S2]

## 3. Access remains uneven

For June 2026, TRAI reported 77.94 internet subscriptions per 100 population nationally, 129.03 in urban areas, and 49.07 in rural areas. The urban-rural difference is 79.96 subscriptions per 100 population; the urban density is about 2.63 times the rural density. [S1]

This is a meaningful signal for further investigation, not a count of connected people. It includes subscriptions rather than unique individuals, may reflect multiple SIMs or accounts, and says nothing by itself about speed, uptime, affordability, device access, or household sharing.

The August 2026 subscription release adds a useful fixed-wireless view. It recorded 13.45 million 5G FWA subscriptions, of which 6.98 million (51.90%) were rural and 6.47 million urban. Rural 5G FWA subscriptions already form a substantial part of the reported base. That means satellite should be tested against existing mobile, fixed-wireless, and wired alternatives rather than assumed to be the only rural option. [S3]

## 4. Jio's published position

In the quarter ended 30 June 2026, RIL reported Jio's total customer base at 533.3 million and net additions of 8.9 million. It reported about 285 million True5G users, an ARPU of INR 215.6 per month, and monthly churn of 1.6%. It also reported a 28.6 million fixed-broadband base, including 14.0 million JioAirFiber home connections. [S4]

These metrics provide a scale and operating baseline, not proof of customer satisfaction or service quality. The reported churn rate is a company KPI with a company-defined denominator. It should not be compared mechanically with an externally calculated churn measure.

The August TRAI subscription release reported 538.03 million Jio wired and wireless broadband subscriptions and a 48.86% share in its broadband provider table. The count includes mobile broadband; the separate Jio fixed-wired access count was 14.81 million. Neither number should be described as 538.03 million home broadband customers. [S3]

**Implication for Jio:** fixed connectivity is a large enough operating line to analyse separately. Track activation, installation time, outages, complaints, service upgrades, and cancellations for wired broadband and AirFiber separately. Break the measures down by service area and customer type before choosing retention or acquisition interventions.

## 5. Connectivity mix and the satellite question

TRAI's August release reported 1,101.21 million broadband subscriptions when M2M cellular mobile connections are included, and 1,010.28 million when M2M is excluded. Within the with-M2M figure, the reported components were 1,033.24 million mobile wireless, 48.63 million fixed wired, and 19.34 million fixed wireless broadband subscriptions. This monthly series must not be blended into the March-June quarterly performance series without reconciling scope and definitions. [S3]

The existing mix matters for strategic comparisons:

- **Mobile broadband** offers individual mobility and uses the handset or dongle as the endpoint.
- **Wired broadband** can provide fixed home or business access where fibre or other fixed infrastructure is available.
- **Fixed wireless access** can connect a location without a wired last-mile line; the August TRAI report includes both 5G FWA and UBR categories.
- **Satellite broadband** could be useful at remote or mobile sites where terrestrial infrastructure is limited, but the commercial case depends on terminal cost, recurring price, availability, capacity, latency, weather resilience, installation, and support.

These are technology-level use cases, not measured customer preferences. In a target location, compare the full installed cost and service quality of fibre, fixed wireless, mobile, and satellite before recommending an option.

## 6. Starlink status: authorisation is not market availability

A Government of India backgrounder reports that Starlink Satellite Communications Pvt. Ltd. received a DoT Unified License on 6 June 2025 authorising GMPCS, Commercial VSAT, and ISP-A services nationwide. It also reports that IN-SPACe approved Gen1 satellite constellation capacity for India for five years on 8 July 2025. [S6]

The Starlink availability map is the relevant company channel for a country-specific status, but its dynamic country status could not be read reliably in this review. The reviewed primary-source material therefore does not establish whether consumer service is currently orderable in India or what India-specific consumer prices and service terms are. No market-size, customer-demand, or market-share forecast is made here. [S7]

**Strategic hypothesis:** Satellite may be most useful for locations where terrestrial options are absent or fail a defined reliability threshold, and for institutional, enterprise, or backhaul use cases with a high cost of disconnection. This remains a hypothesis until availability, pricing, service-level data, and customer research are verified.

## 7. Recommendations

| Priority | Recommendation | Evidence link | Confidence |
| --- | --- | --- | --- |
| 1 - Jio | Instrument wired broadband and AirFiber separately: installation lead time, first-month failures, uptime, complaints, upgrades, and cancellation by service area. Use this to identify fixable retention issues before broad promotional changes. | Jio reports 28.6 million fixed broadband connections and 14.0 million AirFiber connections. [S4] | High that measurement is useful; the underlying pain points are unverified. |
| 2 - Jio | Combine TRAI area-level subscription patterns with Jio's serviceability and quality data to prioritise local expansion. Test fibre and FWA economics location by location. | Rural/urban density differs; 5G FWA is already present in rural areas. [S1, S3] | Medium; detailed local coverage and cost data are needed. |
| 3 - Starlink | Before estimating India's addressable market, verify retail orderability, approved service areas, terminal and installation costs, monthly price, performance, capacity, support, and regulatory conditions. | Official sources confirm authorisation milestones, but the map did not reveal current country status here. [S6, S7] | High that these inputs are prerequisites. |
| 4 - Joint market research | Run an opt-in, anonymised exploratory survey and interviews across rural/urban locations and connectivity types. Ask about current access, reliability, budget, installation costs, and alternatives. Publish sample size and recruitment method; do not call a convenience sample representative. | No customer-level evidence was available for this report. | High that this evidence is needed; no customer result is assumed. |
| 5 - Portfolio build | Build a Power BI dashboard with separate pages for market trends, area opportunity, Jio operating metrics, satellite readiness, and metric definitions. Keep source, period, unit, and scope visible. | Current data mix has different reporting grains and definitions. [S1-S4] | High. |

## 8. Analytics plan and KPIs

The next analytical phase should add customer evidence without blurring it with public statistics.

1. **Public market table:** retain one row per metric, source, reporting period, unit, and definition. Update only from the original source.
2. **Customer survey:** record consent, recruitment channel, geography, current connectivity, spend bands, reliability, support, switching intention, and reactions to explicit hypothetical offers. Keep personally identifying fields out.
3. **Customer modelling:** use actual customer-level data only if it is lawfully available and safe to analyse. If synthetic rows are later used to demonstrate code, label them synthetic and do not claim real-world model accuracy.
4. **Power BI:** display source type and data period, show calculated measures separately, and prevent monthly and quarterly series from being joined without definition checks.

Recommended measures include internet and broadband subscription growth, rural/urban subscription density, wireless ARPU with period labels, wired/FWA installation completion, service uptime, complaint rate, fixed-broadband churn, survey satisfaction, and stated price acceptance. Customer measures should be reported only after an actual sample or dataset exists.

## 9. Limitations and conclusion

This report is descriptive. It does not identify why subscriptions changed, establish causality, measure customer satisfaction, estimate willingness to pay, forecast Starlink adoption, or predict Jio churn. The source data has different reporting periods, units, and denominators. Subscription counts can exceed the number of people and are not a direct measure of unique individuals connected.

The analysis also lacks fine-grained coverage, quality-of-service, household, and customer data. The Starlink status check could not read the dynamic official availability map. These gaps are material to the commercial conclusions.

India's market scale, the lower rural subscription density, Jio's published fixed-broadband scale, and the rural presence of 5G FWA justify more targeted analysis. They do not prove that a specific group wants satellite service or that satellite is the best solution. The next useful step is to join location-level service and quality data with a carefully sampled customer study, then compare terrestrial and satellite options on total cost and service performance.

## Sources

See [references/sources.md](../references/sources.md) for titles, dates, direct URLs, metric definitions, and scope notes. Source markers [S1]-[S7] throughout this report map to that register.
