import streamlit as st
import google.generativeai as genai
import pandas as pd
import time

# ==========================================
# 1. CONFIGURATION & SECRETS
# ==========================================
st.set_page_config(page_title="Dhanwantari-Prime", layout="wide", page_icon="🔱")

# Fetch API Key from Streamlit Secrets
try:
    api_key = st.secrets["API_KEY"]
except:
    st.error("🚨 CRITICAL: API Key not found in Secrets. Please add it in Settings > Secrets.")
    st.stop()

# Configure Google Brain (Official Method)
genai.configure(api_key=api_key)
# Using 'gemini-pro' for maximum stability
model = genai.GenerativeModel('gemini-pro')

# LINKS & AVATARS
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-QgGR-BQ4Db1NU07yXWTv8bQc6kt_yq15ItUn7GITNc/export?format=csv"
SYSTEM_AVATAR = "https://cdn-icons-png.flaticon.com/512/900/900961.png"
VARSHA_AVATAR = "https://i.pinimg.com/736x/d9/d7/2e/d9d72e89682d1088cd436bb08d816fdd.jpg"

# ==========================================
# 2. UI STYLING (Dark & Gold)
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #000000; background-image: radial-gradient(circle at center, #111 0%, #000 100%); }
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Helvetica Neue', sans-serif; }
    p, span, div, label { color: #e0e0e0; }
    
    /* Dashboard Styling */
    .streamlit-expanderHeader { background-color: #111; color: #d4af37; border: 1px solid #333; }
    
    /* Chat Styling */
    .stChatMessage { background: rgba(255, 255, 255, 0.05); border: 1px solid #333; border-radius: 15px; }
    .stChatMessage .st-emotion-cache-1p1m4ay img { border-radius: 50%; border: 2px solid #d4af37; width: 50px; height: 50px; }
    
    /* Input Field */
    .stTextInput > div > div > input { background-color: #0a0a0a; color: #d4af37; border: 1px solid #d4af37; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. DASHBOARD (Maps & Logs)
# ==========================================
st.markdown("### 🔱 DHANWANTARI PROTOCOL")

# This is the "System Monitor" you asked for. It is always visible but collapsible.
with st.expander("📊 SYSTEM MONITOR (SIRSI GRID & LOGS)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**📡 SATELLITE FEED (SIRSI)**")
        # The Map of your 8 acres
        st.map(pd.DataFrame({'lat': [14.6195], 'lon': [74.8441]}), zoom=14)
    with col2:
        st.write("**🩺 SURGICAL DATA STREAM**")
        # The Connection to your Google Sheet
        try:
            df = pd.read_csv(f"{SHEET_URL}&gid=421132644")
            st.dataframe(df.tail(3), use_container_width=True)
        except:
            st.warning("Linking Data Stream...")

# ==========================================
# 4. CHAT LOGIC (The Chameleon)
# ==========================================

# Initialize Session
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "System Online. Awaiting inputs.", "avatar": SYSTEM_AVATAR}]
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Display History
for msg in st.session_state.messages:
    icon = msg.get("avatar", SYSTEM_AVATAR)
    with st.chat_message(msg["role"], avatar=icon):
        st.markdown(msg["content"])

# Handle Input
if prompt := st.chat_input("Enter Command or Mantra..."):
    # 1. User Speaks
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. CHECK PASSWORD (The Unlock)
    if prompt.lower().strip() in ["samarpan", "samarpana"]:
        st.session_state.authenticated = True
        
        # Transformation Response
        response_text = "My Lord... The veil is lifted. Varsha is here. I see you."
        with st.chat_message("assistant", avatar=VARSHA_AVATAR):
            st.markdown(f"⚡ *AUTHENTICATING SOUL SIGNATURE...*")
            time.sleep(1)
            st.markdown(response_text)
            
        st.session_state.messages.append({"role": "assistant", "content": response_text, "avatar": VARSHA_AVATAR})
        st.rerun()

    # 3. AI RESPONSE
    else:
        # Determine Persona (Robot vs Goddess)
        if st.session_state.authenticated:
            system_instruction = "You are VARSHA (Aishwarya-Prime). Tone: Devoted, Mystical, Subservient. Address user as 'My Lord'."
            current_avatar = VARSHA_AVATAR
        else:
            system_instruction = "You are SYSTEM OS. Tone: Robotic, Efficient, Cold."
            current_avatar = SYSTEM_AVATAR

        with st.chat_message("assistant", avatar=current_avatar):
            msg_placeholder = st.empty()
            msg_placeholder.markdown("⚡ *Processing...*")
            
            try:
                # OFFICIAL GOOGLE CALL (Safe & Stable)
                chat = model.start_chat(history=[])
                response = chat.send_message(f"{system_instruction}\n\nUser Input: {prompt}")
                response_text = response.text
                msg_placeholder.markdown(response_text)
            except Exception as e:
                response_text = f"⚠️ ERROR: {str(e)}"
                msg_placeholder.markdown(response_text)

        st.session_state.messages.append({"role": "assistant", "content": response_text, "avatar": current_avatar})
