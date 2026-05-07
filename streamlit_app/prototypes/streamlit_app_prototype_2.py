import streamlit as st
import pandas as pd
import altair as alt
from textwrap import dedent

# =============================================================================
# Page config
# =============================================================================
st.set_page_config(
    page_title="DemandWeaver",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# Helpers
# =============================================================================
def html(markup: str):
    """Render HTML reliably: dedent + strip so Markdown doesn't treat it as code."""
    st.markdown(dedent(markup).strip(), unsafe_allow_html=True)


def style_chart(chart):
    """Force a light, transparent canvas regardless of Streamlit theme."""
    return (
        chart.configure(background="white")
             .configure_view(strokeWidth=0, fill="white")
             .configure_axis(labelColor="#667085", titleColor="#667085",
                             gridColor="#EEF0F4", domainColor="#E6E8EE",
                             tickColor="#E6E8EE")
             .configure_legend(labelColor="#101828", titleColor="#101828")
    )


def sparkline(values, color):
    df = pd.DataFrame({"i": list(range(len(values))), "v": values})
    chart = (
        alt.Chart(df)
        .mark_area(
            line={"color": color, "strokeWidth": 2},
            color=alt.Gradient(
                gradient="linear",
                stops=[alt.GradientStop(color=color, offset=0),
                       alt.GradientStop(color="#ffffff", offset=1)],
                x1=1, x2=1, y1=1, y2=0,
            ),
        )
        .encode(x=alt.X("i:Q", axis=None), y=alt.Y("v:Q", axis=None))
        .properties(height=44)
    )
    return style_chart(chart)


def icon_box(glyph, color):
    return (
        f'<div class="dw-icon-box" style="background:{color}1A;color:{color};">'
        f'<span style="font-size:18px;font-weight:800;">{glyph}</span></div>'
    )


def kpi_card(col, label, value, delta, delta_label, spark_values, color, glyph):
    with col:
        with st.container(border=True):
            html(f"""
<div style="display:flex;align-items:center;gap:12px;">
{icon_box(glyph, color)}
<div class="dw-kpi-label">{label}</div>
</div>
<div class="dw-kpi-value">{value}</div>
<div style="margin-top:4px;">
<span class="dw-delta-up">▲ {delta}</span>
<span class="dw-delta-muted">&nbsp;{delta_label}</span>
</div>
            """)
            st.altair_chart(sparkline(spark_values, color), use_container_width=True)

# =============================================================================
# Global styles
# =============================================================================
html("""
<style>
.stApp { background-color: #F5F7FB; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1500px; }

div[data-testid="stVerticalBlockBorderWrapper"] {
  background:#ffffff; border:1px solid #E6E8EE !important;
  border-radius:14px !important; padding:16px 18px !important;
  box-shadow:0 1px 2px rgba(16,24,40,0.04);
}

h1, h2, h3, h4 { margin-bottom: 0.4rem; color:#101828; }
header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }

.dw-title { font-size:22px; font-weight:700; color:#101828; line-height:1.1; }
.dw-subtitle { font-size:12px; color:#667085; margin-top:2px; }
.dw-label { font-size:12px; color:#667085; }
.dw-value { font-size:16px; font-weight:600; color:#101828; }
.dw-kpi-label { font-size:13px; color:#667085; }
.dw-kpi-value { font-size:26px; font-weight:700; color:#101828; line-height:1.1; margin-top:6px; }
.dw-delta-up { color:#16A34A; font-size:12px; font-weight:500; }
.dw-delta-muted { color:#98A2B3; font-size:12px; }

.dw-pill-active { display:inline-block; padding:3px 10px; border-radius:999px;
  background:#ECFDF3; color:#067647; font-size:12px; font-weight:600; border:1px solid #ABEFC6; }
.dw-pill-strong { display:inline-block; padding:5px 12px; border-radius:999px;
  background:#ECFDF3; color:#067647; font-size:13px; font-weight:700; border:1px solid #ABEFC6; }

.dw-icon-box { width:40px; height:40px; border-radius:10px;
  display:inline-flex; align-items:center; justify-content:center; }

.dw-section-title { font-size:14px; font-weight:600; color:#101828; }
.dw-rising-label { font-size:13px; font-weight:700; color:#1570EF; margin-bottom:4px; }
.dw-news-title { font-size:13px; font-weight:600; color:#101828; line-height:1.3; }
.dw-news-meta  { font-size:11px; color:#667085; margin-top:2px; }
.dw-summary-title { font-size:13px; font-weight:600; color:#101828; }
.dw-summary-body  { font-size:12px; color:#475467; line-height:1.4; }

.stButton > button { background:#1570EF !important; color:#ffffff !important;
  border:none !important; border-radius:10px !important; font-weight:600 !important; }
[data-testid="stMetric"] { background: transparent; }
</style>
""")

# =============================================================================
# Sample data
# =============================================================================
months = ["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May"]

sales_data = pd.DataFrame({
    "month": months,
    "current_year_sales": [2.6, 2.8, 3.6, 4.6, 4.3, 3.8, 3.5, 3.6, 4.2, 3.9],
    "last_year_sales":    [1.8, 2.0, 2.4, 2.5, 2.8, 2.2, 2.5, 2.8, 3.0, 2.9],
    "current_year_units": [21000, 20500, 25000, 26000, 32000, 32000, 29000, 39000, 38000, 37000],
    "last_year_units":    [8000, 9000, 12000, 12500, 21000, 20000, 13500, 22000, 21000, 20500],
    "google_trends":      [78, 55, 70, 50, 72, 80, 46, 58, 82, 60],
    "sales_normalised":   [26, 42, 51, 78, 55, 72, 45, 58, 70, 55],
    "news_volume":        [150, 220, 180, 420, 310, 260, 205, 250, 230, 210],
})

related_queries_rising = pd.DataFrame({
    "Query":  ["iphone 16 price in india", "iphone 16 launch date", "iphone 16 features",
               "iphone 16 pro max", "iphone 16 colors"],
    "Growth": ["+4,350%", "+2,150%", "+1,680%", "+1,420%", "+980%"],
})
related_queries_top = pd.DataFrame({
    "Query": ["iphone 16", "iphone 16 pro max", "iphone 16 price", "iphone 16 launch date", "iphone 16 review"],
    "Score": [100, 86, 74, 62, 48],
})
related_topics_rising = pd.DataFrame({
    "Topic":  ["iPhone 16", "Apple Event", "iOS 18", "A18 Chip", "Apple India"],
    "Type":   ["Product", "Event", "Software", "Technology", "Business"],
    "Growth": ["+1,950%", "+1,250%", "+980%", "+760%", "+620%"],
})
related_topics_top = pd.DataFrame({
    "Topic": ["iPhone", "Apple", "Smartphones", "Mobile Phones", "Technology"],
    "Type":  ["Product", "Company", "Category", "Category", "Category"],
    "Score": [100, 89, 72, 61, 48],
})
news_articles = [
    {"title": "Apple unveils iPhone 16 lineup with AI features and A18 chip",
     "source": "TechCrunch", "date": "06 May 2025"},
    {"title": "iPhone 16 pre-orders break records in India",
     "source": "Economic Times", "date": "05 May 2025"},
    {"title": "What's new in iPhone 16: Top 10 features",
     "source": "The Verge", "date": "04 May 2025"},
]

# =============================================================================
# Header (logo + title + filters + refresh)
# =============================================================================
h1, h2, h3, h4 = st.columns([2.2, 3.5, 3, 1])
with h1:
    html("""
<div style="display:flex;align-items:center;gap:10px;">
<div style="width:36px;height:36px;border-radius:8px;background:#EFF4FF;
display:flex;align-items:center;justify-content:center;">
<span style="color:#1570EF;font-weight:800;font-size:18px;">◆</span>
</div>
<div>
<div class="dw-title">DemandWeaver</div>
<div class="dw-subtitle">Product Demand &amp; Market Signals</div>
</div>
</div>
    """)
with h2:
    selected_product = st.selectbox(
        "Select Product",
        ["iPhone 16", "Samsung Galaxy S24", "OnePlus 12", "Redmi Note 13"],
    )
with h3:
    st.date_input(
        "Date Range",
        value=(pd.to_datetime("2024-08-01"), pd.to_datetime("2025-05-07")),
    )
with h4:
    st.write("")
    st.write("")
    st.button("Refresh Data", use_container_width=True)

# =============================================================================
# Product context strip
# =============================================================================
with st.container(border=True):
    pc = st.columns([0.9, 2.2, 1.2, 1.4, 1, 1.1, 1.2, 1.4, 1.4, 1.2, 1.2])
    with pc[0]:
        html("""
<div style='width:64px;height:64px;border-radius:10px;background:#EEF2F6;
display:flex;align-items:center;justify-content:center;font-size:24px;color:#475467;'>
<span style="font-size:26px;">▮</span>
</div>
        """)
    with pc[1]:
        html(f"""
<div style="display:flex;align-items:center;gap:10px;">
<div style="font-size:20px;font-weight:700;color:#101828;">{selected_product}</div>
<span class="dw-pill-active">Active</span>
</div>
<div class="dw-subtitle" style="margin-top:6px;">Apple · Premium Smartphones</div>
        """)

    def stat(col, label, value):
        with col:
            html(f"<div class='dw-label'>{label}</div><div class='dw-value'>{value}</div>")

    stat(pc[2],  "Category",             "Smartphones")
    stat(pc[3],  "Sub-category",         "Premium Smartphones")
    stat(pc[4],  "Brand",                "Apple")
    stat(pc[5],  "List Price",           "₹79,999")
    stat(pc[6],  "First Sale Date",      "Aug 2024")
    stat(pc[7],  "Total Lifetime Sales", "₹24.68 Cr")
    stat(pc[8],  "Total Units Sold",     "31,420")
    stat(pc[9],  "Avg. Rating",          "★ 4.4 / 5")
    stat(pc[10], "Return Rate",          "3.8%")

# =============================================================================
# KPI cards
# =============================================================================
k1, k2, k3, k4, k5, k6 = st.columns(6)
kpi_card(k1, "Total Sales",    "₹24.68 Cr", "18.6%", "vs last year",
         sales_data["current_year_sales"].tolist(),  "#1570EF", "↗")
kpi_card(k2, "Sales Growth %", "18.6%",     "6.3%",  "vs last year",
         sales_data["current_year_sales"].pct_change().fillna(0).tolist(), "#16A34A", "▦")
kpi_card(k3, "Trend Score",    "78 / 100",  "High Demand", "",
         sales_data["google_trends"].tolist(), "#7C3AED", "↗")
kpi_card(k4, "News Volume",    "356",       "42.7%", "vs last 30 days",
         sales_data["news_volume"].tolist(),  "#F97316", "▤")
kpi_card(k5, "Units Sold",     "31,420",    "15.2%", "vs last year",
         sales_data["current_year_units"].tolist(), "#0EA5A5", "◧")
kpi_card(k6, "Order Count",    "12,842",    "11.8%", "vs last year",
         (sales_data["current_year_units"] / 3).round().tolist(), "#3B82F6", "▤")

# =============================================================================
# Three charts row
# =============================================================================
c1, c2, c3 = st.columns(3)

# --- Sales per month (grouped bars)
with c1:
    with st.container(border=True):
        html("<div class='dw-section-title'>Sales Per Month: Current Year vs Last Year (₹)</div>")
        sales_long = sales_data.melt(
            id_vars="month",
            value_vars=["current_year_sales", "last_year_sales"],
            var_name="series", value_name="sales",
        )
        sales_long["series"] = sales_long["series"].map({
            "current_year_sales": "Current Year (Aug 2024 – May 2025)",
            "last_year_sales":    "Last Year (Aug 2023 – May 2024)",
        })
        chart = (
            alt.Chart(sales_long)
            .mark_bar(cornerRadiusTopLeft=2, cornerRadiusTopRight=2)
            .encode(
                x=alt.X("month:N", sort=months, title=None),
                y=alt.Y("sales:Q", title=None),
                xOffset="series:N",
                color=alt.Color(
                    "series:N",
                    scale=alt.Scale(range=["#1570EF", "#B8C4D6"]),
                    legend=alt.Legend(orient="top", title=None, labelFontSize=11),
                ),
                tooltip=["month", "series", "sales"],
            )
            .properties(height=260)
        )
        st.altair_chart(style_chart(chart), use_container_width=True)

# --- Units trend (current solid + last dashed via two layers)
with c2:
    with st.container(border=True):
        html("<div class='dw-section-title'>Sales Trend (Units) Over Time</div>")
        units_long = sales_data.melt(
            id_vars="month",
            value_vars=["current_year_units", "last_year_units"],
            var_name="series", value_name="units",
        )
        units_long["series"] = units_long["series"].map({
            "current_year_units": "Current Year (Units)",
            "last_year_units":    "Last Year (Units)",
        })

        common_x = alt.X("month:N", sort=months, title=None)
        common_y = alt.Y("units:Q", title=None)

        line_current = (
            alt.Chart(units_long[units_long["series"] == "Current Year (Units)"])
            .mark_line(strokeWidth=2.5, point=alt.OverlayMarkDef(filled=True, size=45))
            .encode(x=common_x, y=common_y, color=alt.value("#16A34A"),
                    tooltip=["month", "units"])
        )
        line_last = (
            alt.Chart(units_long[units_long["series"] == "Last Year (Units)"])
            .mark_line(strokeWidth=2, strokeDash=[4, 4])
            .encode(x=common_x, y=common_y, color=alt.value("#9AA4B2"),
                    tooltip=["month", "units"])
        )
        # Manual legend via hidden encoding so the user sees both series labels
        legend_layer = (
            alt.Chart(units_long).mark_point(opacity=0).encode(
                color=alt.Color(
                    "series:N",
                    scale=alt.Scale(
                        domain=["Current Year (Units)", "Last Year (Units)"],
                        range=["#16A34A", "#9AA4B2"],
                    ),
                    legend=alt.Legend(orient="top", title=None, labelFontSize=11),
                )
            )
        )
        units_chart = alt.layer(line_current, line_last, legend_layer).properties(height=260)
        st.altair_chart(style_chart(units_chart), use_container_width=True)

# --- Sales vs Google Trends
with c3:
    with st.container(border=True):
        html("<div class='dw-section-title'>Sales vs Google Trends (Normalized)</div>")
        comp_long = sales_data.melt(
            id_vars="month",
            value_vars=["sales_normalised", "google_trends"],
            var_name="series", value_name="score",
        )
        comp_long["series"] = comp_long["series"].map({
            "sales_normalised": "Sales (Normalized)",
            "google_trends":    "Google Trends (Normalized)",
        })
        comp_chart = (
            alt.Chart(comp_long)
            .mark_line(strokeWidth=2.5, point=alt.OverlayMarkDef(filled=True, size=35))
            .encode(
                x=alt.X("month:N", sort=months, title=None),
                y=alt.Y("score:Q", title=None),
                color=alt.Color(
                    "series:N",
                    scale=alt.Scale(
                        domain=["Sales (Normalized)", "Google Trends (Normalized)"],
                        range=["#1570EF", "#16A34A"],
                    ),
                    legend=alt.Legend(orient="top", title=None, labelFontSize=11),
                ),
                tooltip=["month", "series", "score"],
            )
            .properties(height=260)
        )
        st.altair_chart(style_chart(comp_chart), use_container_width=True)

# =============================================================================
# Related signals row
# =============================================================================
def render_table(df, value_col, value_color="#16A34A"):
    headers = "".join(
        f"<th style='text-align:left;padding:6px 4px;font-size:11px;color:#98A2B3;font-weight:500;'>{c}</th>"
        for c in df.columns
    )
    rows = ""
    for _, row in df.iterrows():
        cells = ""
        for c in df.columns:
            val = row[c]
            if c == value_col and value_color == "#16A34A":
                cells += (f"<td style='padding:7px 4px;font-size:12px;color:{value_color};"
                          f"font-weight:600;text-align:right;'>▲ {val}</td>")
            elif isinstance(val, (int, float)):
                cells += (f"<td style='padding:7px 4px;font-size:12px;color:#101828;"
                          f"text-align:right;font-weight:500;'>{val}</td>")
            else:
                cells += f"<td style='padding:7px 4px;font-size:12px;color:#101828;'>{val}</td>"
        rows += f"<tr style='border-top:1px solid #F2F4F7;'>{cells}</tr>"
    return (f"<table style='width:100%;border-collapse:collapse;'>"
            f"<thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>")

s1, s2, s3 = st.columns(3)

with s1:
    with st.container(border=True):
        html("<div class='dw-section-title'>Related Search Queries</div>")
        sub1, sub2 = st.columns(2)
        with sub1:
            html("<div class='dw-rising-label'>Rising Queries</div>")
            html(render_table(related_queries_rising, "Growth"))
        with sub2:
            html("<div class='dw-rising-label'>Top Queries</div>")
            html(render_table(related_queries_top, "Score", value_color="#101828"))
        html("<div style='margin-top:10px;'><a style='font-size:12px;color:#1570EF;"
             "text-decoration:none;font-weight:600;'>View all rising queries →</a></div>")

with s2:
    with st.container(border=True):
        html("<div class='dw-section-title'>Related Topics</div>")
        sub1, sub2 = st.columns(2)
        with sub1:
            html("<div class='dw-rising-label'>Rising Topics</div>")
            html(render_table(related_topics_rising, "Growth"))
        with sub2:
            html("<div class='dw-rising-label'>Top Topics</div>")
            html(render_table(related_topics_top, "Score", value_color="#101828"))
        html("<div style='margin-top:10px;'><a style='font-size:12px;color:#1570EF;"
             "text-decoration:none;font-weight:600;'>View all rising topics →</a></div>")

with s3:
    with st.container(border=True):
        html("<div class='dw-section-title'>Market Activity &amp; News</div>")
        n_left, n_right = st.columns([1.1, 1.4])
        with n_left:
            html("<div class='dw-rising-label' style='color:#101828;'>News Volume Over Time</div>")
            news_chart = (
                alt.Chart(sales_data)
                .mark_area(
                    line={"color": "#F97316", "strokeWidth": 2},
                    color=alt.Gradient(
                        gradient="linear",
                        stops=[alt.GradientStop(color="#F97316", offset=0),
                               alt.GradientStop(color="#ffffff", offset=1)],
                        x1=1, x2=1, y1=1, y2=0,
                    ),
                )
                .encode(
                    x=alt.X("month:N", sort=months, title=None),
                    y=alt.Y("news_volume:Q", title=None),
                )
                .properties(height=160)
            )
            st.altair_chart(style_chart(news_chart), use_container_width=True)
        with n_right:
            html("<div style='display:flex;justify-content:space-between;align-items:center;'>"
                 "<div class='dw-rising-label' style='color:#101828;'>Latest News</div>"
                 "<a style='font-size:11px;color:#1570EF;font-weight:600;'>View all news →</a></div>")
            for art in news_articles:
                html(f"""
<div style="padding:8px 0;border-top:1px solid #F2F4F7;">
<div class="dw-news-title">{art['title']}</div>
<div class="dw-news-meta">{art['source']} · {art['date']}</div>
</div>
                """)

# =============================================================================
# Demand Signal Summary
# =============================================================================
with st.container(border=True):
    html("<div class='dw-section-title' style='margin-bottom:12px;'>Demand Signal Summary</div>")
    sm = st.columns([1.2, 1.2, 1.2, 1.2, 1.4])

    summary_blocks = [
        ("#16A34A", "↗", "Internal Sales",
         "Sales are up 18.6% compared to the same period last year."),
        ("#7C3AED", "○", "Search Interest",
         "Search interest is high and shows strong correlation with sales."),
        ("#F97316", "▤", "News Activity",
         "News volume is elevated with 356 articles in the last 30 days."),
        ("#0EA5A5", "✦", "Opportunities",
         "Rising queries and topics indicate growing market interest."),
    ]
    for col, (color, glyph, title, body) in zip(sm[:4], summary_blocks):
        with col:
            html(f"""
<div style="display:flex;gap:10px;align-items:flex-start;">
{icon_box(glyph, color)}
<div>
<div class="dw-summary-title">{title}</div>
<div class="dw-summary-body">{body}</div>
</div>
</div>
            """)

    with sm[4]:
        html("""
<div style="background:#F9FAFB;border:1px solid #EAECF0;border-radius:12px;padding:14px 16px;">
<div style="display:flex;justify-content:space-between;align-items:center;">
<div class="dw-summary-title">Overall Signal</div>
<span class="dw-pill-strong">↗ STRONG</span>
</div>
<div class="dw-summary-body" style="margin-top:6px;">
High demand momentum detected.<br>
Consider inventory planning and targeted campaigns.
</div>
</div>
        """)