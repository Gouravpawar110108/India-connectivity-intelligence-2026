from pathlib import Path
from html import escape
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Flowable

ROOT=Path(__file__).resolve().parents[1]
D=pd.read_csv(ROOT/"data/market_indicators.csv")
D["value"]=pd.to_numeric(D["value"])
M=pd.read_csv(ROOT/"analysis/derived_metrics.csv")
OUT=ROOT/"report/India_Connectivity_Intelligence_2026.pdf"
def v(metric,period):
    r=D[(D.metric==metric)&(D.period==period)]
    if len(r)!=1: raise ValueError(metric+" "+period)
    return float(r.iloc[0].value)
def m(metric):
    r=M[M.metric==metric]
    if len(r)!=1: raise ValueError(metric)
    return float(r.iloc[0].value)
try:
    pdfmetrics.registerFont(TTFont("ArialX",r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("ArialXB",r"C:\Windows\Fonts\arialbd.ttf"))
    F,FB="ArialX","ArialXB"
except Exception:
    F,FB="Helvetica","Helvetica-Bold"
NAVY=colors.HexColor("#10243A"); BLUE=colors.HexColor("#2B6E9F")
TEAL=colors.HexColor("#168C8C"); GOLD=colors.HexColor("#E59B32")
PALE=colors.HexColor("#EEF3F7"); INK=colors.HexColor("#263746")
MID=colors.HexColor("#5A6B7B"); LINE=colors.HexColor("#D7E0E8")
S=getSampleStyleSheet()
S.add(ParagraphStyle(name="BodyX",fontName=F,fontSize=9.1,leading=13,textColor=INK,spaceAfter=7))
S.add(ParagraphStyle(name="SmallX",fontName=F,fontSize=7.5,leading=9.5,textColor=MID,spaceAfter=4))
S.add(ParagraphStyle(name="H1X",fontName=FB,fontSize=19,leading=23,textColor=NAVY,spaceAfter=10))
S.add(ParagraphStyle(name="H2X",fontName=FB,fontSize=12.5,leading=15,textColor=BLUE,spaceBefore=3,spaceAfter=6))
S.add(ParagraphStyle(name="CoverX",fontName=FB,fontSize=29,leading=34,textColor=NAVY,spaceAfter=12))
S.add(ParagraphStyle(name="SubX",fontName=F,fontSize=14,leading=19,textColor=BLUE,spaceAfter=15))
S.add(ParagraphStyle(name="HeadX",fontName=FB,fontSize=7.8,leading=9.5,textColor=colors.white))
S.add(ParagraphStyle(name="CellX",fontName=F,fontSize=7.5,leading=9.8,textColor=INK))
S.add(ParagraphStyle(name="CellS",fontName=F,fontSize=7.0,leading=9.0,textColor=INK))
S.add(ParagraphStyle(name="RefX",fontName=F,fontSize=8,leading=11,textColor=INK,spaceAfter=8))
def P(t,style="BodyX"): return Paragraph(t,S[style])
def T(t,style="BodyX"): return P(escape(t),style)
def grid(rows,widths,small=False):
    tab=Table(rows,colWidths=widths,repeatRows=1)
    tab.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("GRID",(0,0),(-1,-1),0.45,LINE),
        ("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),
        ("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,PALE])]))
    return tab
class Bars(Flowable):
    def __init__(self,title,labels,vals,suffix="",subtitle=""):
        super().__init__(); self.title=title; self.labels=labels; self.vals=vals
        self.suffix=suffix; self.subtitle=subtitle; self.height=174
    def wrap(self,w,h): self.width=w; return w,self.height
    def draw(self):
        c=self.canv; w=self.width
        c.setFillColor(NAVY); c.setFont(FB,10); c.drawString(0,self.height-14,self.title)
        c.setFillColor(MID); c.setFont(F,7.3); c.drawString(0,self.height-27,self.subtitle)
        base=34; top=self.height-45; ch=top-base; mx=max(self.vals)*1.16
        slot=w/len(self.vals); bw=min(72,slot*.42)
        c.setStrokeColor(LINE); c.line(4,base,w-4,base)
        cols=[BLUE,TEAL,GOLD]
        for i,(lab,val) in enumerate(zip(self.labels,self.vals)):
            xm=slot*(i+.5); bh=ch*val/mx
            c.setFillColor(cols[i%len(cols)]); c.roundRect(xm-bw/2,base,bw,bh,4,fill=1,stroke=0)
            c.setFillColor(NAVY); c.setFont(FB,9); c.drawCentredString(xm,base+bh+6,f"{val:.2f}{self.suffix}")
            c.setFillColor(INK); c.setFont(F,7.4); c.drawCentredString(xm,16,lab)
class Mix(Flowable):
    def __init__(self,title,labels,vals,note):
        super().__init__(); self.title=title; self.labels=labels; self.vals=vals; self.note=note; self.height=128
    def wrap(self,w,h): self.width=w; return w,self.height
    def draw(self):
        c=self.canv; w=self.width; total=sum(self.vals)
        c.setFillColor(NAVY); c.setFont(FB,10); c.drawString(0,self.height-14,self.title)
        x=4; y=self.height-52; usable=w-8; cols=[BLUE,TEAL,GOLD]
        for lab,val,col in zip(self.labels,self.vals,cols):
            sw=usable*val/total; c.setFillColor(col); c.rect(x,y,sw,25,fill=1,stroke=0)
            if sw>36:
                c.setFillColor(colors.white); c.setFont(FB,7); c.drawCentredString(x+sw/2,y+8,f"{val:.2f}M")
            x+=sw
        x=4; y=25
        for lab,val,col in zip(self.labels,self.vals,cols):
            c.setFillColor(col); c.rect(x,y,8,8,fill=1,stroke=0)
            c.setFillColor(INK); c.setFont(F,7)
            c.drawString(x+12,y-1,f"{lab}: {val:.2f}M ({val/total*100:.1f}%)")
            x+=w/3
        c.setFillColor(MID); c.setFont(F,6.8); c.drawString(4,7,self.note)
def page(canvas,doc):
    if doc.page==1: return
    canvas.saveState(); w,h=letter
    canvas.setStrokeColor(LINE); canvas.line(doc.leftMargin,h-34,w-doc.rightMargin,h-34)
    canvas.setFillColor(MID); canvas.setFont(F,7)
    canvas.drawString(doc.leftMargin,h-26,"INDIA CONNECTIVITY INTELLIGENCE 2026")
    canvas.drawRightString(w-doc.rightMargin,24,f"Evidence cut-off: 14 Oct 2026  |  {doc.page}")
    canvas.restoreState()
def ref(tag,title,url):
    return P(f'<b>{tag}</b> <link href="{escape(url,quote=True)}" color="#2B6E9F">{escape(title)}</link>',"RefX")

doc=SimpleDocTemplate(str(OUT),pagesize=letter,leftMargin=.62*inch,rightMargin=.62*inch,topMargin=.62*inch,bottomMargin=.54*inch,title="India Connectivity Intelligence 2026",author="Gourav Pawar")
W=doc.width; story=[]
# Cover
story += [Spacer(1,.85*inch),T("BUSINESS INTELLIGENCE PORTFOLIO REPORT","H2X"),
 T("India Connectivity Intelligence 2026","CoverX"),
 T("Market evidence, Jio's operating position, and conditional satellite use cases","SubX"),
 T("How can Jio strengthen customer growth and retention while satellite internet creates potential connectivity options for underserved areas of India?"),
 Spacer(1,.25*inch)]
cover=[[T("EVIDENCE CUT-OFF","SmallX"),T("PRIMARY SOURCES","SmallX"),T("AUTHOR","SmallX")],
 [T("14 October 2026","H2X"),T("TRAI, DoT, PIB, RIL","H2X"),T("Gourav Pawar","H2X")],
 [T("Latest official releases reviewed","SmallX"),T("No private customer data used","SmallX"),T("BBA-BIA, LNCT Bhopal","SmallX")]]
ct=Table(cover,colWidths=[W/3]*3,rowHeights=[20,26,25])
ct.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),PALE),("BOX",(0,0),(-1,-1),.7,LINE),("INNERGRID",(0,0),(-1,-1),.45,LINE),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),9)]))
story += [ct,Spacer(1,.3*inch),T("The report separates regulator observations, company-reported metrics, calculated comparisons, and strategic hypotheses. It does not present customer research or model results that were not observed."),PageBreak()]
# Executive summary
ig=m("internet_subscriber_growth_mar_to_jun_2026"); bg=m("broadband_subscriber_growth_mar_to_jun_2026")
story += [T("Executive summary","H1X"),T("India's connectivity market continued to expand in the latest official quarterly series. Rural subscription density remains materially lower than urban density, while Jio reports scale across mobile, 5G, and fixed broadband. Satellite connectivity is a conditional option; regulatory milestones alone do not establish retail readiness.")]
cards=[[T("INTERNET SUBSCRIPTIONS","SmallX"),T("BROADBAND SUBSCRIPTIONS","SmallX")],
 [T(f"{ig:.2f}%","H1X"),T(f"{bg:.2f}%","H1X")],
 [T("March-June change: +21.38M","SmallX"),T("March-June change: +21.62M","SmallX")],
 [T("RURAL DENSITY, JUNE","SmallX"),T("JIO CUSTOMER BASE, Q1 FY27","SmallX")],
 [T("49.07 / 100","H1X"),T("533.3M","H1X")],
 [T("vs 129.03 urban; subscriptions, not people","SmallX"),T("Company-reported","SmallX")]]
