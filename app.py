import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="V21 AUTO PRO", layout="centered")
st.title("🏀 V21 AUTO PRO (STABLE)")

# ---------------- SETTINGS ----------------
st.sidebar.header("⚙️ SETTINGS")

line = st.sidebar.number_input("Total Line", 100.0, 300.0, 160.0)
quarter_minutes = st.sidebar.selectbox("Quarter Length", [10, 12])
edge = st.sidebar.slider("Signal Strength", 4, 15, 7)
refresh_rate = st.sidebar.slider("Auto Refresh (sec)", 3, 20, 5)

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

# ---------------- CALCULATION ----------------
def calculate():
    total = score1 + score2
    time_played = max(minutes, 1)

    pace = total / time_played
    pace = max(2.5, min(pace, 5.5))

    remaining = quarter_minutes - minutes

    if total == 0:
        r1, r2 = 0.5, 0.5
    else:
        r1 = score1 / total
        r2 = score2 / total

    remain_total = pace * remaining
    t1_end = score1 + (remain_total * r1)
    t2_end = score2 + (remain_total * r2)

    q_end = t1_end + t2_end

    remaining_q = 4 - quarter
    future_pts = pace * quarter_minutes * remaining_q
    final_total = q_end + future_pts

    diff = final_total - line

    if diff > edge:
        signal = "🔥 OVER"
        conf = min(100, int(diff * 5))
    elif diff < -edge:
        signal = "❄️ UNDER"
        conf = min(100, int(abs(diff) * 5))
    else:
        signal = "NO BET"
        conf = 50

    return pace, remaining, t1_end, t2_end, q_end, final_total, signal, conf

# ---------------- AUTO TOGGLE ----------------
auto = st.checkbox("🔄 Auto Refresh")

# ---------------- DISPLAY ----------------
placeholder = st.empty()

def run_app():
    with placeholder.container():
        pace, rem, t1_end, t2_end, q_end, final_total, signal, conf = calculate()

        st.subheader("📈 RESULT")

        st.write(f"Score: {score1} - {score2}")
        st.write(f"Pace: {pace:.2f} pts/min")

        st.markdown("### 🧠 Quarter End")
        st.write(f"A: {t1_end:.1f} | B: {t2_end:.1f}")
        st.write(f"Total: {q_end:.1f}")

        st.markdown("### 🎯 Final")
        st.write(f"{final_total:.1f}")

        st.markdown("### 🔥 Signal")
        st.write(f"{signal} | {conf}%")

        # minute projection
        st.markdown("### ⏱️ Next Minutes")
        mins = int(rem)
        data = [round(pace * i,1) for i in range(1, mins+1)]

        df = pd.DataFrame({
            "Minute Ahead": list(range(1, mins+1)),
            "Expected Points": data
        })
        st.table(df)

        # Telegram alert (only strong)
        if conf >= 75 and signal != "NO BET":
            msg = f"""🏀 LIVE ALERT

Score: {score1}-{score2}
Q{quarter}

Quarter End: {q_end:.1f}
Final: {final_total:.1f}

{signal} ({conf}%)
"""
            send_telegram(msg)

# Run once
run_app()

# Auto refresh
if auto:
    time.sleep(refresh_rate)
    st.rerun()
