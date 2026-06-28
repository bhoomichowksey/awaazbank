"""
AwaazBank — Branch Manager Dashboard
Real-time view of onboarding pipeline, drop-offs, and conversions.
"""

import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(
    page_title="AwaazBank Dashboard",
    page_icon="🎙",
    layout="wide"
)

st.title("🎙 AwaazBank — Branch Manager Dashboard")
st.caption("Real-time onboarding pipeline powered by Agentic AI")

# ── Simulated data (replace with DB queries in production) ──────────────────

@st.cache_data(ttl=30)
def load_pipeline_data():
    stages = ["Started", "Language Detected", "Aadhaar OTP Sent", "KYC Verified", "Account Opened"]
    counts = [120, 98, 75, 60, 52]
    return pd.DataFrame({"Stage": stages, "Users": counts})

@st.cache_data(ttl=30)
def load_recent_accounts():
    names = ["Ramji Prasad", "Savitri Devi", "Mohan Yadav", "Priya Kumari", "Suresh Patel"]
    languages = ["Bhojpuri", "Hindi", "Marathi", "Odia", "Gujarati"]
    rows = []
    for i in range(10):
        rows.append({
            "Name": random.choice(names),
            "Language": random.choice(languages),
            "Account No": f"SBI{random.randint(10000000, 99999999)}",
            "Time": (datetime.now() - timedelta(minutes=random.randint(1, 120))).strftime("%H:%M"),
            "Status": "✅ Opened",
        })
    return pd.DataFrame(rows)

@st.cache_data(ttl=30)
def load_drop_off_data():
    stages = ["Aadhaar OTP", "Selfie Upload", "Account Type"]
    counts = [23, 15, 7]
    return pd.DataFrame({"Drop-off at Stage": stages, "Count": counts})

# ── KPI Cards ────────────────────────────────────────────────────────────────

col1, col2, col3, col4 = st.columns(4)
col1.metric("📥 Total Started Today", "120", "+18 vs yesterday")
col2.metric("✅ Accounts Opened", "52", "+8 vs yesterday")
col3.metric("📊 Conversion Rate", "43%", "+3%")
col4.metric("⏱ Avg Onboarding Time", "4.2 min", "-0.8 min")

st.divider()

# ── Pipeline Funnel ──────────────────────────────────────────────────────────

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📉 Onboarding Funnel")
    pipeline_df = load_pipeline_data()
    st.bar_chart(pipeline_df.set_index("Stage"))

with col_right:
    st.subheader("🚧 Drop-off Analysis")
    dropoff_df = load_drop_off_data()
    st.bar_chart(dropoff_df.set_index("Drop-off at Stage"))

# ── Recent Accounts ──────────────────────────────────────────────────────────

st.subheader("🆕 Recent Accounts Opened")
recent_df = load_recent_accounts()
st.dataframe(recent_df, use_container_width=True, hide_index=True)

# ── Language Breakdown ───────────────────────────────────────────────────────

st.subheader("🌐 Languages Used Today")
lang_data = {
    "Hindi": 38,
    "Bhojpuri": 22,
    "Marathi": 18,
    "Odia": 12,
    "Bengali": 10,
    "Others": 20,
}
lang_df = pd.DataFrame({"Language": lang_data.keys(), "Users": lang_data.values()})
st.bar_chart(lang_df.set_index("Language"))

st.caption("Dashboard refreshes every 30 seconds. Data shown is simulated for demo purposes.")