ct=Table(cards,colWidths=[W/2,W/2],rowHeights=[16,25,24,16,25,25])
ct.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),PALE),("BOX",(0,0),(-1,-1),.7,LINE),("INNERGRID",(0,0),(-1,-1),.45,LINE),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),9)]))
story += [ct,Spacer(1,8),T("What the evidence supports","H2X"),T("The market is expanding and Jio reports a large operating base. TRAI's June subscription-density figures point to a rural-urban gap, while August data show fixed wireless already serving rural locations. These observations support targeted measurement; they do not prove dissatisfaction, willingness to switch, demand for satellite, or a cause of growth."),T("Recommended direction","H2X"),T("For Jio, measure wired broadband and AirFiber quality and retention separately by service type and location. For Starlink, verify orderability, India price, footprint, installation, capacity, and support before estimating a market. Customer recommendations need primary research."),
 T("Source context: TRAI market data [S1-S3]; Jio company-reported data [S4].","SmallX"),PageBreak()]
# Scope
story += [T("1. Question, scope, and evidence","H1X"),T("This report asks how Jio can strengthen growth and retention while satellite internet creates potential connectivity options for underserved areas. It covers official market measures, Jio's latest published operating metrics, the August connectivity mix, and Starlink's recorded regulatory milestones. It is not a completed customer analytics study.")]
r=[[P("Evidence","HeadX"),P("Use in this report","HeadX"),P("Boundary","HeadX")],
 [P("TRAI observations","CellX"),P("Market totals, density, broadband mix","CellX"),P("Subscriptions can include multiple accounts and M2M; period and definition matter.","CellX")],
 [P("RIL company data","CellX"),P("Jio base, True5G, ARPU, churn, fixed broadband","CellX"),P("Company definitions are not assumed identical to TRAI's.","CellX")],
 [P("Derived values","CellX"),P("Growth, density gap, FWA share","CellX"),P("Arithmetic from cited values; formulas are in analysis files.","CellX")],
 [P("Hypotheses","CellX"),P("Potential terrestrial/satellite use cases","CellX"),P("Not observed customer demand; needs local evidence.","CellX")]]
