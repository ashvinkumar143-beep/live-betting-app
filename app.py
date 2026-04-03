import streamlit as st
import time

st.set_page_config(page_title="Live Betting Predictor", layout="wide")

st.title("🔥 Live Betting Predictor (Easy Version)")

# ---------------- SELECT SPORT ----------------
sport = st.selectbox("Select Sport", ["Basketball", "Tennis"])

# ================= BASKETBALL =================
if sport == "Basketball":

    st.subheader("🏀 Basketball Live Input")

    col1, col2 = st.columns(2)

    with col1:
        teamA = st.number_input("Team A Score", 0, 200, 100)
        teamB = st.number_input("Team B Score", 0, 200, 98)

        quarter = st.selectbox("Quarter", [1, 2, 3, 4])
        time_left = st.number_input("Seconds Left in Quarter", 0, 720, 300)

    with col2:
        line = st.number_input("Over/Under Line", 150, 300, 210)

    # -------- CALCULATION --------
    total = teamA + teamB

    # total game time = 48 min = 2880 sec
    elapsed = (quarter - 1) * 720 + (720 - time_left)

    if elapsed > 0:
        pace = total / elapsed
        projected = total + pace * (2880 - elapsed)
    else:
        projected = total

    edge = projected - line

    prob = 50 + edge * 2
    prob = max(10, min(90, prob))

    over = int(prob)
    under = 100 - over

    # -------- OUTPUT --------
    st.subheader("📊 Result")

    st.write(f"Total Score: {total}")
    st.write(f"Projected Total: {int(projected)}")

    col1, col2 = st.columns(2)
    col1.metric("🟢 OVER %", f"{over}%")
    col2.metric("🔴 UNDER %", f"{under}%")

    # Decision
    if over > 65:
        st.success("🔥 STRONG OVER")
    elif under > 65:
        st.error("❄️ STRONG UNDER")
    else:
        st.warning("⚖️ NO CLEAR BET")

# ================= TENNIS =================
if sport == "Tennis":

    st.subheader("🎾 Tennis Live Input")

    p1 = st.number_input("Player 1 Games", 0, 7, 3)
    p2 = st.number_input("Player 2 Games", 0, 7, 2)

    total = p1 + p2
    edge = p1 - p2

    pressure = total / 12

    if p1 >= 5 and p2 >= 5:
        pressure += 0.5

    prob = 50 + edge * 8 * pressure
    prob = max(20, min(80, prob))

    st.subheader("📊 Result")

    col1, col2 = st.columns(2)
    col1.metric("Player 1 %", f"{int(prob)}%")
    col2.metric("Player 2 %", f"{100-int(prob)}%")

    if prob > 65:
        st.success("🔥 Player 1 Strong")
    elif prob < 35:
        st.error("❄️ Player 2 Strong")
    else:
        st.warning("⚖️ Close Match")

# ---------------- AUTO REFRESH ----------------
st.markdown("---")
auto = st.checkbox("Auto Refresh (10s)")

if auto:
    time.sleep(10)
    st.rerun()
