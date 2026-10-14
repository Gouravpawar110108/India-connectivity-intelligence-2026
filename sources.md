# Source register

All analysis is based on public materials. Evidence cut-off: 14 October 2026. Page numbers in the extracted CSVs are the printed PDF page positions (1-based).

| ID | Publisher | Publication | Period | Link |
| --- | --- | --- | --- | --- |
| S1 | Telecom Regulatory Authority of India (TRAI) | Quarterly Performance Indicators, April–June 2026 | Quarter ended 30 June 2026 | [Official PDF](https://www.trai.gov.in/sites/default/files/2026-10/QPIR_12102026.pdf) |
| S2 | TRAI | Yearly Performance Indicators, 2025–26 | Year ended 31 March 2026 | [Official PDF](https://www.trai.gov.in/sites/default/files/2026-10/YIR_05102026_0.pdf) |
| S3 | TRAI | Telecom Subscription Data, August 2026 | August 2026 | [Official PDF](https://www.trai.gov.in/sites/default/files/2026-09/PR_No125of2026_0.pdf) |
| S4 | Reliance Industries Limited | Q1 FY2026–27 Results Presentation | Quarter ended 30 June 2026 | [Official presentation](https://www.ril.com/sites/default/files/2026-07/Presentation_for_RIL_Analyst_Meeting_v17072026.pdf) |
| S5 | Department of Telecommunications | National Broadband Mission 2.0 | 2025 policy document | [Official PDF](https://www.dot.gov.in/static/uploads/2025/07/c7c060d6fec6ac6bb73230c65f134909.pdf) |
| S6 | Press Information Bureau | Leap Beyond: Elevating India's Space Saga | 2025 milestones | [Official backgrounder](https://www.pib.gov.in/PressNoteDetails.aspx?ModuleId=3&NoteId=154955&reg=3&lang=2) |
| S7 | Starlink | Availability map | Current company information | [Starlink map](https://starlink.com/map) |
| S8 | TRAI | Telecom Subscription Data, May 2026 | April and May 2026 annexure values | [Official PDF](https://trai.gov.in/sites/default/files/2026-06/PR_No78of2026_0.pdf) · [local copy](data/raw/TRAI_Telecom_Subscription_May_2026.pdf) |
| S9 | TRAI | Telecom Subscription Data, July 2026 | June and July 2026 annexure values | [Official PDF](https://trai.gov.in/sites/default/files/2026-08/PR_No116of2026_0.pdf) · [local copy](data/raw/TRAI_Telecom_Subscription_July_2026.pdf) |

## Monthly dashboard extraction

`analysis/prepare_public_dataset.py` extracts monthly wireline, 5G FWA, UBR fixed-wireless, broadband access-segment, selected provider-ranking and summary-table observations from S8 and S9. The script records source ID, filename, URL, page number, observation period, metric, geography, provider, unit and a scope note in `data/raw/trai_monthly_extracted_observations.csv` and `data/processed/fact_connectivity.csv`.

The clean table retains source-published totals and provider details in separate records. For a given metric and period, use the `All providers` aggregate where available or sum provider detail where the full set is explicitly available; do not add both. The regional 5G FWA totals reconcile to the report's published totals. Percentages, millions and connection counts have separate units and must not be mixed.

The report's quarterly, yearly, corporate and policy indicators retain their original periods and definitions. They are not interchangeable with the monthly service-area data. The Starlink map is dynamic; the project does not infer current local availability or price from it.