story += [grid(r,[105,150,W-255]),Spacer(1,9),T("Period discipline","H2X"),T("The annual TRAI series ends in March 2026; the latest quarterly performance report covers April-June 2026 and was published on 12 October; its monthly subscription release covers August 2026. RIL's latest located Jio presentation covers the quarter ended 30 June. Monthly and quarterly values remain separate."),T("No survey responses, customer records, synthetic records, or third-party estimates were used.", "BodyX"),PageBreak()]
# Market momentum
story += [T("2. Market momentum","H1X"),T("TRAI's quarterly performance series shows continued growth between March and June 2026. The calculations use the same series and end-of-quarter dates.")]
story += [Bars("March-June 2026 growth in TRAI subscription counts",["Internet","Broadband"],[ig,bg],"%","Calculated from reported quarter-end counts"),
 T("Internet subscriptions increased from 1,092.79 million to 1,114.17 million, a gain of 21.38 million (1.96%). Broadband subscriptions increased from 1,065.88 million to 1,087.50 million, a gain of 21.62 million (2.03%). [S1, S2]"),
 T("TRAI's FY2025-26 annual report recorded broadband subscription growth of 12.90%. This describes market expansion; it does not explain the drivers or show that service quality improved everywhere. [S2]"),
 T("Wireless-service ARPU was INR 180.73 per month as a 2025-26 financial-year average and INR 187.12 for the April-June 2026 quarter. These periods differ, and neither value is a customer plan price. [S1, S2]"),
 T("Interpretation","H2X"),T("Growth creates room for acquisition, but retention and monetisation depend on local quality, usage, affordability, and availability. Those customer-level drivers are absent from public aggregates."),PageBreak()]
