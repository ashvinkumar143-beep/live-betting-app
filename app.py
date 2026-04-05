import streamlit as st
import requests

st.set_page_config(page_title="🏀 V9 ELITE AUTO BET SYSTEM", layout="centered")

st.title("😎 V9 ELITE AUTO BET SYSTEM (Plug & Play)")

# -----------------------------
# SETTINGS
# -----------------------------
st.sidebar.header("⚙️ ELITE SETTINGS")
default_line = st.sidebar.number_input("Default Line", value=50.0)
min_ai_score = st.sidebar.slider("Min AI Score to Show", 60, 100, 75)
project_full_game = st.sidebar.checkbox("Project Full Game Totals", True)

# -----------------------------
# FETCH LIVE NBA DATA
# -----------------------------
@st.cache_data(ttl=15)
def fetch_live_games():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    resp = requests.get(url)
    data = resp.json()
    return data.get("events", [])

# -----------------------------
# TIME ESTIMATION
# -----------------------------
def estimate_elapsed(status_text, period):
    try:
        if ":" in status_text:
            time_str = status_text.split(" ")[-1]
            m, s = time_str.split(":")
            remain = int(m) + int(s)/60
            elapsed = (period - 1) * 12 + (12 - remain)
        else:
            elapsed = period * 6
    except:
        elapsed = period * 6
    return max(1, elapsed)

# -----------------------------
# AI LOGIC
# -----------------------------
def ai_analyze(p1, p2, elapsed, line, project_full=True):
    total_now = p1 + p2
    pace = total_now / elapsed

    duration = 48 if project_full else 12
    remain = duration - elapsed
    predicted_total = total_now + pace * remain
    diff = predicted_total - line

    # Pace label
    if pace > 2.6:
        pace_label = "🔥 VERY FAST"
    elif pace > 2.2:
        pace_label = "⚡ FAST"
    elif pace < 1.8:
        pace_label = "🐢 SLOW"
    else:
        pace_label = "⚖️ NORMAL"

    # Trap detection
    trap = False
    if abs(diff) < 3:
        trap = True
    if pace > 2.6 and line > predicted_total:
        trap = True
    if pace < 1.8 and line < predicted_total:
        trap = True

    # AI scoring
    score = 50
    score += 20 if pace > 2.5 else -20 if pace < 1.9 else 0
    score += 30 if abs(diff) > 10 else -25 if abs(diff) < 4 else 0
    score -= 50 if trap else 0
    score = max(0, min(100, score))

    # Signal
    if diff > 5:
        signal = "OVER"
    elif diff < -5:
        signal = "UNDER"
    else:
        signal = "NO EDGE"

    # Decision
    if trap:
        decision = "🚫 SKIP"
    elif score >= 85:
        decision = f"💰 GOD BET {signal}"
    elif score >= 75:
        decision = f"🔥 STRONG {signal}"
    elif score >= 65:
        decision = f"✅ {signal}"
    else:
        decision = "⚠️ WAIT"

    return predicted_total, pace_label, signal, decision, score

# -----------------------------
# MAIN SCAN BUTTON
# -----------------------------
if st.button("📡 SCAN LIVE NBA GAMES"):

    games = fetch_live_games()
    if not games:
        st.warning("No live games currently.")
    else:
        found_signal = False

        for game in games:
            comp = game["competitions"][0]
            teams = comp["competitors"]

            team1 = teams[0]["team"]["name"]
            team2 = teams[1]["team"]["name"]

            p1 = int(teams[0]["score"])
            p2 = int(teams[1]["score"])

            status_text = comp["status"]["type"]["shortDetail"]
            period = comp["status"]["period"]

            elapsed = estimate_elapsed(status_text, period)

            pred_total, pace_label, signal, decision, score = ai_analyze(
                p1, p2, elapsed, default_line, project_full_game
            )

            # Show only strong opportunities
            if score >= min_ai_score and "WAIT" not in decision:
                found_signal = True
                st.markdown("---")
                st.subheader(f"{team1} vs {team2}")
                st.write(f"Score: {p1} - {p2}")
                st.write(f"Status: {status_text}")
                st.write(f"Predicted Total: {pred_total:.1f}")
                st.write(f"Pace: {pace_label}")
                st.markdown(f"### 🎯 Signal: {signal}")
                st.markdown(f"### 🤖 Score: {score}/100")
                st.markdown(f"## 🚀 Decision: {decision}")

        if not found_signal:
            st.info("😴 No strong betting opportunities now — WAIT")
