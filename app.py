import streamlit as st
import time

st.set_page_config(page_title="🏀 Basketball Quarter Predictor", layout="centered")
st.title("🏀 Basketball Quarter Predictor PRO")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.header("📊 Current Quarter Data")

team1_name = st.text_input("Team 1 Name", "Team A")
team2_name = st.text_input("Team 2 Name", "Team B")

team1_points = st.number_input(f"{team1_name} Current Points", min_value=0, value=0)
team2_points = st.number_input(f"{team2_name} Current Points", min_value=0, value=0)

line = st.number_input("Quarter Total Line (Over/Under)", min_value=1.0, value=50.0)

quarter_duration = st.selectbox("Quarter Duration (minutes)", [10, 12])
time_elapsed = st.number_input("Time Elapsed in Quarter (minutes)", min_value=0.0,
                               max_value=float(quarter_duration), value=0.0, step=0.1)

update_interval = st.slider("Update Interval (seconds)", 1, 10, 5)

# -----------------------------
# PREDICTION FUNCTION
# -----------------------------
def predict_points(team1_pts, team2_pts, elapsed, duration):
    if elapsed == 0:
        return team1_pts, team2_pts, 0
    remaining_time = duration - elapsed
    team1_rate = team1_pts / elapsed
    team2_rate = team2_pts / elapsed
    team1_pred = team1_pts + team1_rate * remaining_time
    team2_pred = team2_pts + team2_rate * remaining_time
    total_pred = team1_pred + team2_pred
    return team1_pred, team2_pred, total_pred

# -----------------------------
# LIVE PREDICTION LOOP
# -----------------------------
st.subheader("📈 Quarter Prediction & Signal")
placeholder = st.empty()

while time_elapsed <= quarter_duration:
    team1_pred, team2_pred, total_pred = predict_points(team1_points, team2_points, time_elapsed, quarter_duration)
    
    # Signal
    if total_pred >
