import streamlit as st
import requests
import json
import os
from datetime import datetime
import random

st.set_page_config(page_title="🏀 V18 BET TOOL", layout="centered")
st.title("🏀 V18 – Quarter & Minute Prediction Betting Tool")

# ---------------- SETTINGS ----------------
st.sidebar.header("⚙️ SETTINGS")
default_line = st.sidebar.number_input("Default Line (Total Points)", 0.0, 300.0, 50.0)
min_signal_diff = st.sidebar.number_input("Min Points Difference for Signal", 1, 20, 5)
quarter_duration = st.sidebar.number_input("Quarter Duration (minutes)", 8, 15, 12)

telegram_token = st.sidebar.text_input("Telegram Token")
telegram_chat_id = st.sidebar.text_input("Telegram Chat ID")

history_file = "history.json"

# ---------------- HISTORY ----------------
def save_history(data):
    hist = []
    if os.path.exists(history_file):
        try:
            hist = json.load(open(history_file))
        except:
            hist = []
    hist.append(data)
    if len(hist) > 50:
        hist = hist[-50:]
    json.dump(hist, open(history_file, "w"), indent=2)

st.sidebar.header("📊 HISTORY (last 10)")
if os.path.exists(history_file):
    try:
        hist = json.load(open(history_file))
        for h in hist[-10:]:
            st.sidebar.write(f"{h['time']} | {h['game']} | {h['signal']} | {h['pred_total']:.1f}")
    except:
        st.sidebar.write("No history yet.")
else:
    st.sidebar.write("No history yet.")

# ---------------- TELEGRAM ----------------
def send_telegram(msg):
    if telegram_token and telegram_chat_id:
        try:
            url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
            requests.post(url, data={"chat_id": telegram_chat_id, "text": msg})
        except:
            pass

# ---------------- PREDICTION ----------------
def predict_quarter(team1_score, team2_score, quarter_num, minutes_elapsed, line, league="NBA"):
    # League avg points per quarter per team
    league_avg = {"NBA": 25, "CBA": 22, "Euro": 20, "NCAA": 18}
    avg_per_quarter = league_avg.get(league, 22)
    
    current_q_points = team1_score + team2_score
    remaining_minutes = quarter_duration - minutes_elapsed
    if remaining_minutes < 0:
        remaining_minutes = 0.1  # avoid zero division
    
    # Pace per minute
    pace = current_q_points / max(minutes_elapsed, 1)
    
    # Predict remaining points in current quarter
    adjust = random.uniform(0.9,1.1)
    remaining_points = pace * remaining_minutes * adjust
    
    # Total predicted points for this quarter
    pred_q_total = current_q_points + remaining_points
    
    # Project full game total (simplified)
    remaining_quarters = 4 - quarter_num
    avg_remaining_points = avg_per_quarter * 2 * remaining_quarters
    pred_total = pred_q_total + avg_remaining_points
    
    # Signal
    if pred_total > line + min_signal_diff:
        signal = "OVER"
    elif pred_total < line - min_signal_diff:
        signal = "UNDER"
    else:
        signal = "NO EDGE"
    
    # Per-minute breakdown
    per_minute = {}
    for m in range(1, int(remaining_minutes)+1):
        per_minute[m] = pace * m * adjust
    
    return pred_total, pred_q_total, signal, per_minute

# ---------------- MANUAL INPUT ----------------
st.header("✍️ Manual Input Mode")
team1 = st.text_input("Team 1")
team2 = st.text_input("Team 2")
team1_score = st.number_input("Team 1 Current Points", 0, 200, 50)
team2_score = st.number_input("Team 2 Current Points", 0, 200, 48)
quarter_num = st.number_input("Quarter Number", 1, 4, 1)
minutes_elapsed = st.number_input("Minutes Elapsed in Quarter", 0, quarter_duration, 5)
line = st.number_input("Line (Total Points)", 0.0, 300.0, default_line)
league = st.selectbox("League", ["NBA","CBA","Euro","NCAA"])

if st.button("Calculate Prediction"):
    pred_total, pred_q_total, signal, per_minute = predict_quarter(
        team1_score, team2_score, quarter_num, minutes_elapsed, line, league
    )
    
    st.subheader(f"{team1} vs {team2} | Quarter {quarter_num}")
    st.write
