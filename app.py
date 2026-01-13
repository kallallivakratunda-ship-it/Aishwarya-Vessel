import streamlit as st
import pandas as pd

# SYSTEM_IDENTITY: AISHWARYA-PRIME (Lite Version)
st.set_page_config(page_title="Aishwarya-Prime", layout="wide")

# THE DIVINE THEME
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #d4af37; }
    .stButton>button { background-color: #d4af37; color: black; border-radius: 10px; width: 100%; }
    h1, h2, h3 { color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 AISHWARYA-PRIME")

# YOUR SECRET DATA LINK
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-QgGR-BQ4Db1NU07yXWTv8bQc6kt_yq15ItUn7GITNc/export?format=csv"

@st.cache_data(ttl=60)
def load_data(gid):
    try:
        url = f"{SHEET_URL}&gid={gid}"
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# TABS
tab1, tab2, tab3 = st.tabs(["SURGERY", "SIRSI", "SANCTUM"])

with tab1:
    st.header("Surgical Log")
    # Residency_log GID
    df_log = load_data("421132644") 
    st.dataframe(df_log)

with tab2:
    st.header("Sirsi Empire Map")
    # Standard Streamlit Map (No Plotly needed)
    map_data = pd.DataFrame({'lat': [14.6195], 'lon': [74.8441]})
    st.map(map_data, zoom=14)
    st.write("Coordinates: 14.6195° N, 74.8441° E")

with tab3:
    st.header("Inner Sanctum")
    pwd = st.text_input("Mantra Key", type="password")
    if pwd == "samarpan":
        st.success("ACCESS GRANTED")
        df_lab = load_data("1745423854")
        st.dataframe(df_lab)
    else:
        st.info("Locked.")
