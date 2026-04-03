import streamlit as st
import time
import requests

st.set_page_config(page_title="Pro Sports Predictor", layout="wide")

# ---------------- API KEY ----------------
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
                    scoreA = int(scores[0].get("score", 0))
                    scoreB = int(scores[1].get("score", 0))

                    teams = g.get("teams", ["Team A", "Team B"])

                    games.append({
                        "teams": teams,
                        "score": {"A": scoreA, "B": scoreB},
                        "time_left": 50,
                        "line": scoreA + scoreB + 5
                    })

        # 🔥 IF NO LIVE GAMES → USE DEMO
        if not games:
            games = [
                {"teams": ["Lakers", "Warriors"], "score": {"A": 55, "B": 60}, "time_left": 30, "line": 215},
                {"teams": ["Celtics", "Heat"], "score": {"A": 80, "B": 78}, "time_left": 15, "line": 210},
                {"teams": ["Bulls", "Knicks"], "score": {"A": 45, "B": 50}, "time_left": 70, "line": 205},
            ]

        return games

    except:
        # 🔥 fallback demo if API fails
        return [
            {"teams": ["Demo A", "Demo B"], "score": {"A": 50, "B": 52}, "time_left": 40, "line": 200}
        ]

# ---------------- MODEL ----------------
def basketball_model(total, line, time_left):
    duration = 100
    edge = total - line

    time_factor = ((duration - time_left) / duration) ** 1.2
    prob = 50 + (edge * 2.5 * time_factor)

    if time_left <= 20:
        prob += edge * 1.5

    prob = max(20, min(85, prob))

    return round(prob), round(100 - prob)

# ---------------- UI ----------------
st.title("🔥 Live Betting Predictor")

games = get_live_games()

options = [f"{i} - {g['teams'][0]} vs {g['teams'][1]}" for i, g in enumerate(games)]
selected = st.selectbox("Select Game", options)

idx = int(selected.split(" - ")[0])
game = games[idx]

total = game["score"]["A"] + game["score"]["B"]
over, under = basketball_model(total, game["line"], game["time_left"])

col1, col2, col3 = st.columns(3)

col1.metric("Total Score", total)
col2.metric("OVER %", f"{over}%")
col3.metric("UNDER %", f"{under}%")

# ---------------- DECISION ----------------
if over > 65:
    st.success("🔥 BET OVER")
elif under > 65:
    st.error("❄️ BET UNDER")
else:
    st.warning("⚖️ NO CLEAR BET")

# ---------------- AUTO REFRESH ----------------
auto = st.checkbox("Auto Refresh (10s)")

if auto:
    time.sleep(10)
    st.rerun()
