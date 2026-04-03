import streamlit as st
import time
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🏀 Basketball Quarter PRO Predictor", layout="wide")
st.title("🏀 Basketball Quarter PRO Predictor")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.sidebar.header("📊 Input Current Quarter Data")

team1_name = st.sidebar.text_input("Team 1 Name", "Team A")
team2_name = st.sidebar.text_input("Team 2 Name", "Team B")

team1_points = st.sidebar.number_input(f"{team1_name} Current Points", min_value=0, value=0)
team2_points = st.sidebar.number_input(f"{team2_name} Current Points", min_value=0, value=0)

line = st.sidebar.number_input("Quarter Total Line (Over/Under)", min_value=1.0, value=50.0)

quarter_duration = st.sidebar.selectbox("Quarter Duration (minutes)", [10, 12])
time_elapsed = st.sidebar.number_input("Time Elapsed in Quarter (minutes)", min_value=0.0,
                                       max_value=float(quarter_duration), value=0.0, step=0.1)

update_interval = st.sidebar.slider("Update Interval (seconds)", 1, 10, 5)

# -----------------------------
# CALCULATION & SIGNAL
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
# LIVE UPDATER
# -----------------------------
st.subheader("📈 Quarter Prediction & Signal")
placeholder = st.empty()
chart_placeholder = st.empty()

df_chart = pd.DataFrame(columns=["Time (min)", f"{team1_name}", f"{team2_name}", "Total Predicted"])

while True:
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
    
    # Update main display
    with placeholder.container():
        st.write(f"**{team1_name} predicted points:** {team1_pred:.1f}")
        st.write(f"**{team2_name} predicted points:** {team2_pred:.1f}")
        st.write(f"**Total predicted points:** {total_pred:.1f} (Line: {line})")
        st.markdown(f"<h2 style='color:{signal_color}'>{signal_text}</h2>", unsafe_allow_html=True)
    
    # Update chart
    df_chart = pd.concat([df_chart, pd.DataFrame({
        "Time (min)": [time_elapsed],
        f"{team1_name}": [team1_pred],
        f"{team2_name}": [team2_pred],
        "Total Predicted": [total_pred]
    })], ignore_index=True)
    
    fig = px.line(df_chart, x="Time (min)", y=[f"{team1_name}", f"{team2_name}", "Total Predicted"],
                  labels={"value": "Predicted Points", "variable": "Team / Total"})
    fig.update_layout(height=400, width=800, legend=dict(orientation="h"))
    chart_placeholder.plotly_chart(fig)
    
    # Stop updating if quarter ends
    if time_elapsed >= quarter_duration:
        st.success("⏱ Quarter Finished!")
        break
    
    # Wait and simulate time increment
    time.sleep(update_interval)
    time_elapsed = round(time_elapsed + update_interval/60, 2)
