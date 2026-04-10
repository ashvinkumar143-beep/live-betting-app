import streamlit as st
import time

st.set_page_config(page_title="V26 Ultra Smart Betting Tool", layout="centered")

# =============================
# AUTO REFRESH (SAFE VERSION)
# =============================
refresh_rate = st.sidebar.slider("Auto Refresh (seconds)", 0, 10, 3)

if refresh_rate > 0:
    time.sleep(refresh_rate)
    st.rerun()

# =============================
# SETTINGS
# =============================
st.sidebar.title("⚙️ Settings")

boost = st.sidebar.slider("Manual Boost (%)", -10, 10, 0)

mode = st.radio("Select Mode", ["🏀 Basketball", "🎾 Tennis"])

# =============================
# 🏀 BASKETBALL
# =============================
if mode == "🏀 Basketball":

    st.title("🏀 Smart Pace Predictor")

    score1 = st.number_input("Score 1", 0, 200, 50)
    score2 = st.number_input("Score 2", 0, 200, 48)

    quarter = st.selectbox("Quarter", [1,2,3,4])
    minutes = st.number_input("Minutes Elapsed", 0.1, 12.0, 6.0)

    duration = st.selectbox("Quarter Duration", [10, 12])
    line = st.number_input("Line", value=160.0)

    total = score1 + score2

    # =============================
    # SMART PACE LOGIC
    # =============================
    pace = total / minutes

    # Slow down unrealistic pace
    if pace > 6:
        pace *= 0.92
    elif pace < 3:
        pace *= 1.05

    remaining = duration - minutes

    predicted_remaining = pace * remaining

    quarter_total = total + predicted_remaining

    # Game projection using quarter weighting
    progress = (quarter - 1) + (minutes / duration)

    if progress == 0:
        full_game = quarter_total * 4
    else:
        full_game = total / progress

    # BOOST
    full_game *= (1 + boost/100)

    # Split teams
    ratio = 0.5 if total == 0 else score1 / total

    pred1 = full_game * ratio
    pred2 = full_game * (1 - ratio)

    # EDGE FILTER (smarter)
    edge = full_game - line

    if edge > 6:
        signal = "🔥 STRONG OVER"
    elif edge > 2:
        signal = "📈 OVER"
    elif edge < -6:
        signal = "❄️ STRONG UNDER"
    elif edge < -2:
        signal = "📉 UNDER"
    else:
        signal = "⚖️ NO BET"

    # =============================
    # OUTPUT
    # =============================
    st.subheader("📊 Prediction")

    st.write(f"Predicted Score 1 → {pred1:.1f}")
    st.write(f"Predicted Score 2 → {pred2:.1f}")
    st.write(f"Game Total → {full_game:.1f}")

    st.write(f"Quarter Projection → {quarter_total:.1f}")

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

    st.title("🎾 Smart Set Predictor")

    set1_a = st.number_input("Set 1 A", 0, 7, 6)
    set1_b = st.number_input("Set 1 B", 0, 7, 3)

    set2_on = st.checkbox("Set 2 Played")

    if set2_on:
        set2_a = st.number_input("Set 2 A", 0, 7, 4)
        set2_b = st.number_input("Set 2 B", 0, 7, 6)
    else:
        set2_a = 0
        set2_b = 0

    cur_a = st.number_input("Current A", 0, 7, 2)
    cur_b = st.number_input("Current B", 0, 7, 1)

    line = st.number_input("Line", value=21.5)

    # =============================
    # LOGIC
    # =============================
    diff1 = set1_a - set1_b

    momentum = 1 if diff1 > 0 else -1

    if set2_on:
        diff2 = set2_a - set2_b
        momentum += 1 if diff2 > 0 else -1

    current_diff = cur_a - cur_b

    score = momentum + (current_diff * 0.7)

    if score > 1:
        winner = "A"
        next_set = "6-3 / 6-4"
    elif score < -1:
        winner = "B"
        next_set = "3-6 / 4-6"
    else:
        winner = "Close"
        next_set = "7-6"

    total = set1_a + set1_b + set2_a + set2_b + cur_a + cur_b

    add = 4 if abs(current_diff) < 2 else 3

    final_total = total + add

    # BOOST
    final_total *= (1 + boost/100)

    low = final_total - 2
    high = final_total + 2

    edge = final_total - line

    if edge > 2:
        signal = "🔥 OVER"
    elif edge < -2:
        signal = "❄️ UNDER"
    else:
        signal = "⚖️ NO BET"

    # =============================
    # OUTPUT
    # =============================
    st.subheader("📊 Prediction")

    st.write(f"Winner → {winner}")
    st.write(f"Next Set → {next_set}")

    st.write("### 📈 Total Games")
    st.write(f"Expected → {final_total:.1f}")
    st.write(f"Range → {low:.1f} to {high:.1f}")

    st.write("### 🎯 Signal")
    st.write(f"Edge → {edge:.1f}")
    st.write(signal)
