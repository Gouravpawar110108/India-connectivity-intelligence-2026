"""Create a star-schema ERD and source-backed dashboard walkthrough GIF."""

from pathlib import Path
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "visuals"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#142B45"
BLUE = "#3275A6"
TEAL = "#148A83"
GOLD = "#D8902F"
INK = "#243447"
MUTED = "#63758A"
PALE = "#EEF3F7"
WHITE = "#FFFFFF"
LINE = "#D5DFE8"

def font(size, bold=False):
    path = Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf")
    if path.exists():
        return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()

def draw_box(draw, xy, title, fields, fill=WHITE):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=18, fill=fill, outline=LINE, width=2)
    draw.rounded_rectangle((x1, y1, x2, y1 + 58), radius=18, fill=NAVY)
    draw.rectangle((x1, y1 + 38, x2, y1 + 58), fill=NAVY)
    draw.text((x1 + 18, y1 + 15), title, font=font(23, True), fill=WHITE)
    y = y1 + 76
    for field in fields:
        draw.text((x1 + 18, y), field, font=font(18), fill=INK)
        y += 32

def build_erd():
    image = Image.new("RGB", (1800, 1080), "#F7F9FC")
    d = ImageDraw.Draw(image)
    d.text((70, 36), "India Connectivity Intelligence 2026", font=font(35, True), fill=NAVY)
    d.text((70, 84), "Star schema | one observed metric per period, service area, provider and source", font=font(20), fill=MUTED)
    fact = (585, 350, 1220, 765)
    boxes = {
        "FactConnectivity": fact,
        "DimPeriod": (90, 220, 500, 410),
        "DimGeography": (90, 650, 500, 850),
        "DimProvider": (1300, 220, 1710, 410),
        "DimMetric": (1300, 500, 1710, 690),
        "DimSource": (1300, 800, 1710, 980),
    }
    # Draw connectors before boxes; endpoint dots mark dimension-to-fact joins.
    connectors = [((500, 315), (585, 405)), ((500, 750), (585, 675)),
                  ((1300, 315), (1220, 405)), ((1300, 595), (1220, 555)),
                  ((1300, 890), (1220, 710))]
    for a, b in connectors:
        d.line((a, b), fill=BLUE, width=4)
        d.ellipse((a[0] - 7, a[1] - 7, a[0] + 7, a[1] + 7), fill=TEAL)
        d.ellipse((b[0] - 7, b[1] - 7, b[0] + 7, b[1] + 7), fill=TEAL)
    draw_box(d, boxes["FactConnectivity"], "FactConnectivity", [
        "observation_id (PK)", "period_end (FK)", "geography (FK)",
        "provider (FK)", "metric_id (FK)", "value | unit", "source_id | page | scope note",
    ], fill="#F0F7FA")
    draw_box(d, boxes["DimPeriod"], "DimPeriod", ["period_end (PK)", "calendar month"])
    draw_box(d, boxes["DimGeography"], "DimGeography", ["geography (PK)", "India / TRAI LSA"])
    draw_box(d, boxes["DimProvider"], "DimProvider", ["provider (PK)", "operator or reported total"])
    draw_box(d, boxes["DimMetric"], "DimMetric", ["metric_id (PK)", "metric name | default unit"])
    draw_box(d, boxes["DimSource"], "DimSource", ["source_id (PK)", "document | URL | page"])
    d.text((70, 1015), "Aggregate rows are retained separately. Filter to provider rows OR the reported all-provider total to avoid double counting.",
           font=font(18, True), fill=MUTED)
    image.save(OUT / "data_model_erd.png", optimize=True)

def build_gif():
    data = pd.read_csv(ROOT / "data" / "processed" / "fact_connectivity.csv")
    all_rows = data[(data.metric_id == "fwa_5g_all_provider_total") & (data.provider == "All providers")]
    frames = []
    for month in ("2026-06-30", "2026-07-31"):
        snapshot = all_rows[(all_rows.period_end == month) & (all_rows.geography != "India")]
        snapshot = snapshot.sort_values("value", ascending=False).head(8)
        total = all_rows[all_rows.period_end == month].value.sum() / 1_000_000
        date_label = "June 2026" if month.endswith("06-30") else "July 2026"
        image = Image.new("RGB", (1400, 900), "#F4F7FA")
        d = ImageDraw.Draw(image)
        d.rounded_rectangle((48, 40, 1352, 860), radius=28, fill=WHITE, outline=LINE, width=2)
        d.text((92, 78), "India Connectivity | 5G fixed wireless", font=font(34, True), fill=NAVY)
        d.text((92, 126), "Service-area snapshot | TRAI monthly subscription data", font=font(20), fill=MUTED)
        d.rounded_rectangle((92, 177, 550, 244), radius=14, fill=PALE)
        d.text((116, 198), "Metric  5G FWA subscriptions", font=font(19, True), fill=INK)
        d.rounded_rectangle((578, 177, 890, 244), radius=14, fill="#E6F3F1")
        d.text((601, 198), f"Period  {date_label}", font=font(19, True), fill=TEAL)
        d.text((970, 184), f"All India  {total:.2f}M", font=font(26, True), fill=NAVY)
        d.text((95, 286), "TRAI service area", font=font(18, True), fill=MUTED)
        d.text((1118, 286), "Subscriptions", font=font(18, True), fill=MUTED)
        left, right = 95, 1280
        max_value = snapshot.value.max()
        for i, row in enumerate(snapshot.itertuples(index=False)):
            y = 335 + i * 58
            name = str(row.geography)
            value = float(row.value)
            d.text((left, y + 5), name, font=font(19, True), fill=INK)
            bar_left, bar_top, bar_max_width = 465, y, 630
            width = max(3, int(bar_max_width * value / max_value))
            d.rounded_rectangle((bar_left, bar_top, bar_left + bar_max_width, bar_top + 34), radius=10, fill="#E8EDF2")
            d.rounded_rectangle((bar_left, bar_top, bar_left + width, bar_top + 34), radius=10, fill=BLUE if i else TEAL)
            d.text((1120, y + 4), f"{value / 1_000_000:.2f}M", font=font(18, True), fill=NAVY)
        d.line((94, 815, 1305, 815), fill=LINE, width=2)
        d.text((94, 829), "Sequential filter-state preview; use dashboard/index.html for live metric, period, area and provider controls.",
               font=font(15), fill=MUTED)
        frames.append(image)
    frames[0].save(OUT / "dashboard_walkthrough.gif", save_all=True,
                   append_images=frames[1:], duration=[5000, 5000], loop=0, optimize=True)

if __name__ == "__main__":
    build_erd()
    build_gif()
    print("Created ERD PNG and 10-second source-backed dashboard preview GIF.")
