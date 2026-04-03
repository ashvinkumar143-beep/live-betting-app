import streamlit as st
import time
import requests
import pandas as pd

st.set_page_config(page_title="Live Betting Predictor PRO", layout="wide")

API_KEY = "b9184d5537fc4e9ad41896f691476a90"

# ---------------- GET GAMES ----------------
def get_live_games():
    try:
        url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/scores/?apiKey={API_KEY}&daysFrom=1"
        res = requests.get(url)
        data = res.json()

        games = []

        if data:
            for g in data:
                scores = g.get("scores")
                if scores and len(scores) >= 2:
                    games.append({
                        "teams": g.get("teams", ["Team A", "Team B"]),
                        "score": {
                            "A": int(scores[0].get("score", 0)),
                            "B": int(scores[1].get("score", 0))
                        },
                        "time_left": 50,
                        "line": 210
                    })

        if not games:
            games = [
                {"teams": ["Lakers", "Warriors"], "score": {"A": 110, "B": 115}, "time_left": 10, "line": 220}
            ]

        return games
    except:
        return [{"teams": ["Demo A", "Demo B"], "score": {"A": 100, "B": 105}, "time_left": 20, "line": 210}]

# ---------------- MODEL ----------------
def model(total, line, time_left):
    duration = 100
    edge = total - line
    prob = 50 + edge * 2
    prob = max(10, min(90, prob))
    return int(prob), int(100 - prob)

# ---------------- UI ----------------
st.title("🔥 Live Betting Predictor PRO")

games = get_live_games()

options = [f"{i} - {g['teams'][0]} vs {g['teams'][1]}" for i, g in enumerate(games)]
selected = st.selectbox("Select Game", options)

game = games[int(selected.split(" - ")[0])]

total = game["score"]["A"] + game["score"]["B"]
over, under = model(total, game["line"], game["time_left"])

# ---------------- DISPLAY ----------------
col1, col2, col3 = st.columns(3)

col1.metric("🏀 Total Score", total)
col2.metric("🟢 OVER %", f"{over}%")
col3.metric("🔴 UNDER %", f"{under}%")

# Progress bars
st.progress(over / 100)
st.progress(under / 100)

# Decision
if over > 65:
    st.success("🔥 STRONG OVER SIGNAL")
    st.balloons()
elif under > 65:
    st.error("❄️ STRONG UNDER SIGNAL")
else:
    st.warning("⚖️ NO CLEAR BET")

# Graph
st.subheader("📈 Trend")
df = pd.DataFrame({
    "Step": [1,2,3,4,5],
    "Score": [total-10, total-5, total, total+3, total+5]
})
st.line_chart(df.set_index("Step"))

# Auto refresh
auto = st.checkbox("Auto Refresh (10s)")
if auto:
    time.sleep(10)
    st.rerun()
