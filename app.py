import streamlit as st
import pandas as pd
import plotly.express as px
from databases.supabase_client import supabase

st.set_page_config(page_title="Game Analytics – Tennis", layout="wide")

# -------------------------
# Helper
# -------------------------
@st.cache_data
def load_table(table):
    return pd.DataFrame(
        supabase.table(table).select("*").execute().data
    )

# -------------------------
# Load all tables
# -------------------------
categories = load_table("categories")
competitions = load_table("competitions")
competitors = load_table("competitors")
rankings = load_table("competitor_rankings")
complexes = load_table("complexes")
venues = load_table("venues")

# Pre-joins
competition_category = competitions.merge(
    categories, on="category_id", how="left"
)

ranking_df = competitors.merge(
    rankings, on="competitor_id", how="left"
)

venue_complex = venues.merge(
    complexes, on="complex_id", how="left"
)

# -------------------------
# Tabs
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🏟 Competitions & Categories",
    "👥 Competitors & Rankings",
    "📍 Complexes & Venues",
    "📊 Dashboard"
])

# =========================================================
# TAB 1: COMPETITIONS & CATEGORIES
# =========================================================
with tab1:
    st.header("Competitions & Categories Analysis")

    st.subheader("1. Competitions with Category Name")
    st.dataframe(
        competition_category[["competition_name", "category_name"]]
    )

    st.subheader("2. Competition Count per Category")
    count_df = competition_category.groupby("category_name").size().reset_index(name="count")
    st.bar_chart(count_df.set_index("category_name"))

    st.subheader("3. Doubles Competitions")
    st.dataframe(
        competitions[competitions["type"] == "doubles"]
        [["competition_name", "gender"]]
    )

    st.subheader("4. Competitions by Category")
    selected_cat = st.selectbox(
        "Select Category",
        categories["category_name"].unique()
    )
    st.dataframe(
        competition_category[
            competition_category["category_name"] == selected_cat
        ][["competition_name", "type", "gender"]]
    )

    st.subheader("5. Parent & Sub Competitions")
    parent_child = competitions.merge(
        competitions,
        left_on="competition_id",
        right_on="parent_id",
        suffixes=("_parent", "_child")
    )
    st.dataframe(
        parent_child[["competition_name_parent", "competition_name_child"]]
    )

    st.subheader("6. Competition Type Distribution by Category")
    dist = competition_category.groupby(
        ["category_name", "type"]
    ).size().reset_index(name="count")

    fig = px.bar(
        dist,
        x="category_name",
        y="count",
        color="type",
        barmode="group"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("7. Top-Level Competitions (No Parent)")
    st.dataframe(
        competitions[competitions["parent_id"].isna()]
        [["competition_name", "type", "gender"]]
    )

# =========================================================
# TAB 2: COMPETITORS & RANKINGS
# =========================================================
with tab2:
    st.header("Competitors & Rankings")

    st.subheader("1. All Competitors with Rank & Points")
    st.dataframe(
        ranking_df[["name", "country", "rank", "points"]]
    )

    st.subheader("2. Top 5 Ranked Competitors")
    st.dataframe(
        ranking_df[ranking_df["rank"] <= 5]
        [["name", "country", "rank", "points"]]
    )

    st.subheader("3. Stable Rank Competitors (No Movement)")
    st.dataframe(
        ranking_df[ranking_df["movement"] == 0]
        [["name", "rank", "points"]]
    )

    st.subheader("4. Total Points by Country")
    country = st.selectbox(
        "Choose Country",
        ranking_df["country"].dropna().unique()
    )
    total_points = ranking_df[
        ranking_df["country"] == country
    ]["points"].sum()

    st.metric("Total Points", int(total_points))

    st.subheader("5. Competitor Count per Country")
    country_count = competitors.groupby("country").size().reset_index(name="count")
    st.bar_chart(country_count.set_index("country"))

    st.subheader("6. Highest Points – Current Week")
    st.dataframe(
        ranking_df.sort_values("points", ascending=False).head(10)
        [["name", "country", "points"]]
    )

# =========================================================
# TAB 3: COMPLEXES & VENUES
# =========================================================
with tab3:
    st.header("Complexes & Venues")

    st.subheader("1. Venues with Complex Name")
    st.dataframe(
        venue_complex[["venue_name", "complex_name", "country_name"]]
    )

    st.subheader("2. Venue Count per Complex")
    venue_count = venue_complex.groupby("complex_name").size().reset_index(name="count")
    st.bar_chart(venue_count.set_index("complex_name"))

    st.subheader("3. Venues by Country")
    selected_country = st.selectbox(
        "Select Country",
        venue_complex["country_name"].unique()
    )
    st.dataframe(
        venue_complex[
            venue_complex["country_name"] == selected_country
        ][["venue_name", "city_name", "timezone"]]
    )

    st.subheader("4. Venues & Timezones")
    st.dataframe(
        venue_complex[["venue_name", "timezone"]]
    )

# =========================================================
# TAB 4: DASHBOARD
# =========================================================
with tab4:
    st.header("Project Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Competitions", competitions.shape[0])
    col2.metric("Total Competitors", competitors.shape[0])
    col3.metric("Countries Represented", competitors["country"].nunique())

    st.subheader("Top 10 Countries by Competitors")
    fig = px.bar(
        country_count.sort_values("count", ascending=False).head(10),
        x="country",
        y="count"
    )
    st.plotly_chart(fig, use_container_width=True)
