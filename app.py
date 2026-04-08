import streamlit as st
import time

st.set_page_config(page_title="V22 Betting Tool", layout="wide")

# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# SETTINGS SIDEBAR
# =========================
st.sidebar.header("⚙️ SETTINGS")

line = st.sidebar.number_input("Default Line", value=160.0)
quarter_minutes = st.sidebar.selectbox("Quarter Duration", [10, 12])
boost = st.sidebar.slider("Manual Boost (%)", -10, 10, 0)

st.sidebar.markdown("----")

st.sidebar.subheader("📊 HISTORY (last 10)")
for h in st.session_state.history[-10:][::-1]:
    st.sidebar.write(h)

# =========================
# MODE SELECT
# =========================
mode = st.selectbox("Select Mode", ["Basketball", "Table Tennis"])

# =========================
# 🏀 BASKETBALL MODE
# =========================
if mode == "Basketball":
    st.title("🏀 Basketball Prediction Tool")

    col1, col2 = st.columns(2)

    with col1:
        team_a = st.text_input("Team A", "A")
        score_a = st.number_input("Score A", 0, 200, 50)

    with col2:
        team_b = st.text_input("Team B", "B")
        score_b = st.number_input("Score B", 0, 200, 48)

    quarter = st.selectbox("Quarter", [1, 2, 3, 4])
    minutes_elapsed = st.slider("Minutes Elapsed", 0.0, float(quarter_minutes), 6.0)

    st.markdown("---")

    # =========================
    # CALCULATION ENGINE
    # =========================

    total_score = score_a + score_b

    if minutes_elapsed == 0:
        st.warning("Enter minutes > 0")
    else:
        elapsed_seconds = minutes_elapsed * 60
        total_seconds_game = quarter_minutes * 60 * 4

        # Pace calculation
        pps = total_score / elapsed_seconds

        # Boost
        pps = pps * (1 + boost / 100)

        # End slowdown (last 2 minutes of Q4)
        if quarter == 4 and (quarter_minutes - minutes_elapsed) <= 2:
            pps *= 0.9

        # Full game prediction
        predicted_total = pps * total_seconds_game

        # Team split
        if total_score > 0:
            ratio_a = score_a / total_score
            ratio_b = score_b / total_score
        else:
            ratio_a = ratio_b = 0.5

        pred_a = predicted_total * ratio_a
        pred_b = predicted_total * ratio_b

        # Quarter prediction
        quarter_seconds_total = quarter_minutes * 60
        pps_quarter = total_score / elapsed_seconds
        predicted_quarter = pps_quarter * quarter_seconds_total

        # Range (more realistic)
        low = predicted_total * 0.97
        high = predicted_total * 1.03

        # Signal
        edge = predicted_total - line

        if edge > 5:
            signal = "🔥 STRONG OVER"
        elif edge > 2:
            signal = "✅ OVER"
        elif edge < -5:
            signal = "❄️ STRONG UNDER"
        elif edge < -2:
            signal = "⬇️ UNDER"
        else:
            signal = "⚖️ NO EDGE"

        # =========================
        # DISPLAY
        # =========================
        st.subheader("📊 Prediction")

        st.write(f"Score: {team_a} {score_a} - {score_b} {team_b}")
        st.write(f"Quarter: Q{quarter} | Time: {minutes_elapsed:.1f} min")

        st.markdown("----")

        st.write(f"🎯 Predicted Total: **{predicted_total:.1f}**")
        st.write(f"📈 Range: {low:.1f} → {high:.1f}")

        st.write(f"🔵 {team_a}: {pred_a:.1f}")
        st.write(f"🔴 {team_b}: {pred_b:.1f}")

        st.write(f"⏱ Quarter Prediction: {predicted_quarter:.1f}")

        st.markdown("----")

        st.write(f"📊 Line: {line}")
        st.write(f"📉 Edge: {edge:.1f}")
        st.write(f"🚀 Signal: {signal}")

        # Minute projection (remaining)
        st.markdown("----")
        st.subheader("⏳ Remaining Minutes Projection")

        remaining_minutes = int(quarter_minutes - minutes_elapsed)

        for m in range(1, remaining_minutes + 1):
            future_total = total_score + (pps * 60 * m)
            st.write(f"Minute +{m}: {future_total:.1f}")

        # Save history
        st.session_state.history.append(
            f"{team_a} vs {team_b} | {signal} | {predicted_total:.1f}"
        )

    # AUTO REFRESH
    time.sleep(2)
    st.rerun()

# =========================
# 🏓 TABLE TENNIS MODE
# =========================
elif mode == "Table Tennis":
    st.title("🏓 Table Tennis Momentum Tool")

    col1, col2 = st.columns(2)

    with col1:
        player_a = st.text_input("Player A", "A")
        score_a = st.number_input("Score A", 0, 20, 6)

    with col2:
        player_b = st.text_input("Player B", "B")
        score_b = st.number_input("Score B", 0, 20, 6)

    st.markdown("---")

    diff = score_a - score_b

    if diff >= 3:
        momentum = f"🔥 {player_a} Strong Control"
    elif diff <= -3:
        momentum = f"🔥 {player_b} Strong Control"
    else:
        momentum = "⚖️ Balanced"

    st.subheader("📊 Analysis")
    st.write(f"Score: {player_a} {score_a} - {score_b} {player_b}")
    st.write(f"Momentum: {momentum}")

    if score_a >= 9 or score_b >= 9:
        st.write("⚠️ End Game Pressure Zone")

    # Save history
    st.session_state.history.append(
        f"{player_a} vs {player_b} | {momentum}"
    )

    # AUTO REFRESH
    time.sleep(2)
    st.rerun()
