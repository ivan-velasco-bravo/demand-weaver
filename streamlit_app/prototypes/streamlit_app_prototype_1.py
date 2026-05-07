import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="DemandWeaver Prototype",
    layout="wide"
)

# -----------------------------
# Sample hardcoded data
# -----------------------------

months = ["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May"]

sales_data = pd.DataFrame({
    "month": months,
    "current_year_sales": [2.6, 2.8, 3.6, 4.6, 4.3, 3.8, 3.5, 3.6, 4.2, 3.9],
    "last_year_sales": [1.8, 2.0, 2.4, 2.5, 2.8, 2.2, 2.5, 2.8, 3.0, 2.9],
    "current_year_units": [21000, 20500, 25000, 26000, 32000, 32000, 29000, 39000, 38000, 37000],
    "last_year_units": [8000, 9000, 12000, 12500, 21000, 20000, 13500, 22000, 21000, 20500],
    "google_trends": [78, 55, 70, 50, 72, 80, 46, 58, 82, 60],
    "sales_normalised": [26, 42, 51, 78, 55, 72, 45, 58, 70, 55],
    "news_volume": [150, 220, 180, 420, 310, 260, 205, 250, 230, 210],
})

related_queries_rising = pd.DataFrame({
    "Query": [
        "iphone 16 price in india",
        "iphone 16 launch date",
        "iphone 16 features",
        "iphone 16 pro max",
        "iphone 16 colours"
    ],
    "Growth": ["+4,350%", "+2,150%", "+1,680%", "+1,420%", "+980%"]
})

related_queries_top = pd.DataFrame({
    "Query": [
        "iphone 16",
        "iphone 16 pro max",
        "iphone 16 price",
        "iphone 16 launch date",
        "iphone 16 review"
    ],
    "Score": [100, 86, 74, 62, 48]
})

related_topics_rising = pd.DataFrame({
    "Topic": ["iPhone 16", "Apple Event", "iOS 18", "A18 Chip", "Apple India"],
    "Type": ["Product", "Event", "Software", "Technology", "Business"],
    "Growth": ["+1,950%", "+1,250%", "+980%", "+760%", "+620%"]
})

related_topics_top = pd.DataFrame({
    "Topic": ["iPhone", "Apple", "Smartphones", "Mobile Phones", "Technology"],
    "Type": ["Product", "Company", "Category", "Category", "Category"],
    "Score": [100, 89, 72, 61, 48]
})

news_articles = [
    {
        "title": "Apple unveils iPhone 16 lineup with AI features and A18 chip",
        "source": "TechCrunch",
        "date": "06 May 2025",
        "description": "Apple announced its latest iPhone series featuring advanced AI capabilities."
    },
    {
        "title": "iPhone 16 pre-orders break records in India",
        "source": "Economic Times",
        "date": "05 May 2025",
        "description": "Apple's latest model sees strong pre-order demand across key Indian markets."
    },
    {
        "title": "What's new in iPhone 16: Top 10 features",
        "source": "The Verge",
        "date": "04 May 2025",
        "description": "A closer look at the most discussed iPhone 16 features."
    }
]

# -----------------------------
# Header controls
# -----------------------------

st.title("DemandWeaver")
st.caption("Product Demand & Market Signals Explorer")

top_col_1, top_col_2, top_col_3 = st.columns([2, 2, 1])

with top_col_1:
    selected_product = st.selectbox(
        "Select Product",
        ["iPhone 16", "Samsung Galaxy S24", "OnePlus 12", "Redmi Note 13"]
    )

with top_col_2:
    date_range = st.date_input(
        "Date Range",
        value=[]
    )

with top_col_3:
    st.write("")
    st.write("")
    st.button("Refresh Data")

# -----------------------------
# Product context card
# -----------------------------

st.markdown("### Selected Product")

context_cols = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])

with context_cols[0]:
    st.metric("Product", selected_product)

with context_cols[1]:
    st.metric("Category", "Smartphones")

with context_cols[2]:
    st.metric("Sub-category", "Premium")

with context_cols[3]:
    st.metric("Brand", "Apple")

with context_cols[4]:
    st.metric("List Price", "₹79,999")

with context_cols[5]:
    st.metric("First Sale", "Aug 2024")

with context_cols[6]:
    st.metric("Avg. Rating", "4.4 / 5")

with context_cols[7]:
    st.metric("Return Rate", "3.8%")

