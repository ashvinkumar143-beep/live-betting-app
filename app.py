import streamlit as st
import time

st.set_page_config(page_title="V27 Auto Betting Tool", layout="centered")

# =============================
# SETTINGS
# =============================
st.sidebar.title("⚙️ Settings")

auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)
refresh_sec = st.sidebar.slider("Refresh Seconds", 2, 10, 3)

mode = st.radio("Select Mode", ["🏀 Basketball", "🎾 Tennis"])

# =============================
# 🏀 BASKETBALL
# =============================
if mode == "🏀 Basketball":

    st.title("🏀 Quarter Pace Predictor")

    score1 = st.number_input("Score 1", value=0)
    score2 = st.number_input("Score 2", value=0)

    quarter = st.selectbox("Quarter", [1,2,3,4])
    minutes = st.number_input("Minutes Elapsed", min_value=0.1, value=5.0)

    duration = st.selectbox("Quarter Duration", [10, 12])
    line = st.number_input("Quarter Line", value=40.0)

    total = score1 + score2

    # Pace
    pace = total / minutes

    if pace > 4.8:
        pace *= 0.92
    elif pace < 3.2:
        pace *= 1.05

    remaining = duration - minutes

    predicted_remaining = pace * remaining
    quarter_total = total + predicted_remaining

    ratio = 0.5 if total == 0 else score1 / total

    team1_q = quarter_total * ratio
    team2_q = quarter_total * (1 - ratio)

    progress = (quarter - 1) + (minutes / duration)
    full_game = total / progress if progress > 0 else quarter_total * 4

    # Labels
    if pace > 4.5:
        pace_label = "🔥 FAST"
    elif pace < 3.5:
        pace_label = "🧊 SLOW"
    else:
        pace_label = "⚖️ NORMAL"

    if minutes < 3:
        stability = "LOW"
    elif minutes < 6:
        stability = "MEDIUM"
    else:
        stability = "HIGH"

    edge = quarter_total - line

    if edge > 4:
        signal = "🔥 STRONG OVER"
    elif edge > 2:
        signal = "📈 OVER"
    elif edge < -4:
        signal = "❄️ STRONG UNDER"
    elif edge < -2:
        signal = "📉 UNDER"
    else:
        signal = "⚖️ NO BET"

    st.subheader("📊 Prediction")

    st.write(f"Quarter Score 1 → {team1_q:.1f}")
    st.write(f"Quarter Score 2 → {team2_q:.1f}")
    st.write(f"Quarter Total → {quarter_total:.1f}")

    st.write(f"Game Total → {full_game:.1f}")

    st.write(f"Pace → {pace_label}")
    st.write(f"Stability → {stability}")

    st.write("### 🎯 Signal")
    st.write(f"Edge → {edge:.1f}")
    st.write(signal)

    st.write("### ⏳ Remaining Minutes")
    for i in range(1, int(remaining)+1):
        val = total + pace * i
        st.write(f"+{i} min → {val:.1f}")

# =============================
# 🎾 TENNIS
# =============================
else:

    st.title("🎾 Tennis Predictor")

    set1_a = st.number_input("Set 1 A", value=6)
    set1_b = st.number_input("Set 1 B", value=3)

    cur_a = st.number_input("Current A", value=2)
    cur_b = st.number_input("Current B", value=2)

    server = st.selectbox("Server", ["A", "B"])

    serve_a = st.number_input("Serve % A", value=70)
    serve_b = st.number_input("Serve % B", value=62)

    break_a = st.number_input("Break Won A", value=2)
    break_b = st.number_input("Break Won B", value=1)

    faced_a = st.number_input("Break Faced A", value=3)
    faced_b = st.number_input("Break Faced B", value=4)

    line = st.number_input("Total Line", value=21.5)

    server_bonus = 0.5 if server == "A" else -0.5

    set_diff = set1_a - set1_b

    score = (
        (serve_a - serve_b) * 0.05 +
        (break_a - break_b) * 1.2 -
        (faced_a - faced_b) * 0.5 +
        server_bonus +
        (set_diff * 0.3) +
        ((cur_a - cur_b) * 0.5)
    )

    if score > 1:
        winner = "A"
        next_set = "6-4"
    elif score < -1:
        winner = "B"
        next_set = "4-6"
    else:
        winner = "Close"
        next_set = "7-6"

    total_now = set1_a + set1_b + cur_a + cur_b

    add = 5 if abs(cur_a - cur_b) < 2 else 3
    final_total = total_now + add

    low = final_total - 2
    high = final_total + 2

    edge = final_total - line

    if edge > 2:
        signal = "🔥 OVER"
    elif edge < -2:
        signal = "❄️ UNDER"
    else:
        signal = "⚖️ NO BET"

    st.subheader("📊 Prediction")

    st.write(f"Winner → {winner}")
    st.write(f"Next Set → {next_set}")

    st.write("### 📈 Total Games")
    st.write(f"Expected → {final_total:.1f}")
    st.write(f"Range → {low:.1f} to {high:.1f}")

    st.write("### 🎯 Signal")
    st.write(f"Edge → {edge:.1f}")
    st.write(signal)

# =============================
# AUTO REFRESH (SAFE)
# =============================
if auto_refresh:
    time.sleep(refresh_sec)
    st.rerun()
