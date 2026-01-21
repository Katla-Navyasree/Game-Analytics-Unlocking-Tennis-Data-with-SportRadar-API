import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from databases.supabase_client import supabase

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="🎾 Game Analytics – Tennis",
    layout="wide"
)

# =================================================
# CUSTOM CSS (COLOURFUL UI)
# =================================================
st.markdown("""
<style>

/* GLOBAL BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top,
        #0b1d33,
        #081425,
        #050b18
    ) !important;
    color: #e5f5ff;
}

/* MAIN CONTENT */
[data-testid="stMainBlockContainer"] {
    background: rgba(8, 20, 40, 0.75);
    backdrop-filter: blur(18px);
    border-radius: 18px;
    padding: 2rem;
    box-shadow: 0 0 60px rgba(0, 255, 255, 0.05);
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06101f, #0b1d33) !important;
    border-right: 1px solid rgba(0,255,255,0.1);
}
[data-testid="stSidebar"] * {
    color: #b8ecff !important;
}

/* HEADINGS */
h1, h2, h3 {
    color: #7dd3fc !important;
    text-shadow: 0 0 12px rgba(56,189,248,0.4);
}

/* KPI CARDS */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0b1d33, #06101f) !important;
    border: 1px solid rgba(0,255,255,0.15);
    border-radius: 16px;
    padding: 18px;
    box-shadow:
        0 0 25px rgba(56,189,248,0.15),
        inset 0 0 20px rgba(124,58,237,0.08);
}
[data-testid="metric-container"]:hover {
    transform: scale(1.05);
    box-shadow: 0 0 40px rgba(124,58,237,0.6);
}

/* TABS */
button[data-baseweb="tab"] {
    font-weight: 600;
    color: #94dfff !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(90deg, #0ea5e9, #7c3aed) !important;
    color: white !important;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(124,58,237,0.6);
}

/* DATAFRAMES */
[data-testid="stDataFrame"] {
    background: rgba(6, 16, 31, 0.85);
    border-radius: 14px;
    border: 1px solid rgba(0,255,255,0.1);
}

/* INPUTS */
input, textarea {
    background-color: #06101f !important;
    color: #e5f5ff !important;
    border-radius: 10px !important;
    border: 1px solid rgba(0,255,255,0.15) !important;
}

</style>
""", unsafe_allow_html=True)




# =================================================
# DATA LOADER
# =================================================
@st.cache_data(ttl=600)
def load_table(table):
    response = supabase.table(table).select("*").execute()
    return pd.DataFrame(response.data)

# =================================================
# LOAD DATA
# =================================================
categories = load_table("categories")
competitions = load_table("competitions")
competitors = load_table("competitors")
rankings = load_table("competitor_rankings")
complexes = load_table("complexes")
venues = load_table("venues")

# =================================================
# PRE-JOINS
# =================================================
competition_category = competitions.merge(
    categories, on="category_id", how="left"
)

ranking_df = competitors.merge(
    rankings, on="competitor_id", how="left"
)

venue_complex = venues.merge(
    complexes, on="complex_id", how="left"
)

ranking_df = ranking_df.dropna(subset=["rank"])

# =================================================
# SIDEBAR FILTERS
# =================================================
st.sidebar.header("🎛 Interactive Filters")

category_filter = st.sidebar.multiselect(
    "Competition Category",
    sorted(competition_category["category_name"].dropna().unique())
)

gender_filter = st.sidebar.multiselect(
    "Gender",
    sorted(competitions["gender"].dropna().unique())
)

rank_range = st.sidebar.slider(
    "Rank Range",
    int(ranking_df["rank"].min()),
    int(ranking_df["rank"].max()),
    (1, 50)
)

country_filter = st.sidebar.multiselect(
    "Country",
    sorted(ranking_df["country"].dropna().unique())
)


# =================================================
# APPLY FILTERS
# =================================================
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