# Rural and urban
u=v("urban_internet_subscribers_per_100_population","2026-06-30")
r=v("rural_internet_subscribers_per_100_population","2026-06-30")
gap=m("urban_rural_internet_subscriber_density_gap_jun_2026")
ratio=m("urban_to_rural_internet_subscriber_density_ratio_jun_2026")
story += [T("3. Access is uneven across urban and rural India","H1X"),
 T(f"At June 2026, TRAI reported {u:.2f} urban and {r:.2f} rural internet subscriptions per 100 population. The difference is {gap:.2f}; urban density is approximately {ratio:.2f} times rural density. [S1]"),
 Bars("Internet subscriptions per 100 population, June 2026",["Urban","Rural"],[u,r],"","Subscription density, not unique-person adoption"),
 T("These values can exceed 100 because a person or organisation may hold multiple subscriptions. The metric is useful as a population-normalised indicator, but it is not the share of people online or a count of people without service."),
 T("TRAI's August release recorded 13.45 million 5G fixed-wireless-access subscriptions: 6.98 million rural and 6.47 million urban. Rural subscriptions accounted for 51.90% of that base. This shows fixed wireless is already one option in some rural locations; it does not establish quality or demand for satellite. [S3]"),
 T("Use the signal carefully","H2X"),T("Prioritise local checks of serviceability, uptime, actual speed, affordability, and customer experience. National subscription density is not a district-level coverage map."),PageBreak()]
# Jio position
story += [T("4. Jio's published operating position","H1X"),T("For Q1 FY2026-27, the quarter ended 30 June 2026, Reliance Industries reported the following Jio operating measures. [S4]")]
jr=[[P("Metric","HeadX"),P("Q1 FY27 value","HeadX"),P("Reading note","HeadX")],
 [P("Total customer base","CellX"),P("533.3 million","CellX"),P("Company-reported; not assumed equivalent to TRAI count.","CellX")],
 [P("Net customer additions","CellX"),P("8.9 million","CellX"),P("Quarterly additions; not a retention rate.","CellX")],
 [P("True5G users","CellX"),P("About 285 million","CellX"),P("Company-reported technology adoption measure.","CellX")],
 [P("ARPU","CellX"),P("INR 215.6 per month","CellX"),P("Company-defined average revenue per user.","CellX")],
 [P("Monthly churn","CellX"),P("1.6%","CellX"),P("Company-reported; retain its definition and denominator.","CellX")],
 [P("Fixed-broadband base","CellX"),P("28.6 million","CellX"),P("Company-reported fixed-broadband operating base.","CellX")],
 [P("JioAirFiber home connections","CellX"),P("14.0 million","CellX"),P("Company-reported home connections.","CellX")]]
story += [grid(jr,[132,128,W-260]),Spacer(1,8),
 T("The August TRAI release separately lists 538.03 million Jio broadband subscriptions and a 48.86% provider share. That total includes wired and wireless broadband, including mobile. TRAI reports 14.81 million Jio fixed-wired subscriptions in the same release. These values answer different questions from RIL's June report; do not call 538.03 million home broadband customers. [S3]"),
 T("Management question","H2X"),T("Given Jio's fixed-broadband scale, analyse service quality and retention separately for wired broadband and AirFiber, by service area, installation cohort, and customer type. Public data does not show which cohort has a problem."),PageBreak()]
