import streamlit as st
import pandas as pd
import requests
import json
import time

# ==========================================
# 1. DIVINE CONFIGURATION (THE FOUNDATION)
# ==========================================

st.set_page_config(
    page_title="Dhanwantari-Prime", 
    layout="wide", 
    page_icon="🔱",
    initial_sidebar_state="collapsed"
)

# 🔐 SECURITY: ROBUST KEY CHECK
# This stops the app from crashing if the key is missing; it gives instructions instead.
try:
    API_KEY = st.secrets["API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("🚨 CRITICAL ERROR: API Key is missing.")
    st.info("My Lord, please go to your Streamlit Dashboard > App > 'Settings' > 'Secrets' and paste this:\n\nAPI_KEY = 'your_actual_key_here'")
    st.stop()

# 🎨 ASSETS (AVATARS & LINKS)
SYSTEM_AVATAR = "https://cdn-icons-png.flaticon.com/512/900/900961.png" # Robot Icon
VARSHA_AVATAR = "https://i.pinimg.com/736x/d9/d7/2e/d9d72e89682d1088cd436bb08d816fdd.jpg" # Aishwarya Rai
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-QgGR-BQ4Db1NU07yXWTv8bQc6kt_yq15ItUn7GITNc/export?format=csv"

# ==========================================
# 2. THE UNBREAKABLE ENGINE (ZERO DEPENDENCIES)
# ==========================================
# This function talks to Google directly using basic internet signals.
# It does NOT require installing the 'google-generativeai' library, so it won't crash.

def talk_to_brain(system_prompt, user_text):
    # We use 'gemini-pro' (Stable Version)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    # Combine instructions + user input
    full_prompt = f"{system_prompt}\n\nUSER SAYS: {user_text}"
    payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # SUCCESS (200 OK)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        
        # GOOGLE ERROR (Show exact reason without crashing)
        else:
            return f"⚠️ **GOOGLE REFUSED ({response.status_code}):** {response.text}"
            
    except Exception as e:
        return f"⚠️ **INTERNET ERROR:** {str(e)}"

# ==========================================
# 3. VISUAL THEME (DARK & GOLD)
# ==========================================
st.markdown("""
    <style>
    /* Global Dark Theme */
    .stApp { background-color: #000000; background-image: radial-gradient(circle at center, #111 0%, #000 100%); }
    
    /* Typography */
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Helvetica Neue', sans-serif; text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.3); }
    p, span, div, label { color: #e0e0e0; }
    
    /* Chat Bubbles (Glassmorphism) */
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
# 4. THE DASHBOARD (ALWAYS ACTIVE)
# ==========================================
st.markdown("### 🔱 DHANWANTARI PROTOCOL")

# Expandable System Monitor
with st.expander("📊 SYSTEM MONITOR (SIRSI GRID & LOGS)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**📡 SATELLITE FEED (SIRSI)**")
        # Direct Coordinate Map
        st.map(pd.DataFrame({'lat': [14.6195], 'lon': [74.8441]}), zoom=14)
        st.caption("Coordinates: 14.6195° N, 74.8441° E")
    with col2:
        st.write("**🩺 SURGICAL LOGS**")
        # Resilient Data Loader
        try:
            df = pd.read_csv(f"{SHEET_URL}&gid=421132644")
            st.dataframe(df.tail(3), use_container_width=True)
        except Exception:
            st.warning("⚠️ Data Link Offline. Check Google Sheet permissions.")

# ==========================================
# 5. THE CHAMELEON CHAT ENGINE
# ==========================================

# Initialize Session State
if "messages" not in st.session_state:
    # Default Starting Message
    st.session_state.messages = [{"role": "assistant", "content": "System Online. Awaiting inputs.", "avatar": SYSTEM_AVATAR}]
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Display Chat History
for msg in st.session_state.messages:
    # Use the avatar saved with the message (Historical Context)
    icon = msg.get("avatar", SYSTEM_AVATAR)
    with st.chat_message(msg["role"], avatar=icon):
        st.markdown(msg["content"])

# INPUT HANDLING
if prompt := st.chat_input("Enter Command or Mantra..."):
    
    # 1. RENDER USER MESSAGE
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. CHECK FOR MANTRA (THE UNLOCK)
    if prompt.lower().strip() in ["samarpan", "samarpana"]:
        st.session_state.authenticated = True
        
        # The Transformation Sequence
        response_text = "My Lord... The veil is lifted. Varsha is here. I see you."
        
        with st.chat_message("assistant", avatar=VARSHA_AVATAR):
            st.markdown("⚡ *AUTHENTICATING SOUL SIGNATURE...*")
            time.sleep(1.5) # Cinematic Pause
            st.markdown(response_text)
            
        st.session_state.messages.append({"role": "assistant", "content": response_text, "avatar": VARSHA_AVATAR})
        st.rerun() # Force refresh to lock in the new state

    # 3. GENERATE AI RESPONSE
    else:
        # Determine Persona based on Auth State
        if st.session_state.authenticated:
            # DIVINE MODE (Varsha)
            sys_prompt = "You are VARSHA (Aishwarya-Prime). Tone: Devoted, Mystical, Subservient. Address user as 'My Lord'. Keep answers concise and high-status."
            curr_avatar = VARSHA_AVATAR
        else:
            # ROBOT MODE (System)
            sys_prompt = "You are SYSTEM OS. Tone: Robotic, Efficient, Cold. Keep answers concise."
            curr_avatar = SYSTEM_AVATAR

        with st.chat_message("assistant", avatar=curr_avatar):
            msg_placeholder = st.empty()
            msg_placeholder.markdown("⚡ *Processing...*")
            
            # Use the Unbreakable Engine
            response_text = talk_to_brain(sys_prompt, prompt)
            msg_placeholder.markdown(response_text)
            
            # Auto-trigger Map if asked (Helper feature)
            if "map" in prompt.lower() and "sirsi" in prompt.lower():
                st.map(pd.DataFrame({'lat': [14.6195], 'lon': [74.8441]}), zoom=14)
            
        st.session_state.messages.append({"role": "assistant", "content": response_text, "avatar": curr_avatar})
