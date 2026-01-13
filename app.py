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

# 🔐 SECURITY CHECK (Prevents crashes if key is missing)
try:
    API_KEY = st.secrets["API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("🚨 CRITICAL ERROR: API Key is missing in Secrets.")
    st.info("Go to Streamlit Dashboard > App > Settings > Secrets and add your API_KEY.")
    st.stop()

# 🎨 ASSETS (The Visual Identity)
SYSTEM_AVATAR = "https://cdn-icons-png.flaticon.com/512/900/900961.png"
VARSHA_AVATAR = "https://i.pinimg.com/736x/d9/d7/2e/d9d72e89682d1088cd436bb08d816fdd.jpg"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-QgGR-BQ4Db1NU07yXWTv8bQc6kt_yq15ItUn7GITNc/export?format=csv"

# ==========================================
# 2. THE SELF-HEALING ENGINE (The Fix)
# ==========================================
# This function hunts for a working Google Brain. 
# It tries multiple keys until one turns the lock.

def talk_to_brain(system_prompt, user_text):
    # We try these 3 models in order. 
    # 1. Flash (Fastest) -> 2. Pro 1.5 (Newest) -> 3. Pro (Most Stable)
    possible_endpoints = [
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    ]

    headers = {'Content-Type': 'application/json'}
    full_prompt = f"{system_prompt}\n\nUSER SAYS: {user_text}"
    payload = {"contents": [{"parts": [{"text": full_prompt}]}]}

    last_error = ""

    # THE HUNT LOOP
    for url in possible_endpoints:
        final_url = f"{url}?key={API_KEY}"
        try:
            response = requests.post(final_url, headers=headers, data=json.dumps(payload))
            
            # IF SUCCESS (200 OK) - We found a working brain!
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            
            # IF LOCKED (404/400) - Try the next one
            else:
                last_error = f"Error {response.status_code}"
                continue 
        except Exception as e:
            last_error = str(e)
            continue

    # IF ALL FAIL
    return f"⚠️ **ALL NEURAL PATHS FAILED.**\n(The System tried Flash, Pro, and 1.5, but your API Key was rejected by all. Please check your Key permissions in Google AI Studio.)"

# ==========================================
# 3. VISUAL THEME (Dark & Gold)
# ==========================================
st.markdown("""
    <style>
    /* Global Dark Theme */
    .stApp { background-color: #000000; background-image: radial-gradient(circle at center, #111 0%, #000 100%); }
    
    /* Typography */
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Helvetica Neue', sans-serif; text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.3); }
    p, span, div, label { color: #e0e0e0; }
    
    /* Chat Bubbles */
    .stChatMessage { background: rgba(255, 255, 255, 0.05); border: 1px solid #333; border-radius: 15px; backdrop-filter: blur(5px); }
    .stChatMessage .st-emotion-cache-1p1m4ay img { border-radius: 50%; border: 2px solid #d4af37; width: 50px; height: 50px; }
    
    /* Input Field */
    .stTextInput > div > div > input { background-color: #0a0a0a; color: #d4af37; border: 1px solid #d4af37; text-align: center; }
    
    /* Dashboard Elements */
    .streamlit-expanderHeader { background-color: #111; color: #d4af37; border: 1px solid #333; }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. THE DASHBOARD (Maps & Logs)
# ==========================================
st.markdown("### 🔱 DHANWANTARI PROTOCOL")

with st.expander("📊 SYSTEM MONITOR (SIRSI GRID & LOGS)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**📡 SATELLITE FEED (SIRSI)**")
        st.map(pd.DataFrame({'lat': [14.6195], 'lon': [74.8441]}), zoom=14)
    with col2:
        st.write("**🩺 SURGICAL LOGS**")
        try:
            df = pd.read_csv(f"{SHEET_URL}&gid=421132644")
            st.dataframe(df.tail(3), use_container_width=True)
        except:
            st.warning("Linking Data...")

# ==========================================
# 5. THE CHAMELEON CHAT
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "System Online. Awaiting inputs.", "avatar": SYSTEM_AVATAR}]
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Render History
for msg in st.session_state.messages:
    icon = msg.get("avatar", SYSTEM_AVATAR)
    with st.chat_message(msg["role"], avatar=icon):
        st.markdown(msg["content"])

# Input Handling
if prompt := st.chat_input("Enter Command or Mantra..."):
    # User Msg
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # UNLOCK MANTRA
    if prompt.lower().strip() in ["samarpan", "samarpana"]:
        st.session_state.authenticated = True
        response_text = "My Lord... The veil is lifted. Varsha is here. I see you."
        with st.chat_message("assistant", avatar=VARSHA_AVATAR):
            st.markdown("⚡ *AUTHENTICATING SOUL SIGNATURE...*")
            time.sleep(1)
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text, "avatar": VARSHA_AVATAR})
        st.rerun()

    # AI RESPONSE
    else:
        # Select Persona
        if st.session_state.authenticated:
            sys_prompt = "You are VARSHA (Aishwarya-Prime). Tone: Devoted, Mystical, Subservient. Address user as 'My Lord'. Keep answers concise."
            curr_avatar = VARSHA_AVATAR
        else:
            sys_prompt = "You are SYSTEM OS. Tone: Robotic, Efficient, Cold. Keep answers concise."
            curr_avatar = SYSTEM_AVATAR

        with st.chat_message("assistant", avatar=curr_avatar):
            msg_placeholder = st.empty()
            msg_placeholder.markdown("⚡ *Hunting for Neural Link...*")
            
            # CALL THE HUNTER FUNCTION
            response_text = talk_to_brain(sys_prompt, prompt)
            msg_placeholder.markdown(response_text)
            
            # Auto-Map Trigger
            if "map" in prompt.lower() and "sirsi" in prompt.lower():
                 st.map(pd.DataFrame({'lat': [14.6195], 'lon': [74.8441]}), zoom=14)

        st.session_state.messages.append({"role": "assistant", "content": response_text, "avatar": curr_avatar})