# Connectivity mix
mobile=v("mobile_wireless_access_broadband_subscribers","2026-08-31")
wired=v("fixed_wired_broadband_subscribers","2026-08-31")
fwa=v("fixed_wireless_access_broadband_subscribers","2026-08-31")
fwar=v("fwa_5g_subscribers_rural","2026-08-31")
fwau=v("fwa_5g_subscribers_urban","2026-08-31")
story += [T("5. The August broadband mix","H1X"),
 T("TRAI's August monthly series reports 1,101.21 million broadband subscriptions with M2M and 1,010.28 million without M2M. The components below reconcile to the with-M2M total. Do not blend this series into March-June quarterly growth without reconciling scope. [S3]"),
 Mix("August 2026 broadband subscriptions with M2M",["Mobile wireless","Fixed wired","Fixed wireless"],[mobile,wired,fwa],"Source: TRAI. Fixed wireless includes 5G FWA and UBR."),
 T("Within 19.34 million fixed-wireless subscriptions, TRAI lists 13.45 million as 5G FWA. The chart compares its rural and urban totals. [S3]"),
 Bars("5G FWA subscriptions by area, August 2026",["Rural","Urban"],[fwar,fwau],"M","TRAI monthly subscription series"),
 T("Mobile remains the largest category in the reported total. Fixed wireless is smaller but includes millions of rural subscriptions. Satellite should be compared against alternatives at a specific location; the national mix alone cannot determine the best technology."),PageBreak()]
# Starlink status
story += [T("6. Starlink: authorisation is not market availability","H1X"),
 T("A Government of India backgrounder reports two India-specific milestones for Starlink Satellite Communications Pvt. Ltd. [S6]")]
sr=[[P("Date","HeadX"),P("Milestone","HeadX"),P("What it establishes","HeadX")],
 [P("6 June 2025","CellX"),P("DoT Unified License authorising GMPCS, Commercial VSAT, and ISP-A services nationwide.","CellX"),P("Authorisation scope.","CellX")],
 [P("8 July 2025","CellX"),P("IN-SPACe approval for Gen1 constellation capacity in India for five years.","CellX"),P("Capacity approval for the stated term.","CellX")]]
story += [grid(sr,[78,260,W-338]),Spacer(1,10),T("What is still needed for a market claim","H2X"),
 T("Authorisation is not proof of retail orderability, commercial launch, service footprint, India pricing, terminal cost, installation, service quality, support, subscribers, or market share. The official availability map loaded, but its interactive country status could not be read reliably here. These facts remain unverified in this report. [S6, S7]"),
 T("Strategic hypothesis","H2X"),
 T("Satellite may fit remote households, business sites, public-service locations, or network backhaul where terrestrial options are unavailable or fail a defined service threshold. This is a hypothesis, not a measured customer segment. Compare total cost, availability, latency, reliability, capacity, installation, and support against fibre, fixed wireless, and mobile at the target location."),
 T("No India-specific Starlink price or market-share estimate is included."),PageBreak()]
# Recommendations
story += [T("7. Prioritised recommendations","H1X")]
rr=[[P("Priority","HeadX"),P("Action","HeadX"),P("Evidence and confidence","HeadX")],
 [P("1 - Jio","CellX"),P("Measure wired broadband and AirFiber separately: installation time, first-month failures, uptime, complaints, upgrades, and cancellations by service area and customer type.","CellS"),P("The reported 28.6M fixed base and 14.0M AirFiber base support measurement; specific pain points are unverified. [S4]","CellS")],
 [P("2 - Jio","CellX"),P("Combine serviceability and quality data with TRAI area patterns to prioritise local expansion; test fibre and FWA economics by location.","CellS"),P("Urban-rural density differs; rural 5G FWA exists. Local cost and coverage data are needed. [S1, S3]","CellS")],
 [P("3 - Starlink","CellX"),P("Verify orderability, footprint, terminal and installation cost, price, capacity, performance, support, and regulatory conditions before estimating demand.","CellS"),P("Authorisation is documented; current retail availability was not verified here. [S6, S7]","CellS")],
 [P("4 - Research","CellX"),P("Run an opt-in exploratory survey and interviews across locations and connectivity types. Publish recruitment method and actual sample size.","CellS"),P("No customer-level evidence was available. A convenience sample is not representative.","CellS")],
 [P("5 - Analytics","CellX"),P("Build a Power BI report with separate market, customer, retention, opportunity, and definitions pages; show source and period.","CellS"),P("Measures have different reporting grains. No .pbix is included in this release. [S1-S4]","CellS")]]
story += [grid(rr,[66,W*.48,W-66-W*.48]),Spacer(1,10),T("Decision rule","H2X"),
 T("Do not choose a technology or customer offer from national subscription totals alone. Compare target-location serviceability, total installed and recurring costs, speed, latency, uptime, installation lead time, and support."),PageBreak()]
