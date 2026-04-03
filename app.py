import streamlit as st
import time

st.set_page_config(page_title="🏀 Betting Tool Pro", layout="centered")

st.title("🏀 Basketball Quarter Betting Tool PRO")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.header("📊 Enter Betting Details")

odds1 = st.number_input("Bet 1 Odds", min_value=1.01, value=1.20)
odds2 = st.number_input("Bet 2 Odds", min_value=1.01, value=1.25)

stake1 = st.number_input("Stake Bet 1", min_value=1.0, value=100.0)
stake2 = st.number_input("Stake Bet 2", min_value=1.0, value=100.0)

# -----------------------------
# CALCULATE BUTTON
# -----------------------------
if st.button("💰 Calculate Strategy"):
    total_stake = stake1 + stake2

    win1 = odds1 * stake1
    win2 = odds2 * stake2

    profit1 = win1 - total_stake
    profit2 = win2 - total_stake

    st.subheader("📊 Results")
    st.write(f"Total Stake: {total_stake:.2f}")

    st.write(f"➡️ If Bet 1 Wins: {profit1:.2f}")
    st.write(f"➡️ If Bet 2 Wins: {profit2:.2f}")

    if profit1 > 0 and profit2 > 0:
        st.success("🔥 GUARANTEED PROFIT (NO LOSS)")
    elif profit1 > 0 or profit2 > 0:
        st.warning("⚠️ Partial Profit (One side wins)")
    else:
        st.error("❌ Loss on both sides")

# -----------------------------
# SMART STAKE SUGGESTION
# -----------------------------
st.header("🧠 Smart No-Loss Stake Calculator")

base_stake = st.number_input("Base Stake", min_value=1.0, value=100.0)

if st.button("⚖️ Auto Balance Stakes"):
    stake_a = base_stake
    stake_b = (odds1 * stake_a) / odds2

    total = stake_a + stake_b
    win_a = odds1 * stake_a - total
    win_b = odds2 * stake_b - total

    st.subheader("💡 Suggested Stakes")
    st.write(f"Bet 1 Stake: {stake_a:.2f}")
    st.write(f"Bet 2 Stake: {stake_b:.2f}")

    st.write(f"If Bet 1 Wins: {win_a:.2f}")
    st.write(f"If Bet 2 Wins: {win_b:.2f}")

# -----------------------------
# QUARTER TIMER
# -----------------------------
st.header("⏱ Quarter Timer")

minutes = st.selectbox("Select Quarter Duration", [10, 12])

if st.button("▶️ Start Timer"):
    total_seconds = minutes * 60
    timer_placeholder = st.empty()

    for i in range(total_seconds, 0, -1):
        mins = i // 60
        secs = i % 60
        timer_placeholder.markdown(f"### ⏳ {mins:02d}:{secs:02d}")
        time.sleep(1)

    timer_placeholder.markdown("### ✅ Quarter Finished!")

# -----------------------------
# STRATEGY TIPS
# -----------------------------
st.header("📈 Strategy Tips")

st.write("""
✅ Use odds between **1.20 – 1.40**  
✅ Bet on different outcomes (Over/Under, Team A/B)  
✅ Focus on **quarters** (more control)  
✅ Avoid high odds (too risky)  
✅ Use Smart Balance to reduce loss  
""")
