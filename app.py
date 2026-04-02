import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="🔥 Pro Live Betting Tracker")
st.title("🔥 Pro Live Betting Tracker (Final Version)")

# ---------- SESSION ----------
if "history" not in st.session_state:
    st.session_state.history = {}

# ---------- SPORT ----------
sport = st.selectbox("Select Sport", ["Basketball", "Soccer", "Tennis"])

# ---------- INPUT ----------
col1, col2 = st.columns(2)

with col1:
    game_id = st.text_input("Game ID", "match1")

    team1 = st.number_input("Team 1 Score", 0)
    team2 = st.number_input("Team 2 Score", 0)

    time_left = st.number_input("Time Left", 0.0, 90.0, 5.0)
    line = st.number_input("Over/Under Line", value=40.0)

# ---------- GAME SETTINGS ----------
if sport == "Basketball":
    duration = 10
elif sport == "Soccer":
    duration = 90
else:
    duration = 12

# ---------- CALC ----------
total = team1 + team2
elapsed = duration - time_left

# Smooth projection (reduce fake spikes)
if elapsed > 1:
    pace = total / elapsed
    projected_total = total + (pace * time_left * 0.85)  # smoothing factor
else:
    projected_total = total

edge = projected_total - line

# ---------- OVER/UNDER PROB ----------
prob = 50 + edge * 5
prob = max(0, min(100, prob))

over_prob = round(prob)
under_prob = 100 - over_prob

# ---------- WIN PROB ----------
score_diff = team1 - team2
win_prob_1 = 50 + score_diff * 6
win_prob_1 = max(0, min(100, win_prob_1))
win_prob_2 = 100 - win_prob_1

# ---------- DECISION ----------
if edge > 5 and time_left <= duration * 0.4:
    decision = "OVER"
    color = "green"
elif edge < -5 and time_left <= duration * 0.4:
    decision = "UNDER"
    color = "red"
else:
    decision = "SKIP"
    color = "gray"

# ---------- STRONG SIGNAL ----------
if abs(edge) > 8 and time_left <= duration * 0.35:
    signal = "🔥 STRONG SIGNAL"
else:
    signal = ""

# ---------- TRAP DETECTION ----------
trap = ""
if elapsed < duration * 0.3 and abs(edge) > 6:
    trap = "⚠️ Possible Early Trap"

if elapsed > duration * 0.7 and abs(edge) < 3:
    trap = "⚠️ Low Value / Slow Game"

# ---------- STORE ----------
if game_id not in st.session_state.history:
    st.session_state.history[game_id] = []

st.session_state.history[game_id].append(total)

# ---------- OUTPUT ----------
with col2:
    st.subheader("📊 Analysis")

    st.write(f"Projected Total: {round(projected_total)}")
    st.write(f"Edge: {round(edge,2)}")

    st.markdown(
        f"<h2 style='color:{color};text-align:center;'>Decision: {decision}</h2>",
        unsafe_allow_html=True
    )

    if signal:
        st.markdown(f"<h3 style='color:orange;text-align:center;'>{signal}</h3>", unsafe_allow_html=True)

    if trap:
        st.markdown(f"<h4 style='color:red;text-align:center;'>{trap}</h4>", unsafe_allow_html=True)

    st.write(f"🟢 OVER: {over_prob}%")
    st.write(f"🔴 UNDER: {under_prob}%")

    st.subheader("🏆 Win Prediction")
    st.write(f"Team 1: {round(win_prob_1)}%")
    st.write(f"Team 2: {round(win_prob_2)}%")

# ---------- ALERT ----------
if decision in ["OVER", "UNDER"] and abs(edge) > 5:
    st.markdown(
        """
        <audio autoplay>
          <source src="https://www.soundjay.com/button/beep-07.mp3" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True
    )

# ---------- GRAPH ----------
st.subheader("📈 Score Trend")

fig, ax = plt.subplots()
ax.plot(st.session_state.history[game_id], marker='o')
ax.set_xlabel("Updates")
ax.set_ylabel("Total Score")
ax.set_title(f"{game_id}")

st.pyplot(fig)

# ---------- MULTI GAME ----------
st.subheader("📋 Active Games")

for gid in st.session_state.history:
    last = st.session_state.history[gid][-1]
    st.write(f"{gid} → {last}")
