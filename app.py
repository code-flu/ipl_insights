import pandas as pd
import streamlit as st

import style
from src.match_tab import display_match_tab

# Apply custom style
style.apply_custom_styles()

match_tab, player_tab = st.tabs(["Matches", "Players"])


# Load data
@st.cache_data
def load_data():
    t = pd.read_csv('data/teams.csv')
    p = pd.read_csv('data/players.csv')
    m = pd.read_csv('data/matches.csv')
    d = pd.read_csv('data/deliveries.csv')
    return t, p, m, d


teams, players, matches, deliveries = load_data()

# Sidebar
with st.sidebar:
    col1, mid, col2 = st.columns([1, 3, 20])
    with col1:
        st.image('images/logo.png', width=55)
    with col2:
        st.title(':rainbow[Insights]')

    team_list = teams['team'].unique()
    selected_team = st.selectbox(':blue[Select a team]', team_list)
    year_list = teams.loc[teams['team'] == selected_team, 'year'].unique()[::-1]
    selected_years = st.multiselect(
        ':blue[Select Seasons]',
        year_list,
        year_list[:6])

display_match_tab(match_tab, matches, selected_team, selected_years)

with player_tab:
    st.title("Development in progress...")