# -----------------------------
# KPI cards
# -----------------------------

st.markdown("### Demand Overview")

kpi_1, kpi_2, kpi_3, kpi_4, kpi_5, kpi_6 = st.columns(6)

kpi_1.metric("Total Sales", "₹24.68 Cr", "18.6%")
kpi_2.metric("Sales Growth %", "18.6%", "6.3%")
kpi_3.metric("Trend Score", "78 / 100", "High Demand")
kpi_4.metric("News Volume", "356", "42.7%")
kpi_5.metric("Units Sold", "31,420", "15.2%")
kpi_6.metric("Order Count", "12,842", "11.8%")

# -----------------------------
# Charts
# -----------------------------

st.markdown("### Internal Performance & External Demand")

chart_col_1, chart_col_2, chart_col_3 = st.columns(3)

sales_long = sales_data.melt(
    id_vars="month",
    value_vars=["current_year_sales", "last_year_sales"],
    var_name="series",
    value_name="sales"
)

with chart_col_1:
    st.markdown("#### Sales Per Month")
    sales_chart = (
        alt.Chart(sales_long)
        .mark_bar()
        .encode(
            x="month:N",
            y="sales:Q",
            color="series:N",
            tooltip=["month", "series", "sales"]
        )
        .properties(height=280)
    )
    st.altair_chart(sales_chart, use_container_width=True)

units_long = sales_data.melt(
    id_vars="month",
    value_vars=["current_year_units", "last_year_units"],
    var_name="series",
    value_name="units"
)

with chart_col_2:
    st.markdown("#### Sales Trend: Units")
    units_chart = (
        alt.Chart(units_long)
        .mark_line(point=True)
        .encode(
            x="month:N",
            y="units:Q",
            color="series:N",
            tooltip=["month", "series", "units"]
        )
        .properties(height=280)
    )
    st.altair_chart(units_chart, use_container_width=True)

comparison_long = sales_data.melt(
    id_vars="month",
    value_vars=["sales_normalised", "google_trends"],
    var_name="series",
    value_name="score"
)

with chart_col_3:
    st.markdown("#### Sales vs Google Trends")
    comparison_chart = (
        alt.Chart(comparison_long)
        .mark_line(point=True)
        .encode(
            x="month:N",
            y="score:Q",
            color="series:N",
            tooltip=["month", "series", "score"]
        )
        .properties(height=280)
    )
    st.altair_chart(comparison_chart, use_container_width=True)

# -----------------------------
# Related signals
# -----------------------------

st.markdown("### Related Search & Market Signals")

signal_col_1, signal_col_2, signal_col_3 = st.columns(3)

with signal_col_1:
    st.markdown("#### Related Search Queries")
    st.markdown("**Rising Queries**")
    st.dataframe(related_queries_rising, use_container_width=True, hide_index=True)
    st.markdown("**Top Queries**")
    st.dataframe(related_queries_top, use_container_width=True, hide_index=True)

with signal_col_2:
    st.markdown("#### Related Topics")
    st.markdown("**Rising Topics**")
    st.dataframe(related_topics_rising, use_container_width=True, hide_index=True)
    st.markdown("**Top Topics**")
    st.dataframe(related_topics_top, use_container_width=True, hide_index=True)

with signal_col_3:
    st.markdown("#### News Volume")
    news_chart = (
        alt.Chart(sales_data)
        .mark_area(opacity=0.4)
        .encode(
            x="month:N",
            y="news_volume:Q",
            tooltip=["month", "news_volume"]
        )
        .properties(height=240)
    )
    st.altair_chart(news_chart, use_container_width=True)

# -----------------------------
# News feed
# -----------------------------

st.markdown("### Latest News Articles")

for article in news_articles:
    with st.container(border=True):
        st.markdown(f"**{article['title']}**")
        st.caption(f"{article['source']} · {article['date']}")
        st.write(article["description"])

# -----------------------------
# Signal summary
# -----------------------------

st.markdown("### Demand Signal Summary")

summary_col_1, summary_col_2, summary_col_3, summary_col_4 = st.columns(4)

with summary_col_1:
    st.info("Internal sales are up 18.6% compared to the same period last year.")

with summary_col_2:
    st.info("Search interest is high and broadly aligned with sales movement.")

with summary_col_3:
    st.info("News activity is elevated, with 356 articles in the selected period.")

with summary_col_4:
    st.success("Overall signal: Strong demand momentum detected.")