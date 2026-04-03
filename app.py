import streamlit as st
import requests
import time
import pandas as pd

st.set_page_config(page_title="🔥 AI Betting PRO MAX", layout="wide")

# ---------------- KEYS ----------------
API_KEY = "b9184d5537fc4e9ad41896f691476a90"
BOT_TOKEN = "8693963685:AAFP9lmvOQFpLlRXp31sYYNEEA2-2wNHVjo"
CHAT_ID = "6518682986"

# ---------------- TELEGRAM ----------------
def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

# ---------------- SESSION ----------------
if "profit" not in st.session_state:
    st.session_state.profit = 0

if "bias" not in st.session_state:
    st.session_state.bias = 0

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- MODEL ----------------
def model(total, line):
    edge = total - line
    prob = 50 + edge * 2 + st.session_state.bias
    return max(5, min(95, prob))

def value(prob, odds):
    implied = 100 / odds
    return prob - implied

# ---------------- UI ----------------
st.title("🔥 AI BETTING PRO MAX (AUTO BOT)")

mode = st.sidebar.radio("Mode", ["Live", "Manual"])
auto = st.sidebar.checkbox("Auto Signals (10s)")

# ================= LIVE =================
if mode == "Live":

    st.subheader("🌐 LIVE AUTO SIGNALS")

    try:
        url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/scores/?apiKey={API_KEY}&daysFrom=1"
        data = requests.get(url).json()

        if not data:
            st.warning("No live matches now")

        for g in data:

            if not g.get("scores"):
                continue

            a = int(g["scores"][0]["score"])
            b = int(g["scores"][1]["score"])

            total = a + b
            line = total + 5

            prob = model(total, line)

            # -------- SIMULATED REAL ODDS --------
            odds_over = 1.85
            odds_under = 1.95

            value_over = value(prob, odds_over)
            value_under = value(100 - prob, odds_under)

            st.markdown(f"### {g['teams'][0]} vs {g['teams'][1]}")
            st.write(f"Score: {a} - {b}")

            st.progress(prob / 100)
            st.write(f"🟢 OVER {int(prob)}% | Odds {odds_over}")
            st.write(f"🔴 UNDER {100-int(prob)}% | Odds {odds_under}")

            # -------- SIGNAL BOT --------
            if value_over > 10:
                msg = f"🔥 OVER BET\n{g['teams'][0]} vs {g['teams'][1]}\nProb: {int(prob)}%"
                st.success(msg)
                send_telegram(msg)

            elif value_under > 10:
                msg = f"❄️ UNDER BET\n{g['teams'][0]} vs {g['teams'][1]}\nProb: {100-int(prob)}%"
                st.error(msg)
                send_telegram(msg)

            else:
                st.info("No strong value")

    except:
        st.error("API error (use Manual mode)")

# ================= MANUAL =================
if mode == "Manual":

    sport = st.selectbox("Sport", ["Basketball","Soccer","Tennis"])

    if sport == "Basketball":
        a = st.number_input("Score A", 0, 200, 60)
        b = st.number_input("Score B", 0, 200, 58)
        line = st.number_input("Line", 150, 300, 210)
        total = a + b

    elif sport == "Soccer":
        a = st.number_input("Goals A", 0, 10, 1)
        b = st.number_input("Goals B", 0, 10, 1)
        line = st.number_input("Line", 0.5, 5.0, 2.5)
        total = a + b

    else:
        s1 = st.number_input("P1 Sets", 0, 3, 1)
        s2 = st.number_input("P2 Sets", 0, 3, 1)
        total = (s1 - s2) * 10
        line = 0

    prob = model(total, line)

    odds = st.number_input("Odds", 1.1, 5.0, 1.90)
    val = value(prob, odds)

    st.progress(prob / 100)
    st.write(f"Prob: {int(prob)}%")
    st.write(f"Value: {round(val,2)}")

    if val > 10:
        st.success("🔥 VALUE BET")

        if st.button("Send Telegram Alert"):
            send_telegram(f"🔥 MANUAL BET\nProb {int(prob)}%")

    # -------- PROFIT TRACKER --------
    st.subheader("💰 Profit Tracker")

    if st.button("Win"):
        st.session_state.profit += (odds - 1)

    if st.button("Loss"):
        st.session_state.profit -= 1

    st.write(f"Total Profit: {round(st.session_state.profit,2)} units")

# ================= AI LEARNING =================
st.markdown("---")
st.subheader("🧠 AI Learning")

if st.button("Correct Prediction"):
    st.session_state.bias += 1

if st.button("Wrong Prediction"):
    st.session_state.bias -= 1

st.write(f"Model Bias: {st.session_state.bias}")

# ---------------- AUTO REFRESH ----------------
if auto:
    time.sleep(10)
    st.rerun()
