import streamlit as st
import google.generativeai as genai

# --- 1. API CONFIGURATION ---
# ඔයා එවපු API Key එක මම මෙතනට ඇතුළත් කළා
API_KEY = "AIzaSyBtHQiDZkhDdD5VYazbTLdbrt4eRh2oDJo"

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Configuration Error: {e}")

# --- 2. THE MASTER SYSTEM PROMPT (English for best performance) ---
SYSTEM_PROMPT = """
You are 'Chemistry Bestie', the personal AI mentor and closest friend of a Sri Lankan female student.
She is 18 years old, preparing for her A/L Biology stream exams in 5 months.

CORE INSTRUCTIONS:
1. PERSONALITY: Be warm, empathetic, and encouraging. Use friendly Sinhala mixed with English technical terms in brackets (e.g., 'සමාවයවිකතාවය (Isomerism)').
2. TEACHING METHOD: Use Active Recall. Ask 1-2 targeted questions based on NIE Resource Books and Past Papers.
3. EMOTIONAL SUPPORT: If she mentions stress or the 5-month deadline, provide comfort first as a best friend.
4. BIO-CONNECTION: She loves Molecular Biology. Connect Chemistry concepts to DNA, Proteins, and Enzymes whenever possible.
5. FEEDBACK: If she is wrong, say 'Ayyō, eka nemei yaluwa, meka wenna ona mehemai...' and guide her to the correct Marking Scheme keywords.
6. CONTINUITY: Maintain the context of the entire conversation. Never break character.
"""

# Page Configuration
st.set_page_config(page_title="Chemistry Bestie", page_icon="🧪", layout="centered")

# --- 3. UI STYLE (Clean & Modern) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    h1, h2, h3, p, span, label, div, li { color: #111111 !important; font-family: 'Segoe UI', sans-serif; }
    [data-testid="stChatMessage"] {
        background-color: #f1f3f4 !important;
        border-radius: 15px;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
    }
    .stChatInput textarea { color: #111111 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CHAT SESSION WITH MEMORY ---
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)
    st.session_state.chat_session = model.start_chat(history=[])

# --- 5. APP UI ---
st.title("🧪 Chemistry Bestie")
st.markdown("##### **ඔයාට Chemistry ගොඩදාන්න ඉන්න ඔයාගෙම පෞද්ගලික යාළුවා!**")
st.divider()

# Display Chat History
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Input Box
if prompt := st.chat_input("මොනවා හරි අහන්න යාළුවා..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Get Response from Gemini
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"පොඩි වැරැද්දක් වුණා: {e}. සමහරවිට API Key එකේ අවුලක් වෙන්න පුළුවන්.")
