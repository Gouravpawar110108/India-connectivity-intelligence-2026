# LinkedIn post draft

I’ve published a new BI portfolio project: **India Connectivity Intelligence 2026**.

The project turns official TRAI telecom subscription reports into a source-traceable data workflow and an interactive dashboard. It includes four headline KPIs, filters for measure, month, service area and provider, monthly and regional comparisons, source-row inspection, and a CSV export that follows the selected filters.

One finding from the April–July 2026 series: reported 5G fixed wireless access subscriptions increased from **12.55 million to 13.21 million**, a calculated **5.24%** change. The July month-over-month increase was **2.11%**. In July, Andhra Pradesh had the largest reported regional 5G FWA total, followed by Uttar Pradesh (East), Maharashtra, Bihar and Tamil Nadu.

These are subscription counts, not unique people. The analysis is descriptive and does not measure service quality, customer satisfaction, churn or future demand. I kept TRAI-reported aggregate totals separate from provider rows to avoid double-counting.

The repository includes the source PDFs and page-level references, extracted and cleaned CSVs, SQL cleaning and KPI queries, a star-schema diagram, the executive report, and the dashboard source. A native Power BI `.pbix` or Tableau workbook is not included in this release; the processed data is ready to import into either tool.

Project: https://github.com/Gouravpawar110108/India-connectivity-intelligence-2026

I’d welcome feedback on the data model, KPI definitions, or dashboard design.

#DataAnalytics #BusinessIntelligence #PowerBI #Telecom #India #DataVisualization
