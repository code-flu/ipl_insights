import altair as alt
import streamlit as st


# Custom CSS styling
def apply_custom_styles():
    # Page configuration
    st.set_page_config(
        page_title="IPL Insights: Indian Premier League Analysis Dashboard",
        page_icon="🏏",
        layout="wide",
        initial_sidebar_state="expanded")
    alt.themes.enable("dark")

    # Main Container Padding
    st.markdown("""
    <style>
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stSidebarUserContent"] {
        padding: 1rem 2rem 0rem;
    }
    svg[aria-label="Clear all"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
