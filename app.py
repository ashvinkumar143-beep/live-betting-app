# app.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide", page_title="Live Betting Tracker")
st.title("🏀 Live Betting Tracker")

# Session
if "history" not in st.session_state:
    st.session_state.history = []

# Inputs
team1 = st.number_input("Team 1 Score", 0)
team2 = st.number_input("Team 2 Score", 0)
time_left = st.number_input("Minutes Left in Quarter", 0.0, 10.0, 5.0)
line = st.number_input("Over/Under Line", value=40)

total = team1 + team2
elapsed = 10 - time_left

st.session_state.history.append(total)

# Projection
if elapsed > 0:
    pace = total / elapsed
    proj = pace * 10
else:
    proj = total

# Decision
edge = proj - line

if edge > 3 and time_left <= 4:
    decision = "🟢 ENTER (OVER)"
elif edge < -3 and time_left <= 4:
    decision = "🟢 ENTER (UNDER)"
else:
    decision = "🔴 SKIP"

# Output
st.write(f"Projected Total: {round(proj)}")
st.write(f"Edge: {round(edge,2)}")
st.write(f"Decision: {decision}")

# Graph
fig, ax = plt.subplots()
ax.plot(st.session_state.history)
ax.set_xlabel("Updates")
ax.set_ylabel("Total Score")
ax.set_title("Live Score Trend")
st.pyplot(fig)
