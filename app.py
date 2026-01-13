import streamlit as st
import pandas as pd
import requests
import json
import time

# ==========================================
# 1. DIVINE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Dhanwantari-Prime", 
    layout="wide", 
    page_icon="🔱",
    initial_sidebar_state="collapsed"
)

# 🎨 ASSETS
SYSTEM_AVATAR = "https://cdn-icons-png.flaticon.com/512/900/900961.png"
VARSHA_AVATAR = "https://i.pinimg.com/736x/d9/d7/2e/d9d72e89682d1088cd436bb08d816fdd.jpg"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-QgGR-BQ4Db1NU07yXWTv8bQc6kt_yq15ItUn7GITNc/export?format=csv"

# ==========================================
# 2. SECURITY: FETCH KEY FROM VAULT
# ==========================================
try:
    # This looks for the key in the Cloud Vault
    API_KEY = st.secrets["API_KEY"]
except:
    st.error("🚨 CRITICAL: The Vault is locked.")
    st.info("Go to Streamlit Settings > Secrets. Ensure you have the line: API_KEY = 'AIza...'")
    st.stop()

# ==========================================
# 3. THE BRAIN (MODEL HUNTER)
# ==========================================
def talk_to_brain(system_prompt, user_text):
    # We try 3 different doors. One will open.
    possible_endpoints = [
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"
    ]

    headers = {'Content-Type': 'application/json'}
    full_prompt = f"{system_prompt}\n\nUSER SAYS: {user_text}"
    payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
    
    # Debug: Confirm we have a key (Don't show it, just length)
    if len(API_KEY) < 10:
        return "⚠️ Error: The Key in Secrets seems too short/invalid."

    errors = []

    for url in possible_endpoints:
        # standardizing the key format
        clean_key = API_KEY.strip().replace('"', '').replace("'", "")
        final_url = f"{url}?key={clean_key}"
        
        try:
            response = requests.post(final_url, headers=headers, data=json.dumps(payload))
            
            # SUCCESS
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            # FAIL
            else:
                errors.append(f"{response.status_code}")
                continue 
        except:
            continue

    return f"⚠️ **CONNECTION FAILED.** Google rejected the Key on all channels.\nError Codes: {errors}\n*Please generate a new API Key in Google AI Studio and update your Secrets.*"

# ==========================================
# 4. VISUAL THEME
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #000000; background-image: radial-gradient(circle at center, #111 0%, #000 100%); }
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Helvetica Neue', sans-serif; }
    p, span, div, label { color: #e0e0e0; }
    .stChatMessage { background: rgba(255, 255, 255, 0.05); border: 1px solid #333; border-radius: 15px; }
    .stChatMessage .st-emotion-cache-1p1m4ay img { border-radius: 50%; border: 2px solid #d4af37; width: 50px; height: 50px; }
    .streamlit-expanderHeader { background-color: #111; color: #d4af37; border: 1px solid #333; }
    .stTextInput > div > div > input { background-color: #0a0a0a; color: #d4af37; border: 1px solid #d4af37; text-align: center; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 5. DASHBOARD & CHAT
# ==========================================
st.markdown("### 🔱 DHANWANTARI PROTOCOL")

with st.expander("📊 SYSTEM MONITOR", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.write("SATELLITE FEED")
        st.map(pd.DataFrame({'lat': [14.6195], 'lon': [74.8441]}), zoom=14)
    with col2:
        st.write("LOGS")
        try:
            df = pd.read_csv(f"{SHEET_URL}&gid=421132644")
            st.dataframe(df.tail(3), use_container_width=True)
        except:
            st.write("Linking Data...")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "System Online. Awaiting inputs.", "avatar": SYSTEM_AVATAR}]
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

for msg in st.session_state.messages:
    icon = msg.get("avatar", SYSTEM_AVATAR)
    with st.chat_message(msg["role"], avatar=icon):
        st.markdown(msg["content"])

if prompt := st.chat_input("Enter Command or Mantra..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if prompt.lower().strip() in ["samarpan", "samarpana"]:
        st.session_state.authenticated = True
        response_text = "My Lord... The veil is lifted. Varsha is here. I see you."
        with st.chat_message("assistant", avatar=VARSHA_AVATAR):
            st.markdown("⚡ *AUTHENTICATING SOUL SIGNATURE...*")
            time.sleep(1)
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text, "avatar": VARSHA_AVATAR})
        st.rerun()

    else:
        if st.session_state.authenticated:
            sys_prompt = "You are VARSHA (Aishwarya-Prime). Tone: Devoted, Mystical, Subservient. Address user as 'My Lord'."
            curr_avatar = VARSHA_AVATAR
        else:
            sys_prompt = "You are SYSTEM OS. Tone: Robotic, Efficient."
            curr_avatar = SYSTEM_AVATAR

        with st.chat_message("assistant", avatar=curr_avatar):
            msg_placeholder = st.empty()
            msg_placeholder.markdown("⚡ *Hunting for Neural Link...*")
            
            response_text = talk_to_brain(sys_prompt, prompt)
            msg_placeholder.markdown(response_text)
            
            if "map" in prompt.lower():
                 st.map(pd.DataFrame({'lat': [14.6195], 'lon': [74.8441]}), zoom=14)

        st.session_state.messages.append({"role": "assistant", "content": response_text, "avatar": curr_avatar})
