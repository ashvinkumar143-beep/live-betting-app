import streamlit as st

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
# BUTTON-BASED PREDICTION
# -----------------------------
if st.button("📈 Predict Quarter Result"):
    team1_pred, team2_pred, total_pred = predict_points(team1_points, team2_points, time_elapsed, quarter_duration)

    # Signal
    if total_pred > line:
        signal_text = "✅ OVER"
        signal_color = "green"
    elif total_pred < line:
        signal_text = "❌ UNDER"
        signal_color = "red"
    else:
        signal_text = "⚪ NO CLEAR SIGNAL"
        signal_color = "gray"

    # Display
    st.write(f"**{team1_name} predicted points:** {team1_pred:.1f}")
    st.write(f"**{team2_name} predicted points:** {team2_pred:.1f}")
    st.write(f"**Total predicted points:** {total_pred:.1f} (Line: {line})")
    st.markdown(f"<h2 style='color:{signal_color}'>{signal_text}</h2>", unsafe_allow_html=True)

st.markdown("---")
st.write("💡 **Tip:** Enter new points and time elapsed, then click 'Predict Quarter Result' each time to update signals.")