# =================================================
# TABS
# =================================================
tab1, tab2, tab3, tab4, tab5,tab6 = st.tabs([
    "Project Overview",
    "🏟 Competitions",
    "👥 Competitors",
    "📍 Venues",
    "📊 Dashboard",
    "📘 SQL Explorer",
    
])

# =================================================
# TAB: 📘PROJECT OVERVIEW
# =================================================
with tab1:
    st.header("📘 Game Analytics: Unlocking Tennis Data")

    st.subheader("🎯 Project Objective")
    st.markdown("""
The **Game Analytics: Unlocking Tennis Data** project is designed to build an
end-to-end sports analytics solution using tennis data obtained from the
**SportRadar API**.

The application collects, processes, stores, and visualizes tennis competition,
venue, and competitor ranking data to provide meaningful insights for sports
enthusiasts, analysts, and organizations.
    """)

    st.divider()

    st.subheader("🧩 Key Components of the Project")
    st.markdown("""
**1. Data Extraction**
- Fetches tennis data from SportRadar API endpoints  
- Parses nested JSON into structured format  

**2. Data Storage**
- Uses a relational SQL database  
- Well-designed schema with primary & foreign keys  

**3. Data Analysis**
- Executes analytical SQL queries to understand:
  - Competition hierarchies  
  - Player rankings and points  
  - Venue and complex distribution  

**4. Data Visualization**
- Interactive Streamlit dashboard  
- Filters, search, KPIs, and charts  
    """)

    st.divider()

    st.subheader("💼 Business Use Cases")
    st.markdown("""
- **Event Exploration:** Navigate tournament structures  
- **Trend Analysis:** Analyze competitions by category and type  
- **Performance Insights:** Study competitor rankings and movements  
- **Decision Support:** Assist event organizers with data-driven insights  
    """)

    st.divider()

    st.subheader("🛠 Technologies Used")
    st.markdown("""
- **Python** – API integration and data processing  
- **SQL (MySQL / PostgreSQL)** – Data storage and querying  
- **Streamlit** – Interactive dashboard development  
- **SportRadar API** – Professional tennis data source  
    """)

    st.divider()

    st.subheader("📊 Expected Outcome")
    st.markdown("""
A fully functional web application that enables users to:
- Explore tennis competitions and venues  
- Analyze player rankings and performance  
- Gain actionable insights through interactive dashboards  

This project demonstrates strong skills in **API integration, database design,
SQL analytics, and Streamlit application development**.
    """)
