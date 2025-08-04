import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import psycopg2

# Streamlit page config
st.set_page_config(page_title="Agriculture Dashboard", layout="wide")

# Database connection
@st.cache_resource
def get_connection():
    user = 'postgres'
    password = 'Arjun1110'
    host = 'localhost'
    port = '5432'
    database = 'agriculture_data'
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
    return engine

engine = get_connection()

# Load data
@st.cache_data
def load_data():
    query = "SELECT * FROM agriculture_data"
    return pd.read_sql(query, engine)

df = load_data()

st.title("🌾 Agricultural Data Visualization (India)")

# Sidebar filters
with st.sidebar:
    st.header("Filter Data")
    selected_year = st.selectbox("Select Year", sorted(df['year'].dropna().unique()), index=0)
    selected_state = st.multiselect("Select States", options=df['state_name'].dropna().unique(), default=None)

filtered_df = df.copy()
if selected_year:
    filtered_df = filtered_df[filtered_df['year'] == selected_year]
if selected_state:
    filtered_df = filtered_df[filtered_df['state_name'].isin(selected_state)]

# Radio button to select view
view_option = st.radio("Select View Type:", options=["Histograms", "Heatmap", "SQL Insights"])

# HISTOGRAMS
if view_option == "Histograms":
    st.subheader("📊 Crop Production & Yield Histograms")
    crop_sets = [
        ('Rice', 'rice_area', 'rice_production', 'rice_yield'),
        ('Wheat', 'wheat_area', 'wheat_production', 'wheat_yield'),
        ('Oilseeds', 'oilseeds_area', 'oilseeds_production', 'oilseeds_yield'),
        ('Maize', 'maize_area', 'maize_production', 'maize_yield'),
        ('Soybean', 'soyabean_area', 'soyabean_production', 'soyabean_yield'),
        ('Sugarcane', 'sugarcane_area', 'sugarcane_production', 'sugarcane_yield'),
        ('Sunflower', 'sunflower_area', 'sunflower_production', 'sunflower_yield'),
        ('Kharif Sorghum', 'kharif_sorghum_area', 'kharif_sorghum_production', 'kharif_sorghum_yield'),
        ('Rabi Sorghum', 'rabi_sorghum_area', 'rabi_sorghum_production', 'rabi_sorghum_yield'),
        ('Finger Millet', 'finger_millet_area', 'finger_millet_production', 'finger_millet_yield')
    ]

    for title, area, prod, yield_ in crop_sets:
        st.markdown(f"#### {title} Distributions")
        col1, col2, col3 = st.columns(3)
        with col1:
            fig = px.histogram(filtered_df, x=area, nbins=30, title=f"{title} Area")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.histogram(filtered_df, x=prod, nbins=30, title=f"{title} Production")
            st.plotly_chart(fig, use_container_width=True)
        with col3:
            fig = px.histogram(filtered_df, x=yield_, nbins=30, title=f"{title} Yield")
            st.plotly_chart(fig, use_container_width=True)

# HEATMAP
elif view_option == "Heatmap":
    st.subheader("🌡️ Correlation Heatmap")
    corr_columns = [
        'rice_production', 'wheat_production', 'oilseeds_production',
        'kharif_sorghum_production', 'rabi_sorghum_production',
        'sugarcane_production', 'sunflower_production',
        'pearl_millet_production', 'finger_millet_production',
        'soyabean_production', 'maize_production']

    corr_data = df[corr_columns].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_data, annot=True, cmap='coolwarm', fmt=".2f", square=True)
    st.pyplot(fig)

