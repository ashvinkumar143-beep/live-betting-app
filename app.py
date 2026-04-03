import streamlit as st
import time
import requests

st.set_page_config(page_title="Pro Sports Predictor PRO", layout="wide")

# ---------------- API CONFIG ----------------
API_KEY = "b9184d5537fc4e9ad41896f691476a90"

# ---------------- LIVE API ----------------
def get_live_games():
    try:
        url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/scores/?apiKey={API_KEY}&daysFrom=1"
        res = requests.get(url)
        data = res.json()

        games = []

        for g in data:
            if "scores" in g and len(g["scores"]) >= 2:
                scoreA = int(g["scores"][0].get("score", 0))
                scoreB = int(g["scores"][1].get("score", 0))

                teams = g.get("teams", ["Team A", "Team B"])

                games.append({
                    "teams": teams,
                    "score": {"A": scoreA, "B": scoreB},
                    "time_left": 50,
                    "line": scoreA + scoreB + 5
                })

        return games

    except Exception as e:
        st.error(f"API Error: {e}")
        return []

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
st.title("🔥 PRO SPORTS AI DASHBOARD")

games = get_live_games()

if not games:
    st.warning("No live games now OR API limit reached")
else:
    options = [f"{i} - {g['teams'][0]} vs {g['teams'][1]}" for i, g in enumerate(games)]
    selected = st.selectbox("Select Game", options)

    idx = int(selected.split(" - ")[0])
    game = games[idx]

    total = sum(game["score"].values())
    over, under = basketball_model(total, game["line"], game["time_left"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Score", total)
    col2.metric("OVER %", f"{over}%")
    col3.metric("UNDER %", f"{under}%")

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