# =================================================
# TAB 2: COMPETITIONS
# =================================================
with tab2:
    st.header("🏟 Competitions Explorer")

    st.dataframe(
        filtered_competitions[
            ["competition_name", "category_name", "type", "gender"]
        ],
        use_container_width=True
    )

    st.subheader("📊 Competitions per Category")
    dist = (
        filtered_competitions
        .groupby("category_name")
        .size()
        .reset_index(name="count")
    )

    fig = px.bar(
        dist,
        x="category_name",
        y="count",
        color="category_name",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# TAB 3: COMPETITORS & RANKINGS
# =================================================
with tab3:
    st.header("👥 Competitors & Rankings")

    # -------------------------------------------------
    # SEARCH BOX
    # -------------------------------------------------
    search_name = st.text_input(
        "🔍 Search Competitor (by name)",
        placeholder="Type player name..."
    )

    # -------------------------------------------------
    # APPLY SEARCH FILTER
    # -------------------------------------------------
    search_df = filtered_rankings.copy()

    if search_name:
        search_df = search_df[
            search_df["name"].str.contains(search_name, case=False, na=False)
        ]

    # -------------------------------------------------
    # BASIC METRICS (USE SEARCH_DF)
    # -------------------------------------------------
    st.subheader("📊 Competitor Summary")

    total_competitors = search_df["competitor_id"].nunique()
    total_countries = search_df["country"].nunique()
    avg_rank = int(search_df["rank"].mean()) if not search_df.empty else 0
    avg_points = int(search_df["points"].mean()) if not search_df.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Total Competitors", total_competitors)
    c2.metric("🌍 Countries Represented", total_countries)
    c3.metric("📉 Avg Rank", avg_rank)
    c4.metric("⭐ Avg Points", avg_points)

    st.divider()

    # -------------------------------------------------
    # RAW DATA PREVIEW (USE SEARCH_DF)
    # -------------------------------------------------
    st.subheader("📋 Competitor Data Preview")
    
    ordered_df=(
        search_df.sort_values(
            by=["rank", "points", "name"],
            ascending=[True, False, True]
        )
        .reset_index(drop=True) 
    )
    
    st.dataframe(
    ordered_df[["name", "country", "rank", "points", "movement"]],
    use_container_width=True
)
    # -------------------------------------------------
    # RANK VS POINTS (TOP PLAYERS) – USE SEARCH_DF
    # -------------------------------------------------
    st.subheader("🌟 Rank vs Points (Top Players)")

    top_players = (
        search_df
        .sort_values("points", ascending=False)
        .head(50)
    )

    fig = px.scatter(
        top_players,
        x="rank",
        y="points",
        size="points",
        color="country",
        hover_name="name",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # RANK VS POINTS RELATIONSHIP – USE SEARCH_DF
    # -------------------------------------------------
    st.subheader("📈 Rank vs Points Relationship")

    fig = px.scatter(
        search_df,
        x="rank",
        y="points",
        color="country",
        hover_name="name"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # TOP 10 COMPETITORS – USE SEARCH_DF
    # -------------------------------------------------
    st.subheader("🏆 Top 10 Ranked Competitors")

    top10 = search_df.sort_values("rank").head(10)

    fig = px.bar(
        top10,
        x="name",
        y="points",
        color="rank"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # RANK MOVEMENT ANALYSIS – USE SEARCH_DF
    # -------------------------------------------------
    st.subheader("🔄 Rank Movement Analysis")

    movement_df = (
        search_df["movement"]
        .apply(lambda x: "Improved" if x > 0 else "Declined" if x < 0 else "Stable")
        .value_counts()
        .reset_index()
    )
    movement_df.columns = ["movement_type", "count"]

    fig = px.pie(
        movement_df,
        names="movement_type",
        values="count",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # COMPETITORS BY COUNTRY – USE SEARCH_DF
    # -------------------------------------------------
    st.subheader("🌍 Competitors by Country")

    country_df = (
        search_df
        .groupby("country")
        .size()
        .reset_index(name="total_competitors")
        .sort_values("total_competitors", ascending=False)
        .head(10)
    )

    fig = px.bar(
        country_df,
        x="country",
        y="total_competitors",
        color="total_competitors"
    )
    st.plotly_chart(fig, use_container_width=True)

    

# =================================================
# TAB 4: COMPLEXES & VENUES
# =================================================
with tab4:
    st.header("📍 Venues Explorer")

    # -------------------------------------------------
    # COUNTRY FILTER
    # -------------------------------------------------
    venue_country = st.selectbox(
        "🌍 Select Country",
        sorted(venue_complex["country_name"].dropna().unique())
    )

    country_venues = venue_complex[
        venue_complex["country_name"] == venue_country
    ]

    st.divider()

    # -------------------------------------------------
    # KPI SUMMARY
    # -------------------------------------------------
    total_venues = country_venues["venue_name"].nunique()
    total_complexes = country_venues["complex_name"].nunique()
    total_cities = country_venues["city_name"].nunique()
    total_timezones = country_venues["timezone"].nunique()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🏟 Venues", total_venues)
    k2.metric("🏢 Complexes", total_complexes)
    k3.metric("🏙 Cities", total_cities)
    k4.metric("🕒 Timezones", total_timezones)

    st.divider()

    # -------------------------------------------------
    # DATA TABLE
    # -------------------------------------------------
    st.subheader("📋 Venue Details")

    st.dataframe(
        country_venues[
            ["venue_name", "complex_name", "city_name", "timezone"]
        ],
        use_container_width=True
    )

    st.divider()

    # -------------------------------------------------
    # VENUES PER COMPLEX (EXISTING + STYLED)
    # -------------------------------------------------
    st.subheader("🏟 Venues per Complex")

    vc = (
        country_venues
        .groupby("complex_name")
        .size()
        .reset_index(name="count")
    )

    fig = px.bar(
        vc,
        x="complex_name",
        y="count",
        color="complex_name",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # VENUES BY CITY (NEW)
    # -------------------------------------------------
    st.subheader("🏙 Venues by City")

    city_df = (
        country_venues
        .groupby("city_name")
        .size()
        .reset_index(name="venues")
        .sort_values("venues", ascending=False)
    )

    fig = px.bar(
        city_df,
        x="city_name",
        y="venues",
        color="venues"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # VENUES BY TIMEZONE (NEW)
    # -------------------------------------------------
    st.subheader("🕒 Venues by Timezone")

    tz_df = (
        country_venues
        .groupby("timezone")
        .size()
        .reset_index(name="venues")
    )

    fig = px.pie(
        tz_df,
        names="timezone",
        values="venues",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

# =================================================
# TAB 5: DASHBOARD
# =================================================

with tab5:
    st.header("📊 Performance Dashboard")

    # -----------------------------
    # KPI CALCULATIONS
    # -----------------------------
    total_competitors = filtered_rankings["competitor_id"].nunique()
    total_competitions = filtered_competitions.shape[0]
    total_countries = filtered_rankings["country"].nunique()
    avg_points = int(filtered_rankings["points"].mean())

    # -----------------------------
    # KPI ROW
    # -----------------------------
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Competitors", total_competitors)
    col2.metric("🏟 Competitions", total_competitions)
    col3.metric("🌍 Countries", total_countries)
    col4.metric("⭐ Avg Points", avg_points)

    st.markdown("---")

    # -----------------------------
    # RADIAL KPI RING
    # -----------------------------
    fig_kpi = go.Figure(go.Indicator(
        mode="gauge+number",
        value=total_competitors,
        title={"text": "Active Competitors"},
        gauge={
            "axis": {"range": [0, max(500, total_competitors)]},
            "bar": {"color": "#7CFCB5"}
        }
    ))
    fig_kpi.update_layout(
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#7CFCB5"}
    )
    st.plotly_chart(fig_kpi, use_container_width=True)

    # -----------------------------
    # TWO GAUGES
    # -----------------------------
    colA, colB = st.columns(2)
    completion_rate = min(100, int((total_competitors / 500) * 100))
    country_coverage = min(100, int((total_countries / 100) * 100))

    with colA:
        fig1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=completion_rate,
            title={"text": "Data Coverage"},
            gauge={"axis": {"range": [0, 100]}}
        ))
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=280,
            font={"color": "white"}
        )
        st.plotly_chart(fig1, use_container_width=True)

    with colB:
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=country_coverage,
            title={"text": "Country Reach"},
            gauge={"axis": {"range": [0, 100]}}
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=280,
            font={"color": "white"}
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # LINE CHART
    # -----------------------------
    st.subheader("📈 Rank vs Points Trend")
    trend_df = filtered_rankings.sort_values("rank").head(50)

    fig_line = px.line(
        trend_df,
        x="rank",
        y="points",
        markers=True,
        color_discrete_sequence=["#7CFCB5"]
    )
    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # -----------------------------
    # COUNTRY DISTRIBUTION
    # -----------------------------
    st.subheader("🌍 Country Distribution")
    country_count = (
        filtered_rankings
        .groupby("country")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(10)
    )

    fig_bar = px.bar(
        country_count,
        x="country",
        y="count",
        color="count",
        color_continuous_scale="Viridis"
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # DONUT: TOP 10 POINT SHARE
    # -----------------------------
    st.subheader("🥇 Top 10 Players – Points Share")
    top10 = filtered_rankings.sort_values("points", ascending=False).head(10)

    fig_donut = px.pie(
        top10,
        names="name",
        values="points",
        hole=0.5
    )
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")

   

   

    # -----------------------------
    # BAR: AVG POINTS BY COUNTRY
    # -----------------------------
    st.subheader("🌍 Average Points by Country")
    avg_country = (
        filtered_rankings
        .groupby("country")["points"]
        .mean()
        .reset_index(name="avg_points")
        .sort_values("avg_points", ascending=False)
        .head(10)
    )

    fig_avg = px.bar(
        avg_country,
        x="country",
        y="avg_points",
        color="avg_points",
        color_continuous_scale="Turbo"
    )
    fig_avg.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(fig_avg, use_container_width=True)

    

# =================================================
# TAB 6: SQL EXPLORER (DROPDOWN + VISUALS)
# =================================================
with tab6:
    st.header("📘 SQL Explorer")
    st.caption("Select a query → View SQL → View Visualization")

    QUERY_LIST = [
        "1. Competitions with Category",
        "2. Competitions per Category",
        "3. Doubles Competitions",
        "4. ITF Men Competitions",
        "5. Parent & Sub Competitions",
        "6. Competition Type Distribution",
        "7. Top-level Competitions",
        "8. Rank vs Points",
        "9. Top 5 Ranked Players",
        "10. Stable Rank Players",
        "11. Competitors per Country",
        "12. Highest Points Holders",
        "13. Venues with Complex",
        "14. Venues per Complex",
        "15. Venues in AUSTRALIA",
        "16. Venue Timezones",
        "17. Complexes with >1 Venue",
        "18. Venues by Country",
        "19. Venues for Nacional"
    ]

    choice = st.selectbox("Select SQL Query", QUERY_LIST)

    st.divider()

    # ================= COMPETITIONS =================
    if choice == QUERY_LIST[0]:
        st.subheader("Competitions with Category")
        st.code("""
SELECT c.competition_name, cat.category_name
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id;
""", language="sql")
        st.dataframe(competition_category[["competition_name","category_name"]])

    elif choice == QUERY_LIST[1]:
        st.subheader("Competitions per Category")
        st.code("""
SELECT cat.category_name, COUNT(*) FROM Competitions GROUP BY cat.category_name;
""", language="sql")
        df = competition_category.groupby("category_name").size().reset_index(name="total")
        st.plotly_chart(px.bar(df, x="category_name", y="total"), use_container_width=True)

    elif choice == QUERY_LIST[2]:
        st.subheader("Doubles Competitions")
        st.code("SELECT * FROM Competitions WHERE type='doubles';", language="sql")
        st.dataframe(competitions[competitions["type"]=="doubles"])

    elif choice == QUERY_LIST[3]:
        st.subheader("ITF Men Competitions")
        st.code("SELECT * FROM Competitions WHERE category='ITF Men';", language="sql")
        st.dataframe(
            competition_category[
                competition_category["category_name"]=="ITF Men"
            ][["competition_name"]]
        )

    elif choice == QUERY_LIST[4]:
        st.subheader("Parent & Sub Competitions")
        st.code("SELECT parent, child FROM Competitions;", language="sql")
        pc = competitions.merge(
            competitions,
            left_on="parent_id",
            right_on="competition_id",
            suffixes=("_child","_parent")
        )
        st.dataframe(pc[["competition_name_parent","competition_name_child"]])

    elif choice == QUERY_LIST[5]:
        st.subheader("Competition Type Distribution")
        st.code("SELECT category, type, COUNT(*) FROM Competitions;", language="sql")
        df = competition_category.groupby(["category_name","type"]).size().reset_index(name="total")
        st.plotly_chart(px.bar(df, x="category_name", y="total", color="type", barmode="stack"),
                         use_container_width=True)

    elif choice == QUERY_LIST[6]:
        st.subheader("Top-level Competitions")
        st.code("SELECT * FROM Competitions WHERE parent_id IS NULL;", language="sql")
        st.dataframe(competitions[competitions["parent_id"].isna()][["competition_name"]])

    # ================= COMPETITORS =================
    elif choice == QUERY_LIST[7]:
        st.subheader("Rank vs Points")
        st.code("SELECT rank, points FROM Competitor_Rankings;", language="sql")
        st.plotly_chart(px.scatter(ranking_df, x="rank", y="points",
                                   hover_name="name", color="country"),
                         use_container_width=True)

    elif choice == QUERY_LIST[8]:
        st.subheader("Top 5 Ranked Players")
        st.code("SELECT * FROM Rankings WHERE rank<=5;", language="sql")
        top5 = ranking_df[ranking_df["rank"]<=5]
        st.plotly_chart(px.bar(top5, x="name", y="points", color="rank"),
                         use_container_width=True)

    elif choice == QUERY_LIST[9]:
        st.subheader("Stable Rank Players")
        st.code("SELECT * FROM Rankings WHERE movement=0;", language="sql")
        st.dataframe(ranking_df[ranking_df["movement"]==0][["name","rank","movement"]])

    elif choice == QUERY_LIST[10]:
        st.subheader("Competitors per Country")
        st.code("SELECT country, COUNT(*) FROM Competitors GROUP BY country;", language="sql")
        df = ranking_df.groupby("country").size().reset_index(name="total")
        st.plotly_chart(px.bar(df.sort_values("total",ascending=False).head(10),
                               x="country", y="total"),
                         use_container_width=True)

    elif choice == QUERY_LIST[11]:
        st.subheader("Highest Points Holders")
        st.code("SELECT MAX(points) FROM Rankings;", language="sql")
        maxp = ranking_df["points"].max()
        st.dataframe(ranking_df[ranking_df["points"]==maxp][["name","points"]])

    # ================= VENUES =================
    elif choice == QUERY_LIST[12]:
        st.subheader("Venues with Complex")
        st.code("SELECT venue, complex FROM Venues;", language="sql")
        st.dataframe(venue_complex[["venue_name","complex_name"]])

    elif choice == QUERY_LIST[13]:
        st.subheader("Venues per Complex")
        st.code("SELECT complex, COUNT(*) FROM Venues;", language="sql")
        df = venue_complex.groupby("complex_name").size().reset_index(name="total")
        st.plotly_chart(px.bar(df, x="complex_name", y="total"), use_container_width=True)

    elif choice == QUERY_LIST[14]:
        st.subheader("Venues in AUSTRALIA")
        st.code("SELECT * FROM Venues WHERE country='AUSTRALIA';", language="sql")
        st.dataframe(venues[venues["country_name"]=="AUSTRALIA"])

    elif choice == QUERY_LIST[15]:
        st.subheader("Venue Timezones")
        st.code("SELECT venue_name, timezone FROM Venues;", language="sql")
        st.dataframe(venues[["venue_name","timezone"]])

    elif choice == QUERY_LIST[16]:
        st.subheader("Complexes with Multiple Venues")
        st.code("SELECT complex HAVING COUNT(*)>1;", language="sql")
        df = venue_complex.groupby("complex_name").size().reset_index(name="total")
        st.dataframe(df[df["total"]>1])

    elif choice == QUERY_LIST[17]:
        st.subheader("Venues by Country")
        st.code("SELECT country, COUNT(*) FROM Venues GROUP BY country;", language="sql")
        df = venues.groupby("country_name").size().reset_index(name="total")
        st.plotly_chart(px.pie(df, names="country_name", values="total", hole=0.4),
                         use_container_width=True)

    elif choice == QUERY_LIST[18]:
        st.subheader("Venues for Nacional Complex")
        st.code("SELECT venue FROM Venues WHERE complex='Nacional';", language="sql")
        st.dataframe(
            venue_complex[
                venue_complex["complex_name"]=="Nacional"
            ][["venue_name"]]
        )
