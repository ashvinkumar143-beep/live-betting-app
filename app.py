# app.py - Live Betting Tracker (Beginner-Friendly & Mobile Ready)

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide", page_title="Live Betting Tracker")
st.title("🏀 Live Betting Tracker")

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# INPUTS (left column)
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    team1 = st.number_input("Team 1 Score", 0)
    team2 = st.number_input("Team 2 Score", 0)
    time_left = st.number_input("Minutes Left in Quarter", 0.0, 10.0, 5.0)
    line = st.number_input("Over/Under Line", value=40)

# Calculate total and pace
total = team1 + team2
elapsed = 10 - time_left  # quarter length = 10 minutes

st.session_state.history.append(total)

if elapsed > 0:
    pace = total / elapsed
    proj = pace * 10  # project total for full quarter
else:
    proj = total

edge = proj - line

# -------------------------------
# DECISION & COLOR
# -------------------------------
if edge > 3 and time_left <= 4:
    decision = "OVER"
    color = "green"
elif edge < -3 and time_left <= 4:
    decision = "UNDER"
    color = "red"
else:
    decision = "SKIP"
    color = "gray"

with col2:
    st.write(f"Projected Total: {round(proj)}")
    st.write(f"Edge: {round(edge,2)}")
    st.markdown(
        f"<h2 style='color:{color};text-align:center;'>Decision: {decision}</h2>",
        unsafe_allow_html=True
    )

# -------------------------------
# BEEP ALERT
# -------------------------------
if decision in ["OVER", "UNDER"]:
    st.markdown(
        """
        <audio autoplay>
          <source src="https://www.soundjay.com/button/beep-07.mp3" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# SCORE TREND GRAPH
# -------------------------------
fig, ax = plt.subplots()
ax.plot(st.session_state.history, marker='o')
ax.set_xlabel("Updates")
ax.set_ylabel("Total Score")
ax.set_title("Live Score Trend")
st.pyplot(fig)
