import plotly.graph_objects as go
import streamlit as st


def total_match(matches, years, team) -> int:
    return len(matches[(matches['year'].isin(years)) & (matches['teams'].str.contains(team))])


def total_win(matches, years: object, team: object) -> int:
    return len(matches[
                   (matches['year'].isin(years)) & (matches['teams'].str.contains(team)) & (matches['winner'] == team)])


def total_lost(matches, years, team) -> int:
    return len(matches[
                   (matches['year'].isin(years)) & (matches['teams'].str.contains(team)) & (
                           matches['winner'] != team) & (
                       matches['winner'].notna())])


def display_match_tab(tab, matches, selected_team, selected_years):
    with tab:
        col = st.columns((3, 5), gap='small')
        match_count = total_match(matches, selected_years, selected_team)
        win_count = total_win(matches, selected_years, selected_team)
        lost_count = total_lost(matches, selected_years, selected_team)
        tie_count = match_count - win_count - lost_count

        # Pie Chart
        with col[0]:
            st.markdown(f"##### Overall Performance")
            fig = go.Figure(
                go.Pie(
                    hole=0.5,
                    textinfo='label+value',
                    hoverinfo='label+percent',
                    labels=['Won', 'Lost', 'Tied'],
                    values=[win_count, lost_count, tie_count],
                    marker=dict(colors=['#2ca02c', '#d62728', '#ff7f0e'])
                ))
            fig.update_layout(width=300, height=300, margin=dict(l=0, r=0, t=30, b=10, pad=0),
                              annotations=[
                                  dict(text=f'Matches: {match_count}', x=0.5, y=0.5, font_size=15, showarrow=False)])
            st.plotly_chart(fig)

        # Bar Chart
        with col[1]:
            st.markdown(f"##### Performance over the seasons")
            win_data = [total_win(matches, [year], selected_team) for year in selected_years]
            lost_data = [total_lost(matches, [year], selected_team) for year in selected_years]
            tie_data = [
                total_match(matches, [year], selected_team) - total_win(matches, [year], selected_team) - total_lost(
                    matches, [year], selected_team)
                for year in selected_years]

            fig = go.Figure(data=[
                go.Bar(name='Won', x=selected_years, y=win_data, text=win_data, ),
                go.Bar(name='Lost', x=selected_years, y=lost_data, text=lost_data, ),
                go.Bar(name='Tied', x=selected_years, y=tie_data, text=tie_data, ),
            ])

            fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0, pad=0),
                              barmode='stack',
                              yaxis_title='Number of Matches',
                              xaxis=dict(
                                  title='Seasons',
                                  type='category',
                                  categoryorder='category ascending'
                              ))
            st.plotly_chart(fig)

        st.markdown(f"##### Impact of Toss Results on Match Victories")
        col = st.columns((1, 8), gap='small')
        with col[0]:
            toss_result = st.radio(
                ":blue[Toss Result]",
                ["Won", "Lost"])

            toss_decision = st.radio(
                ":blue[Toss Decision]",
                ["Bat", "Field", "Any"])

            # Filter matches based on selected years and team
            filtered_matches = matches[
                (matches['year'].isin(selected_years)) &
                (matches['teams'].str.contains(selected_team))
                ]

            # Filter matches based on toss result
            if toss_result == "Lost":
                filtered_matches = filtered_matches[filtered_matches['toss_winner'] != selected_team]
            else:
                filtered_matches = filtered_matches[filtered_matches['toss_winner'] == selected_team]

            match_count_on_toss_result = len(filtered_matches)

            # Filter matches based on toss decision
            if toss_decision == "Field":
                filtered_matches = filtered_matches[filtered_matches['toss_decision'] == 'field']
            elif toss_decision == "Bat":
                filtered_matches = filtered_matches[filtered_matches['toss_decision'] == 'bat']

            win_match_count = len(filtered_matches[filtered_matches['winner'] == selected_team])
        with col[1]:
            fig = go.Figure(
                go.Pie(
                    hole=0.8,
                    textinfo='value',
                    hoverinfo='label+value',
                    labels=['Won', 'Lost/Tie'],
                    values=[win_match_count, match_count_on_toss_result - win_match_count],
                    showlegend=False,
                    marker=dict(colors=['#2ca02c', '#fff'], line=dict(color='#000000', width=0.2))
                ))
            winning_percent = (win_match_count / match_count_on_toss_result) * 100
            fig.update_layout(width=220, height=220, margin=dict(l=0, r=0, t=0, b=10, pad=0),
                              annotations=[
                                  dict(text="{:.0f}%".format(winning_percent), x=0.5, y=0.5, font_size=50, showarrow=False)])
            st.plotly_chart(fig)
