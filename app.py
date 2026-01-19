import streamlit as st
import pandas as pd
import plotly.express as px
from databases.supabase_client import supabase

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(page_title="Game Analytics – Tennis", layout="wide")

# =========================================================
# THEME (Dark Blue Glass UI)
# =========================================================
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #0b1d33, #081425, #050b18) !important;
    color: #e5f5ff;
}
[data-testid="stMainBlockContainer"] {
    background: rgba(8,20,40,0.75);
    backdrop-filter: blur(18px);
    border-radius: 18px;
    padding: 2rem;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06101f, #0b1d33) !important;
}
[data-testid="stSidebar"] * {
    color: #b8ecff !important;
}
h1,h2,h3 {
    color: #7dd3fc !important;
    text-shadow: 0 0 12px rgba(56,189,248,0.4);
}
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0b1d33, #06101f) !important;
    border-radius: 16px;
    border: 1px solid rgba(0,255,255,0.15);
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(90deg, #0ea5e9, #7c3aed) !important;
    color: white !important;
    border-radius: 12px;
}
[data-testid="stDataFrame"] {
    background: rgba(6,16,31,0.85);
    border-radius: 14px;
    border: 1px solid rgba(0,255,255,0.1);
}
input, textarea {
    background-color: #06101f !important;
    color: #e5f5ff !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================
st.markdown("## 🎾 **Game Analytics – Tennis**")
st.caption("Interactive Sports Data Dashboard | SportRadar API")

# =========================================================
# DATA LOADER
# =========================================================
@st.cache_data(ttl=600)
def load_table(table):
    response = supabase.table(table).select("*").execute()
    return pd.DataFrame(response.data)

# =========================================================
# LOAD DATA
# =========================================================
categories = load_table("categories")
competitions = load_table("competitions")
competitors = load_table("competitors")
rankings = load_table("competitor_rankings")
complexes = load_table("complexes")
venues = load_table("venues")

# =========================================================
# PRE-JOINS
# =========================================================
competition_category = competitions.merge(categories, on="category_id", how="left")
ranking_df = competitors.merge(rankings, on="competitor_id", how="left")
venue_complex = venues.merge(complexes, on="complex_id", how="left")

ranking_df = ranking_df.dropna(subset=["rank"])

# =========================================================
# SIDEBAR FILTERS (LIKE VIDEO)
# =========================================================
st.sidebar.header("📱 Interactive Filters")

category_filter = st.sidebar.multiselect(
    "Competition Category",
    sorted(competition_category["category_name"].dropna().unique()),
    default=["ATP", "ITF Men"]
)

gender_filter = st.sidebar.multiselect(
    "Gender",
    sorted(competition_category["gender"].dropna().unique()),
    default=["men", "women", "mixed"]
)

rank_range = st.sidebar.slider(
    "Rank Range",
    int(ranking_df["rank"].min()),
    int(ranking_df["rank"].max()),
    (1, 50)
)

country_filter = st.sidebar.multiselect(
    "Country",
    sorted(ranking_df["country"].dropna().unique()),
    default=["Finland", "Latvia", "Georgia", "Slovakia"]
)

search_player = st.sidebar.text_input("🔍 Search Competitor")

# =========================================================
# APPLY FILTERS
# =========================================================
filtered_competitions = competition_category.copy()
if category_filter:
    filtered_competitions = filtered_competitions[
        filtered_competitions["category_name"].isin(category_filter)
    ]
if gender_filter:
    filtered_competitions = filtered_competitions[
        filtered_competitions["gender"].isin(gender_filter)
    ]

filtered_rankings = ranking_df.copy()
filtered_rankings = filtered_rankings[
    (filtered_rankings["rank"] >= rank_range[0]) &
    (filtered_rankings["rank"] <= rank_range[1])
]
if country_filter:
    filtered_rankings = filtered_rankings[
        filtered_rankings["country"].isin(country_filter)
    ]
if search_player:
    filtered_rankings = filtered_rankings[
        filtered_rankings["name"].str.contains(search_player, case=False, na=False)
    ]

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🏟 Competitions",
    "👥 Competitors",
    "📍 Venues",
    "📊 Dashboard"
])

# =========================================================
# TAB 1: COMPETITIONS EXPLORER
# =========================================================
with tab1:
    st.markdown("## 🏟 Competitions Explorer")

    st.dataframe(
        filtered_competitions[
            ["competition_name", "category_name", "type", "gender"]
        ],
        use_container_width=True
    )

    st.markdown("### 📊 Competitions per Category")

    count_df = filtered_competitions.groupby("category_name").size().reset_index(name="count")

    fig = px.bar(
        count_df,
        x="category_name",
        y="count",
        color="category_name",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TAB 2: COMPETITORS EXPLORER
# =========================================================
with tab2:
    st.markdown("## 👥 Competitors Explorer")

    st.dataframe(
        filtered_rankings[
            ["name", "country", "rank", "points", "movement"]
        ],
        use_container_width=True
    )

    st.markdown("### 🏆 Top Ranked Players")

    top10 = ranking_df.sort_values("rank").head(10)

    st.dataframe(
        top10[["name", "country", "rank", "points"]],
        use_container_width=True
    )

# =========================================================
# TAB 3: VENUES EXPLORER (VIDEO STYLE)
# =========================================================
with tab3:
    st.markdown("## 📍 Venues Explorer")

    selected_venue_country = st.selectbox(
        "Select Country",
        sorted(venue_complex["country_name"].dropna().unique())
    )

    venue_country = venue_complex[
        venue_complex["country_name"] == selected_venue_country
    ]

    st.dataframe(
        venue_country[
            ["venue_name", "complex_name", "city_name", "timezone"]
        ],
        use_container_width=True
    )

# =========================================================
# TAB 4: DASHBOARD
# =========================================================
with tab4:
    st.markdown("## 📊 Project Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Competitions", competitions.shape[0])
    col2.metric("Total Competitors", competitors.shape[0])
    col3.metric("Countries Represented", competitors["country"].nunique())

    st.markdown("### 🌍 Top Countries by Players")

    country_count = competitors.groupby("country").size().reset_index(name="count")

    fig2 = px.bar(
        country_count.sort_values("count", ascending=False).head(10),
        x="country",
        y="count",
        template="plotly_dark"
    )

    st.plotly_chart(fig2, use_container_width=True)
