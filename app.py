import streamlit as st
import requests
import json
import os
from datetime import datetime

st.set_page_config(page_title="🏀 V17 GOD BOT ELITE", layout="centered")
st.title("💥 V17 GOD BOT ELITE – LIVE + MANUAL + SMART QUARTER + TELEGRAM + HISTORY")

# ---------------- SETTINGS ----------------
st.sidebar.header("⚙️ SETTINGS")
default_line = st.sidebar.number_input("Default Line", value=50.0)
min_ai_score = st.sidebar.slider("Min AI Score", 60, 100, 75)
quarter_duration = st.sidebar.number_input("Quarter Minutes", 8, 15, 12)

telegram_token = st.sidebar.text_input("Telegram Token")
telegram_chat_id = st.sidebar.text_input("Telegram Chat ID")

simulate_live = st.sidebar.checkbox("Simulate Games (if no live)")

history_file = "history.json"

# ---------------- NCAA API ----------------
@st.cache_data(ttl=30)
def fetch_ncaa():
    try:
        today = datetime.now()
        url = f"https://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/{today.year}/{today.month}/{today.day}/all-conf"
        r = requests.get(url)
        data = r.json()
        return data.get("games", [])
    except:
        return []

# ---------------- SIMULATION ----------------
def simulate_games():
    # Simulated NBA / CBA / Euro fallback
    return [
        {"teams": ["Lakers", "Warriors"], "score": [55, 52], "status": "Q3 06:00", "period": 3},
        {"teams": ["CBA Team A", "CBA Team B"], "score": [48, 50], "status": "Q2 04:00", "period": 2},
        {"teams": ["Euro Team X", "Euro Team Y"], "score": [60, 57], "status": "Q1 08:00", "period": 1},
    ]

# ---------------- TIME ----------------
def calc_elapsed(status, period):
    try:
        if ":" in status:
            t = status.split(" ")[-1]
            m, s = t.split(":")
            remain = int(m) + int(s)/60
            elapsed = (period - 1) * quarter_duration + (quarter_duration - remain)
        else:
            elapsed = period * (quarter_duration/2)
    except:
        elapsed = period * (quarter_duration/2)
    return max(1, elapsed)

# ---------------- AI CORE ----------------
def ai(p1, p2, elapsed, line):
    total = p1 + p2
    pace = total / elapsed

    full_time = quarter_duration * 4
    remain = max(full_time - elapsed, 0)

    pred_total = total + pace * remain
    pred_total = min(pred_total, total + 120)

    diff = pred_total - line

    # pace label
    if pace > 2.6:
        pace_label = "🔥 FAST"
    elif pace < 1.8:
        pace_label = "🐢 SLOW"
    else:
        pace_label = "⚖️ NORMAL"

    # scoring
    score = 50
    score += 25 if pace > 2.5 else -20 if pace < 1.9 else 0
    score += 30 if abs(diff) > 10 else -20 if abs(diff) < 4 else 0
    score = max(0, min(100, score))

    # signal
    if diff > 5:
        signal = "OVER"
    elif diff < -5:
        signal = "UNDER"
    else:
        signal = "NO EDGE"

    # decision
    if score >= 85:
        decision = f"💰 GOD BET {signal}"
    elif score >= 75:
        decision = f"🔥 STRONG {signal}"
    elif score >= 65:
        decision = f"✅ {signal}"
    else:
        decision = "⚠️ WAIT"

    # quarter projection
    remain_q = max(quarter_duration - (elapsed % quarter_duration), 0)
    quarter_points = pace * remain_q

    return pred_total, pace_label, signal, decision, score, quarter_points

# ---------------- TELEGRAM ----------------
def send_telegram(msg):
    if telegram_token and telegram_chat_id:
        try:
            url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
            requests.post(url, data={"chat_id": telegram_chat_id, "text": msg})
        except:
            pass

# ---------------- HISTORY ----------------
def save_history(data):
    hist = []
    if os.path.exists(history_file):
        try:
            hist = json.load(open(history_file))
        except:
            hist = []
    hist.append(data)
    json.dump(hist, open(history_file, "w"), indent=2)

# ---------------- HISTORY SIDEBAR ----------------
st.sidebar.header("📊 HISTORY")
if os.path.exists(history_file):
    try:
        hist = json.load(open(history_file))
        for h in hist[-10:]:
            st.sidebar.write(f"{h['time']} | {h['game']} | {h['decision']} | Score {h['score']}")
    except:
        st.sidebar.write("No history yet.")
else:
    st.sidebar.write("No history yet.")

# ---------------- LIVE MODE ----------------
st.header("📡 LIVE MODE")
if st.button("SCAN LIVE"):
    games = fetch_ncaa()
    if not games and simulate_live:
        games = simulate_games()
    if not games:
        st.warning("No live games now")
    else:
        for g in games:
            try:
                t1, t2 = g["teams"]
                p1, p2 = g["score"]
                status = g["status"]
                period = g["period"]

                if "Final" in str(status):
                    continue

                elapsed = calc_elapsed(status, period)
                pred, pace, signal, decision, score, q_pts = ai(p1, p2, elapsed, default_line)

                if score >= min_ai_score:
                    st.markdown("---")
                    st.subheader(f"{t1} vs {t2}")
                    st.write(f"{p1} - {p2} | {status}")
                    st.write(f"Predicted Total: {round(pred,1)}")
                    st.write(f"Pace: {pace}")
                    st.write(f"Quarter Remaining Points: {round(q_pts,1)}")
                    st.write(f"Signal: {signal}")
                    st.write(f"Score: {score}")
                    st.write(f"Decision: {decision}")

                    msg = f"{t1} vs {t2}\n{p1}-{p2}\n{decision}"
                    send_telegram(msg)
                    save_history({
                        "time": str(datetime.now()),
                        "game": f"{t1} vs {t2}",
                        "decision": decision,
                        "score": score
                    })

            except:
                continue

# ---------------- MANUAL MODE ----------------
st.header("✍️ MANUAL MODE")
team1 = st.text_input("Team 1")
team2 = st.text_input("Team 2")
p1 = st.number_input("Team1 Points", 0, 200, 50)
p2 = st.number_input("Team2 Points", 0, 200, 48)
elapsed = st.number_input("Minutes Elapsed", 1, 48, 12)
line = st.number_input("Line", 0.0, 300.0, 50.0)

if st.button("CALCULATE"):
    pred, pace, signal, decision, score, q_pts = ai(p1, p2, elapsed, line)
    st.subheader(f"{team1} vs {team2}")
    st.write(f"Predicted Total: {round(pred,1)}")
    st.write(f"Pace: {pace}")
    st.write(f"Quarter Remaining Points: {round(q_pts,1)}")
    st.write(f"Signal: {signal}")
    st.write(f"Score: {score}")
    st.write(f"Decision: {decision}")

    msg = f"{team1} vs {team2}\n{p1}-{p2}\n{decision}"
    send_telegram(msg)

    save_history({
        "time": str(datetime.now()),
        "game": f"{team1} vs {team2}",
        "decision": decision,
        "score": score
    })
