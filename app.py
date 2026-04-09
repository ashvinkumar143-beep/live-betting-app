import streamlit as st
import time

st.set_page_config(page_title="V24 Smart Pace Tool", layout="wide")

# =============================
# AUTO REFRESH
# =============================
refresh_rate = 3
st.sidebar.write(f"Auto refresh: {refresh_rate}s")
time.sleep(refresh_rate)

# =============================
# MODE
# =============================
mode = st.sidebar.selectbox("Mode", ["Basketball", "Table Tennis"])

# =============================
# SETTINGS
# =============================
line = st.sidebar.number_input("Line", value=150.0)
quarter_duration = st.sidebar.selectbox("Quarter Duration", [10, 12])
boost = st.sidebar.slider("Manual Boost (%)", -10, 10, 0)

# =============================
# 🏀 BASKETBALL (SMART PACE)
# =============================
if mode == "Basketball":

    st.title("🏀 V24 Smart Pace Predictor")

    col1, col2 = st.columns(2)

    with col1:
        score1 = st.number_input("Team 1 Score", 0, 200, 0)
        score2 = st.number_input("Team 2 Score", 0, 200, 0)

    with col2:
        quarter = st.selectbox("Quarter", [1,2,3,4])
        minutes = st.number_input("Minutes Elapsed", 0.1, float(quarter_duration), 5.0)

    total = score1 + score2

    # BASE PACE
    base_pace = total / minutes if minutes > 0 else 0

    # =============================
    # SMART PACE ADJUSTMENT
    # =============================
    if minutes < 3:
        pace = base_pace * 0.85   # slow down early hype
    elif minutes <= 8:
        pace = base_pace          # best accuracy zone
    else:
        pace = base_pace * 0.92   # fatigue slowdown

    remaining = quarter_duration - minutes
    remain_pts = pace * remaining

    # BOOST
    remain_pts *= (1 + boost/100)

    # TEAM SPLIT
    ratio1 = score1 / total if total > 0 else 0.5
    ratio2 = score2 / total if total > 0 else 0.5

    t1_pred = score1 + remain_pts * ratio1
    t2_pred = score2 + remain_pts * ratio2

    quarter_total = t1_pred + t2_pred

    # SAFE FULL GAME SCALE
    full_game = (quarter_total * 4) / quarter

    # ANTI CRAZY LIMIT
    if full_game > 260:
        full_game = 260
    if full_game < 120:
        full_game = 120

    edge = full_game - line

    if edge > 10:
        signal = "🔥 STRONG OVER"
    elif edge > 5:
        signal = "OVER"
    elif edge < -10:
        signal = "❄️ STRONG UNDER"
    elif edge < -5:
        signal = "UNDER"
    else:
        signal = "⚖️ NO BET"

    # OUTPUT
    st.subheader("📊 Prediction")

    st.write(f"Score → {score1} : {score2}")
    st.write(f"Base Pace → {base_pace:.2f}")
    st.write(f"Adjusted Pace → {pace:.2f}")

    st.write("### 🧠 Quarter")
    st.write(f"Team 1 → {t1_pred:.1f}")
    st.write(f"Team 2 → {t2_pred:.1f}")
    st.write(f"Total → {quarter_total:.1f}")

    st.write("### 📈 Full Game")
    st.write(f"Prediction → {full_game:.1f}")

    st.write("### 🎯 Signal")
    st.write(f"Edge → {edge:.1f}")
    st.write(f"{signal}")

    st.write("### ⏱ Remaining Minutes")
    for i in range(1, int(remaining)+1):
        st.write(f"+{i} min → {(pace*i):.1f} pts")

# =============================
# 🏓 TABLE TENNIS (CLEAN)
# =============================
else:

    st.title("🏓 Table Tennis Smart Tool")

    col1, col2 = st.columns(2)

    with col1:
        p1 = st.text_input("Player A", "A")
        s1 = st.number_input("Score A", 0, 20, 8)

    with col2:
        p2 = st.text_input("Player B", "B")
        s2 = st.number_input("Score B", 0, 20, 6)

    server = st.selectbox("Server", ["A", "B"])

    diff = s1 - s2

    # MOMENTUM
    if abs(diff) <= 1:
        momentum = "⚖️ Balanced"
    elif abs(diff) == 2:
        momentum = "➕ Slight Lead"
    else:
        momentum = "🔥 Strong"

    leader = p1 if diff > 0 else p2

    # FINISH
    finish = f"{leader} 11-{min(s1,s2)+2}"

    # PRESSURE
    if max(s1,s2) < 8:
        pressure = "Normal"
    elif max(s1,s2) < 10:
        pressure = "Rising"
    else:
        pressure = "🔥 Clutch"

    # EDGE
    if diff > 2:
        edge = "Strong A"
    elif diff > 0:
        edge = "Lean A"
    elif diff < -2:
        edge = "Strong B"
    elif diff < 0:
        edge = "Lean B"
    else:
        edge = "No Edge"

    # OUTPUT
    st.subheader("📊 Analysis")

    st.write(f"{p1} {s1} - {s2} {p2}")
    st.write(f"📊 Momentum → {momentum}")
    st.write(f"🎯 Finish → {finish}")
    st.write(f"🔥 Pressure → {pressure}")
    st.write(f"⚡ Server → {server}")
    st.write(f"📈 Edge → {edge}")
