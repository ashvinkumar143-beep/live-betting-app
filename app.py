import streamlit as st import time import requests import pandas as pd

st.set_page_config(page_title="Pro Sports Predictor PRO", layout="wide")

---------------- API CONFIG ----------------

API_KEY = "b9184d5537fc4e9ad41896f691476a90"  

---------------- LIVE API ----------------

def get_live_games(): try: url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/scores/?apiKey={API_KEY}&daysFrom=1" res = requests.get(url) data = res.json()

games = []
    for g in data:
        if g.get("scores"):
            scoreA = g["scores"][0]["score"]
            scoreB = g["scores"][1]["score"]

            games.append({
                "teams": [g["teams"][0], g["teams"][1]],
                "score": {"A": scoreA, "B": scoreB},
                "time_left": 50,  # API usually doesn't give → simulate
                "line": scoreA + scoreB + 5
            })

    return games
except:
    return []

---------------- BASKETBALL MODEL ----------------

def basketball_model(total, line, time_left): duration = 100 edge = total - line

time_factor = ((duration - time_left) / duration) ** 1.2

prob = 50 + (edge * 2.5 * time_factor)

if time_left <= 20:
    prob += edge * 1.5

prob = max(20, min(85, prob))

return round(prob), round(100 - prob)

---------------- TENNIS MODEL ----------------

def tennis_model(g1, g2): total = g1 + g2 edge = g1 - g2

pressure = total / 12
if g1 >= 5 and g2 >= 5:
    pressure += 0.3

prob = 50 + (edge * 6 * pressure)
prob = max(25, min(75, prob))

return round(prob), round(100 - prob)

---------------- ALERT SYSTEM ----------------

def check_alert(over, under): if over > 70: return "🔥 STRONG OVER SIGNAL" elif under > 70: return "❄️ STRONG UNDER SIGNAL" return None

---------------- UI ----------------

st.title("🔥 PRO SPORTS AI DASHBOARD")

mode = st.sidebar.selectbox("Select Sport", ["Basketball", "Tennis"])

---------------- BASKETBALL ----------------

if mode == "Basketball": st.subheader("🏀 LIVE GAMES")

games = get_live_games()

if not games:
    st.warning("No live data — check API key")
else:
    options = [f"{i} - {g['teams'][0]} vs {g['teams'][1]}" for i, g in enumerate(games)]
    selected = st.selectbox("Select Game", options)

    idx = int(selected.split(" - ")[0])
    game = games[idx]

    total = sum(game["score"].values())
    over, under = basketball_model(total, game["line"], game["time_left"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total", total)
    col2.metric("OVER %", f"{over}%")
    col3.metric("UNDER %", f"{under}%")

    # Alert
    alert = check_alert(over, under)
    if alert:
        st.error(alert)

    # Graph
    st.subheader("📈 Prediction Trend")
    df = pd.DataFrame({
        "Step": list(range(1, 6)),
        "Over %": [over - 5, over - 3, over, over + 2, over + 3]
    })
    st.line_chart(df.set_index("Step"))

    # BEST BET
    st.subheader("🎯 BEST BET")
    if over > 65:
        st.success("BET OVER")
    elif under > 65:
        st.error("BET UNDER")
    else:
        st.warning("NO STRONG BET")

---------------- TENNIS ----------------

if mode == "Tennis": st.subheader("🎾 TENNIS AI")

g1 = st.number_input("Player 1 Games", 0, 10, 3)
g2 = st.number_input("Player 2 Games", 0, 10, 2)

p1, p2 = tennis_model(g1, g2)

col1, col2 = st.columns(2)
col1.metric("P1 %", f"{p1}%")
col2.metric("P2 %", f"{p2}%")

if p1 > 65:
    st.success("🔥 Player 1 Strong")
elif p2 > 65:
    st.error("❄️ Player 2 Strong")
else:
    st.warning("⚖️ Balanced")

---------------- AUTO REFRESH ----------------

st.sidebar.markdown("---") auto = st.sidebar.checkbox("Auto Refresh (10s)")

if auto: time.sleep(10) st.rerun()
