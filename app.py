import streamlit as st
import time

st.set_page_config(page_title="V23 Smart Betting Tool", layout="wide")

# =============================
# AUTO REFRESH (IMPORTANT)
# =============================
refresh_rate = 3  # seconds
st.empty()
time.sleep(refresh_rate)
st.experimental_rerun()

# =============================
# MODE SELECT
# =============================
mode = st.sidebar.selectbox("Select Mode", ["Basketball", "Table Tennis"])

# =============================
# SETTINGS
# =============================
line = st.sidebar.number_input("Default Line", value=150.0)
quarter_duration = st.sidebar.selectbox("Quarter Duration", [10, 12])
boost = st.sidebar.slider("Manual Boost (%)", -10, 10, 0)

# =============================
# 🏀 BASKETBALL MODE
# =============================
if mode == "Basketball":

    st.title("🏀 Basketball Live Predictor")

    col1, col2 = st.columns(2)

    with col1:
        score1 = st.number_input("Team 1 Score", 0, 200, 0)
        score2 = st.number_input("Team 2 Score", 0, 200, 0)

    with col2:
        quarter = st.selectbox("Quarter", [1,2,3,4])
        minutes = st.number_input("Minutes Elapsed", 0.1, float(quarter_duration), 5.0)

    total = score1 + score2

    # SAFE CALCULATION
    if minutes > 0:
        pace = total / minutes
    else:
        pace = 0

    remaining = quarter_duration - minutes
    remain_pts = pace * remaining

    # Boost adjust
    remain_pts = remain_pts * (1 + boost/100)

    # Team split
    ratio1 = score1 / total if total > 0 else 0.5
    ratio2 = score2 / total if total > 0 else 0.5

    t1_pred = score1 + remain_pts * ratio1
    t2_pred = score2 + remain_pts * ratio2

    quarter_total = t1_pred + t2_pred
    full_game = (quarter_total * 4) / quarter

    edge = full_game - line

    if edge > 8:
        signal = "🔥 OVER"
    elif edge < -8:
        signal = "❄️ UNDER"
    else:
        signal = "⚖️ NO BET"

    # OUTPUT
    st.subheader("📊 Prediction")

    st.write(f"Current Score → {score1} : {score2}")
    st.write(f"Pace → {pace:.2f}")

    st.write("### 🧠 Quarter Prediction")
    st.write(f"Team 1 → {t1_pred:.1f}")
    st.write(f"Team 2 → {t2_pred:.1f}")
    st.write(f"Quarter Total → {quarter_total:.1f}")

    st.write("### 📈 Full Game")
    st.write(f"Predicted Total → {full_game:.1f}")

    st.write("### 🎯 Decision")
    st.write(f"Edge → {edge:.1f}")
    st.write(f"Signal → {signal}")

    st.write("### ⏱ Remaining Minutes Projection")
    for i in range(1, int(remaining)+1):
        st.write(f"+{i} min → {(pace*i):.1f} pts")


# =============================
# 🏓 TABLE TENNIS MODE (FIXED)
# =============================
else:

    st.title("🏓 Table Tennis Smart Tool")

    col1, col2 = st.columns(2)

    with col1:
        p1 = st.text_input("Player A", "A")
        score1 = st.number_input("Score A", 0, 20, 8)

    with col2:
        p2 = st.text_input("Player B", "B")
        score2 = st.number_input("Score B", 0, 20, 6)

    server = st.selectbox("Server", ["A", "B"])

    diff = score1 - score2

    # MOMENTUM
    if abs(diff) <= 1:
        momentum = "⚖️ Balanced"
    elif abs(diff) == 2:
        momentum = "➕ Slight Lead"
    else:
        momentum = "🔥 Strong Control"

    leader = p1 if diff > 0 else p2

    # EXPECTED FINISH
    if abs(diff) >= 3:
        finish = f"{leader} 11-{min(score1,score2)+2}"
    else:
        finish = f"{leader} 11-{min(score1,score2)+3}"

    # PRESSURE
    if max(score1, score2) < 8:
        pressure = "Normal"
    elif max(score1, score2) < 10:
        pressure = "Rising"
    else:
        pressure = "🔥 Clutch"

    # EDGE
    edge = "Lean A" if diff > 1 else "Lean B" if diff < -1 else "No Edge"

    # OUTPUT
    st.subheader("📊 Analysis")

    st.write(f"Score → {p1} {score1} - {score2} {p2}")

    st.write(f"📊 Momentum → {momentum}")
    st.write(f"🎯 Expected Finish → {finish}")
    st.write(f"🔥 Pressure → {pressure}")
    st.write(f"⚡ Server → {server} advantage")
    st.write(f"📈 Edge → {edge}")
