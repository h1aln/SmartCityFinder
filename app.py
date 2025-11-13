
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Smart City Finder", layout="wide")

DATA_DIR = Path(__file__).parent / "data"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_DIR / "merged_smartcity.csv")
    return df

df = load_data()

st.title("🏙️ Smart City Finder")
st.markdown(
    "Use this visual agent to explore **U.S. cities** based on "
    "**demographics**, **crime & safety**, and **income**."
)

# Sidebar controls
st.sidebar.header("Your Priorities")
profile = st.sidebar.selectbox(
    "Who are you?", ["Individual (housing)", "Business (investment)"]
)

if profile == "Individual (housing)":
    default_weights = (0.45, 0.25, 0.30)
else:
    default_weights = (0.30, 0.45, 0.25)

w_safety = st.sidebar.slider("Safety weight", 0.0, 1.0, float(default_weights[0]))
w_income = st.sidebar.slider("Income weight", 0.0, 1.0, float(default_weights[1]))
w_aff   = st.sidebar.slider("Affordability weight", 0.0, 1.0, float(default_weights[2]))

# normalize weights so they sum to 1
total_w = w_safety + w_income + w_aff
if total_w == 0:
    w_safety = w_income = w_aff = 1/3
else:
    w_safety /= total_w
    w_income /= total_w
    w_aff   /= total_w

df["UserScore"] = (
    w_safety * df["SafetyIndex_norm"] +
    w_income * df["median_household_income_2020_norm"] +
    w_aff   * df["AffordabilityIndex_norm"]
)

# Layout columns
map_col, scatter_col = st.columns([1.2, 1])

with map_col:
    st.subheader("Map Overview: Safety & Income by City")
    fig_map = px.scatter_geo(
        df,
        lat="lat",
        lon="lng",
        scope="usa",
        hover_name="city",
        hover_data={
            "state": True,
            "median_household_income_2020": True,
            "violent_crime_rate_2020": True,
            "population": True,
            "UserScore": ':.2f',
        },
        color="violent_crime_rate_2020",
        size="population",
        color_continuous_scale="Reds",
        size_max=30,
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

with scatter_col:
    st.subheader("Income vs Violent Crime Rate")
    fig_scatter = px.scatter(
        df,
        x="median_household_income_2020",
        y="violent_crime_rate_2020",
        size="population",
        color="state",
        hover_name="city",
        labels={
            "median_household_income_2020": "Median Household Income (USD)",
            "violent_crime_rate_2020": "Violent Crime Rate (per 100k)",
        },
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("Multi-factor Comparison (Safety, Income, Affordability)")
fig_parallel = px.parallel_coordinates(
    df,
    dimensions=[
        "SafetyIndex_norm",
        "median_household_income_2020_norm",
        "AffordabilityIndex_norm",
    ],
    color="UserScore",
    color_continuous_scale="Viridis",
    labels={
        "SafetyIndex_norm": "Safety",
        "median_household_income_2020_norm": "Income",
        "AffordabilityIndex_norm": "Affordability",
    },
)
st.plotly_chart(fig_parallel, use_container_width=True)

st.subheader("Top 10 Recommended Cities")
top_n = st.slider("Number of cities to show", 5, 20, 10)
top_df = df.sort_values("UserScore", ascending=False).head(top_n)
st.dataframe(
    top_df[[
        "city",
        "state",
        "population",
        "median_household_income_2020",
        "violent_crime_rate_2020",
        "UserScore",
    ]].reset_index(drop=True)
)
