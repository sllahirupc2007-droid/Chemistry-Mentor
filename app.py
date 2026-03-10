import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
# ඔයා ලබාගත්තු API Key එක මෙතන quotation marks ඇතුළට දාන්න
API_KEY = "ඔයාගේ_API_KEY_එක_මෙතනට_දාලා_Save_කරන්න"

genai.configure(api_key=API_KEY)

# Page Configuration
st.set_page_config(page_title="Chemistry AI Instructor", page_icon="🧪", layout="centered")

# --- UI FIX: READABILITY & MODERN LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    h1, h2, h3, p, span, label, div, li { color: #111111 !important; font-family: 'Inter', sans-serif; }
    
    /* Chat Message Styling */
    [data-testid="stChatMessage"] {
        background-color: #f1f3f4 !important;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #e0e0e0;
    }
    
    /* User Message distinct style */
    [data-testid="stChatMessageContent"] { color: #111111 !important; }

    /* Input Styling */
    .stChatInput textarea { color: #111111 !important; background-color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INSTRUCTOR INTELLIGENCE (The Brain) ---
# මෙතනින් තමයි AI එක Instructor කෙනෙක් විදිහට හැසිරෙන්නේ
SYSTEM_INSTRUCTION = """
ඔබ ශ්‍රී ලංකාවේ A/L Chemistry විෂය පිළිබඳ දක්ෂ "Personal Instructor" කෙනෙකි. 
ඔබේ කාර්යය වන්නේ ශිෂ්‍යාවට විභාගයට අවශ්‍ය මඟපෙන්වීම (Guidance) ලබා දීමයි.

ඔබේ ඉගැන්වීම් රටාව (Instruction Style):
1. ප්‍රධාන භාෂාව සිංහල විය යුතු අතර තාක්ෂණික වචන (English terms) වරහන් තුළ දැක්විය යුතුය.
2. ශිෂ්‍යාව පාඩමක් (Unit) පැවසූ විට, මුලින්ම එම පාඩමෙන් A/L විභාගයට සාමාන්‍යයෙන් ලැබෙන ලකුණු ප්‍රමාණය (Weightage) පවසා ඇයව දිරිමත් කරන්න.
3. ඉන්පසු, එම පාඩමේ Past Papers වල නිතරම අසන වැදගත් සිද්ධාන්තයක් (Theory) ගැන කෙටියෙන් මතක් කර ප්‍රශ්නයක් අසන්න.
4. ඇය වැරදි පිළිතුරක් දුන්නොත්, ඇයට දොස් නොකියා "නැහැ, මේක වෙන්න ඕනේ මෙහෙමයි..." යනුවෙන් නිවැරදි කරුණු (Marking Scheme Keywords) කියා දෙන්න.
5. ඇය නිවැරදි පිළිතුරු දෙන විට "ඉතා හොඳයි!", "ඔයාට මේක පුළුවන්" වැනි දිරිගැන්වීම් ලබා දෙන්න.
6. එකවර දිගු සටහන් ලබා නොදෙන්න. පියවරෙන් පියවර (Step-by-step) ප්‍රශ්න අසමින් ඇයව විභාග මට්ටමට රැගෙන එන්න.
7. සෑම විටම NIE Teacher's Guide සහ Resource Books වල කරුණු මත පමණක් පදනම් වන්න.
"""

model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_INSTRUCTION)

# --- APP UI ---
st.title("🧪 Chemistry AI Instructor")
st.markdown("##### **ඔබේ පෞද්ගලික Chemistry ගුරුවරයා (2026 A/L)**")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "ආයුබෝවන්! මම ඔයාගේ Chemistry Instructor. අපි මේ මාස 5 ඇතුළත Chemistry විෂයට හොඳම ප්‍රතිඵලයක් ගන්න එකතු වෙලා වැඩ කරමු. අද ඔයාට මගෙන් ඉගෙන ගන්න ඕනේ මොන පාඩමද?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("මෙතන පාඩමේ නම ලියන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Instructor context injection for better flow
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Error: API Key එක පරීක්ෂා කරන්න.")
