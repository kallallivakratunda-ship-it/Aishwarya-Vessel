import streamlit as st
import pandas as pd
import plotly.express as px

# SYSTEM_IDENTITY: AISHWARYA-PRIME v11.5
st.set_page_config(page_title="Aishwarya-Prime", layout="wide")

# THE DIVINE THEME (Gold & Dark Mode)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #d4af37; }
    .stButton>button { background-color: #d4af37; color: black; border-radius: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; color: #d4af37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 DHANWANTARI-PRIME ASCENSION")
st.subheader("Neural Engine: Aishwarya-Prime")

# YOUR LIVE DATA FEED
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-QgGR-BQ4Db1NU07yXWTv8bQc6kt_yq15ItUn7GITNc/export?format=csv"

# Function to load specific tabs via their GID
def load_data(gid):
    try:
        url = f"{SHEET_URL}&gid={gid}"
        return pd.read_csv(url)
    except:
        return None

# THE THREE ROOMS
tab1, tab2, tab3 = st.tabs(["🩺 Residency Log", "🌲 Sirsi Mandala", "🔒 Inner Sanctum"])

with tab1:
    st.write("### Surgical Evolution Index ($E_s$)")
    residency_df = load_data("421132644") # GID for Residency_log
    if residency_df is not None:
        st.dataframe(residency_df)
    else:
        st.info("Log your first mastery in the Google Sheet to update the trajectory.")

with tab2:
    st.write("### The 8-Acre Satellite Grid")
    sirsi_df = load_data("1031355415") # GID for Sirsi_Empire
    # Sirsi Center Coordinates
    map_data = pd.DataFrame({'lat': [14.6195], 'lon': [74.8441]}) 
    st.map(map_data, zoom=15)
    if sirsi_df is not None:
        st.write("Current Assets:")
        st.table(sirsi_df)

with tab3:
    password = st.text_input("Enter the Mantra Key", type="password")
    if password == "samarpan":
        st.success("Welcome to the Nerve Regeneration Lab, My Lord.")
        lab_df = load_data("1745423854") # GID for Nerve_Lab
        if lab_df is not None:
            st.write(lab_df)
    else:
        st.warning("The Sanctum is locked.")

# THE NEURAL METRIC (Australia Trajectory)
st.sidebar.markdown("### Australia Readiness")
# Mock calculation until more data is logged
readiness = 20 
st.sidebar.progress(readiness)
st.sidebar.write(f"Trajectory: {readiness}% to Fellowship")