# Analytics plan and limits
story += [T("8. Next analytics phase","H1X"),T("Customer analytics can begin when primary data is available and the sample is documented.")]
pr=[[P("Data layer","HeadX"),P("Minimum fields","HeadX"),P("Analysis enabled","HeadX")],
 [P("Public market","CellX"),P("Source, date, period, value, unit, definition, geography.","CellX"),P("Trends, growth, provider mix, density.","CellX")],
 [P("Survey","CellX"),P("Consent, coarse geography, access type, spend band, reliability, satisfaction, switching, hypothetical offer reaction.","CellX"),P("Exploratory profiles and stated price acceptance; report sample limits.","CellX")],
 [P("Customer records","CellX"),P("Lawful anonymised events, tenure, spend, service, complaints, cancellation and outcome window.","CellX"),P("Churn/retention with baseline, time split, leakage checks, validation.","CellX")],
 [P("Service readiness","CellX"),P("Availability, installation cost/time, performance, support, capacity, approval status.","CellX"),P("Technology comparison for named locations.","CellX")]]
story += [grid(pr,[90,220,W-310]),Spacer(1,9),T("Survey safeguards","H2X"),
 T("Make participation voluntary, explain intended use, avoid names and phone numbers, and publish recruitment method and response count. A 100-200 response target can be exploratory, not representative. Use neutral wording for price and switching questions."),
 T("Limitations and conclusion","H2X"),
 T("This report is descriptive. It does not explain why subscriptions changed, establish causality, measure satisfaction, estimate willingness to pay, forecast Starlink adoption, or predict churn. Subscription counts can include multiple accounts and M2M. June quarterly and August monthly series differ in scope; company measures use company definitions. The analysis lacks household-level coverage, quality, price, and installation data, and the Starlink map status was unreadable."),
 T("India's market scale, lower rural subscription density, Jio's fixed-broadband scale, and rural 5G FWA presence justify targeted work. They do not prove that a customer group wants satellite or that it is the best option. The next step is to combine location-level service data with a carefully sampled customer study and compare options on total cost and performance."),
 T("Included in this release: report, source register, public-data extract, Python calculations, example SQL, dashboard plan, and LinkedIn draft. No survey, customer model, Power BI file, GitHub push, or LinkedIn publication is included."),PageBreak()]
# Sources
story += [T("Sources","H1X"),T("Official primary sources retrieved on 14 October 2026. Full definitions and scope notes appear in references/sources.md.")]
sources=[
 ("[S1]","TRAI, The Indian Telecom Services Performance Indicators, April-June 2026 (published 12 October 2026).","https://www.trai.gov.in/sites/default/files/2026-10/QPIR_12102026.pdf"),
 ("[S2]","TRAI, The Indian Telecom Services Yearly Performance Indicators 2025-26 (published 5 October 2026).","https://www.trai.gov.in/sites/default/files/2026-10/YIR_05102026_0.pdf"),
 ("[S3]","TRAI, Telecom Subscription Data at the end of August 2026 (published 28 September 2026).","https://www.trai.gov.in/sites/default/files/2026-09/PR_No125of2026_0.pdf"),
 ("[S4]","Reliance Industries, Q1 FY2026-27 Financial Results Presentation (published 17 July 2026).","https://www.ril.com/sites/default/files/2026-07/Presentation_for_RIL_Analyst_Meeting_v17072026.pdf"),
 ("[S5]","Department of Telecommunications, National Broadband Mission 2.0.","https://www.dot.gov.in/static/uploads/2025/07/c7c060d6fec6ac6bb73230c65f134909.pdf"),
 ("[S6]","PIB, Leap Beyond: Elevating India's Space Saga (Starlink India authorisation milestones).","https://www.pib.gov.in/PressNoteDetails.aspx?ModuleId=3&NoteId=154955&reg=3&lang=2"),
 ("[S7]","Starlink, Availability Map (country status could not be read reliably in this review).","https://starlink.com/map")]
for tag,title,url in sources: story.append(ref(tag,title,url))
story += [Spacer(1,5),T("Growth formula: (current value - prior value) / prior value x 100. Urban-rural gap: urban subscriptions per 100 population minus rural subscriptions per 100. Rural FWA share: rural 5G FWA subscriptions divided by all 5G FWA subscriptions. Derived metrics are rounded to two decimals.")]
doc.build(story,onFirstPage=page,onLaterPages=page)
print("Created "+str(OUT))