# SQL INSIGHTS
elif view_option == "SQL Insights":
    st.subheader("📈 SQL-Based Insights")
    query_dict = {
        "1. Year-wise Rice Production (Top 3 States)": """
            with top_states as (
                select state_name from agriculture_data
                group by state_name order by sum(rice_production) desc limit 3)
            select year, state_name, sum(rice_production) as total_rice_production
            from agriculture_data where state_name in (select state_name from top_states)
            group by year, state_name order by year, total_rice_production desc
        """,
        "2. Top 5 Districts by Wheat Yield Increase (5 Years)": """
            with last_five_years as (
                select distinct year from agriculture_data order by year desc limit 5),
            year_range as (
                select max(year) as latest_year, min(year) as earliest_year from last_five_years),
            district_yields as (
                select dist_name, year, avg(wheat_yield) as avg_yield from agriculture_data
                where year in (select * from last_five_years)
                group by dist_name, year),
            yield_comparison as (
                select dist_name,
                max(case when year = (select latest_year from year_range) then avg_yield end) as yield_now,
                max(case when year = (select earliest_year from year_range) then avg_yield end) as yield_before
                from district_yields group by dist_name)
            select dist_name, yield_before, yield_now, yield_now - yield_before as yield_increase
            from yield_comparison where yield_now is not null and yield_before is not null
            order by yield_increase desc limit 5
        """,
        "3. States with Highest Oilseed Production Growth": """
            with recent_years as (select distinct year from agriculture_data order by year desc limit 5),
            oilseed_summary as (
                select state_name, year, sum(oilseeds_production) as total_production
                from agriculture_data where year in (select year from recent_years)
                group by state_name, year),
            pivoted as (
                select state_name,
                max(case when year = (select min(year) from recent_years) then total_production end) as production_start,
                max(case when year = (select max(year) from recent_years) then total_production end) as production_end
                from oilseed_summary group by state_name)
            select state_name, production_start, production_end,
            round((((production_end - production_start) / production_start) * 100)::numeric, 2) as growth_rate_percent
            from pivoted where production_start is not null and production_end is not null and production_start <> 0
            order by growth_rate_percent desc limit 5
        """,
        "4. District-wise Rice Area vs Production Correlation": """
            select dist_name, state_name,
            ((count(*) * sum(rice_production * rice_area) - sum(rice_production) * sum(rice_area)) /
            (sqrt(count(*) * sum(rice_production * rice_production) - power(sum(rice_production), 2)) *
             sqrt(count(*) * sum(rice_area * rice_area) - power(sum(rice_area), 2)))) as rice_corr
            from agriculture_data
            where rice_production is not null and rice_area is not null
            group by dist_name, state_name
            having sqrt(count(*) * sum(rice_production * rice_production) - power(sum(rice_production), 2)) <> 0
               and sqrt(count(*) * sum(rice_area * rice_area) - power(sum(rice_area), 2)) <> 0
        """,
        "5. Yearly Cotton Production in Top 5 States": """
            with total_cotton as (
                select state_name, sum(cotton_production) as total
                from agriculture_data group by state_name order by total desc limit 5),
            cotton_trend as (
                select year, state_name, sum(cotton_production) as yearly_production
                from agriculture_data where state_name in (select state_name from total_cotton)
                group by year, state_name)
            select * from cotton_trend order by year, state_name
        """,
        "6. Top Groundnut Districts in 2017": """
            select dist_name, state_name, groundnut_production
            from agriculture_data where year = 2017
            order by groundnut_production desc limit 5
        """,
        "7. Annual Avg Maize Yield (All States)": """
            select year, round(avg(maize_yield)::numeric, 2) as avg_maize_yield
            from agriculture_data group by year order by year
        """,
        "8. Total Oilseed Area per State": """
            select state_name, round(sum(oilseeds_area)::numeric,2) as total_oilseeds_area
            from agriculture_data group by state_name order by total_oilseeds_area desc
        """,
        "9. Top 5 Rice Yield Districts": """
            select dist_name, state_name, max(rice_yield) as max_rice_yield
            from agriculture_data group by dist_name, state_name
            order by max_rice_yield desc limit 5
        """,
        "10. Wheat vs Rice Production (Top 5 States)": """
            with top_states as (
                select state_name, sum(wheat_production + rice_production) as total_production
                from agriculture_data group by state_name order by total_production desc limit 5)
            select year, state_name,
            round(sum(wheat_production)::numeric, 2) as total_wheat,
            round(sum(rice_production)::numeric, 2) as total_rice
            from agriculture_data where state_name in (select state_name from top_states)
            group by year, state_name order by year, state_name
        """
    }

    selected_query = st.selectbox("Choose SQL Insight", list(query_dict.keys()))
    sql_result = pd.read_sql(query_dict[selected_query], engine)
    st.dataframe(sql_result, use_container_width=True)

    if 'year' in sql_result.columns:
        fig = px.line(sql_result, x='year', y=sql_result.columns[-1], color=sql_result.columns[1])
        st.plotly_chart(fig, use_container_width=True)



