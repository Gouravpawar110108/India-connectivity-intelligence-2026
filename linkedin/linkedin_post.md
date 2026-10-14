# LinkedIn post draft

I’m sharing an update to my portfolio project: **India Connectivity Intelligence 2026**.

I used official TRAI monthly subscription reports to build a small, source-traceable data pipeline and an interactive dashboard covering April–July 2026. The repository includes the extracted data, a 1,000-row sample, cleaned fact and dimension tables, SQLite cleaning and KPI queries, a star-schema diagram, and a dashboard walkthrough.

One finding: reported 5G fixed wireless access subscriptions increased from **12.55 million in April to 13.21 million in July 2026**, a calculated **5.24%** increase. In July, Andhra Pradesh had the largest service-area total, followed by Uttar Pradesh (East), Maharashtra, Bihar and Tamil Nadu.

These are subscription counts, not unique people. The analysis is descriptive and does not claim service quality, customer satisfaction, churn or future demand. I kept TRAI-published aggregate totals separate from provider rows to avoid double-counting.

I also included the source PDFs and page-level references so the calculations can be reviewed and reproduced. The repository has an interactive HTML dashboard and Power BI/Tableau-ready CSVs; a native PBIX workbook is not included in this version.

Project and files: https://github.com/Gouravpawar110108/India-connectivity-intelligence-2026

Feedback on the data model, SQL KPIs or dashboard is welcome.

#DataAnalytics #PowerBI #Telecom #India #BusinessAnalytics #DataVisualization
