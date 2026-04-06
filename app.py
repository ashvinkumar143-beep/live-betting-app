import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import json
import os

st.set_page_config(page_title="V20 PRO BET TOOL", layout="centered")
st.title("🏀 V20 – SIMPLE HIGH PROBABILITY TOOL")

# ---------------- SETTINGS ----------------
st.sidebar.header("⚙️ SETTINGS")
line = st.sidebar.number_input("Total Line", 100.0, 300.0, 160.0)
quarter_minutes = st.sidebar.selectbox("Quarter Length", [10, 12])
edge = st.sidebar.slider("Signal Strength", 3, 15, 6)

telegram_token = st.sidebar.text_input("Telegram Token")
telegram_chat_id = st.sidebar.text_input("Chat ID")

# ---------------- TELEGRAM ----------------
def send_telegram(msg):
    if telegram_token and telegram_chat_id:
        try:
            url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
            requests.post(url, data={"chat_id": telegram_chat_id, "text": msg})
        except:
            pass

# ---------------- INPUT ----------------
st.header("📊 LIVE INPUT")

col1, col2 = st.columns(2)
with col1:
    score1 = st.number_input("Team A Score", 0, 200, 50)
with col2:
    score2 = st.number_input("Team B Score", 0, 200, 48)

quarter = st.selectbox("Quarter", [1,2,3,4])
minutes = st.number_input("Minutes Played", 0.0, float(quarter_minutes), 5.0)

# ---------------- CORE CALCULATION ----------------
def calculate():
    total = score1 + score2
    time_played = max(minutes, 1)

    # Stable pace
    pace = total / time_played
    pace = max(2.5, min(pace, 5.5))  # realistic clamp

    remaining = quarter_minutes - minutes

    # Split pace by team ratio
    if total == 0:
        ratio1 = 0.5
        ratio2 = 0.5
    else:
        ratio1 = score1 / total
        ratio2 = score2 / total

    # Remaining points
    remain_total = pace * remaining
    remain_team1 = remain_total * ratio1
    remain_team2 = remain_total * ratio2

    # Quarter END prediction (TEAM LEVEL ✅)
    team1_end = score1 + remain_team1
    team2_end = score2 + remain_team2
    quarter_end_total = team1_end + team2_end

    # Full game projection
    remaining_q = 4 - quarter
    future_pts = pace * quarter_minutes * remaining_q
    final_total = quarter_end_total + future_pts

    # Confidence logic
    diff = final_total - line
    if diff > edge:
        signal = "🔥 OVER"
        confidence = min(100, int(diff * 5))
    elif diff < -edge:
        signal = "❄️ UNDER"
        confidence = min(100, int(abs(diff) * 5))
    else:
        signal = "NO BET"
        confidence = 50

    return pace, remaining, team1_end, team2_end, quarter_end_total, final_total, signal, confidence

# ---------------- RUN ----------------
if st.button("🚀 CALCULATE"):
    pace, rem, t1_end, t2_end, q_end, final_total, signal, conf = calculate()

    st.subheader("📈 RESULT")

    st.write(f"Current Total: {score1 + score2}")
    st.write(f"Pace: {pace:.2f} pts/min")
    st.write(f"Time Remaining: {rem:.1f} min")

    st.markdown("### 🧠 QUARTER END PREDICTION")
    st.write(f"Team A: {t1_end:.1f}")
    st.write(f"Team B: {t2_end:.1f}")
    st.write(f"Total: {q_end:.1f}")

    st.markdown("### 🎯 FINAL GAME PREDICTION")
    st.write(f"Projected Total: {final_total:.1f}")

    st.markdown("### 🔥 SIGNAL")
    st.write(f"{signal} | Confidence: {conf}%")

    # ---------------- MINUTE BREAKDOWN ----------------
    st.markdown("### ⏱️ NEXT MINUTES PROJECTION")

    data = []
    for i in range(1, int(rem)+1):
        pts = pace * i
        data.append(round(pts,1))

    df = pd.DataFrame({
        "Minute Ahead": list(range(1, int(rem)+1)),
        "Expected Total Points Added": data
    })

    st.table(df)

    # ---------------- TELEGRAM ----------------
    if signal != "NO BET":
        msg = f"""🏀 LIVE BET V20

Score: {score1}-{score2}
Q{quarter} | {minutes}min

Quarter End:
A {t1_end:.1f} - B {t2_end:.1f}

Final: {final_total:.1f}

{signal} ({conf}%)
"""
        send_telegram(msg)
