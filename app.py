import streamlit as st
import pandas as pd
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
telegram_token = st.sidebar.text_input("
