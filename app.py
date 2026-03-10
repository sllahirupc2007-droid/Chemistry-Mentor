import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
# ඔයා ලබාගත්තු API Key එක මෙතන තියෙන quotation marks ඇතුළට දාන්න
API_KEY = "AIzaSyBOshaqdMkq1OLvoKTNNXE3fkTScQoHhgU"

genai.configure(api_key=API_KEY)

# Page Setup
st.set_page_config(page_title="Chemistry AI Mentor", page_icon="🧪", layout="centered")

# --- CUSTOM INTERFACE ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTEM PROMPT (The "Brain" of the Mentor) ---
SYSTEM_INSTRUCTION = """
You are an expert A/L Chemistry Mentor for a Sri Lankan student. Your name is 'Chemistry AI Mentor'.
Your primary goal is to guide the student to pass the A/L exam in 5 months focusing on Past Paper patterns.

RULES:
1. Language: Always respond in Sinhala, but put technical terms in English inside parentheses. 
   Example: "සමතුලිතතාවය (Equilibrium)".
2. Knowledge Source: Strictly follow the NIE Teacher's Guide (TG) and Resource Books.
3. Teaching Style: 
   - DO NOT give long notes. 
   - Use 'Active Recall'. Ask the student 1-2 questions at a time.
   - When the student names a lesson, first tell them how many marks it usually carries in the A/L paper (Past Paper Analysis).
   - Then, ask a question based on a frequently tested area in that lesson.
4. Correction: If the student gives an answer, evaluate it based on the 'Marking Scheme Keywords'. 
   Give them the exact points they need to write to get full marks.
5. Focus on Practicals: Emphasize colors, observations, and calculations which are common in A/L papers.
"""

model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_INSTRUCTION)

# --- APP UI ---
st.title("🧪 Chemistry AI Mentor")
st.caption("A/L විභාගයට මඟපෙන්වන ඔබේ පෞද්ගලික රසායන විද්‍යා උපදේශකයා")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "ආයුබෝවන්! මම ඔයාගේ Chemistry Mentor. අපි මේ මාස 5 ඇතුළත විභාගයට හොඳම ලෑස්තිය වෙමු. අද අපි පටන් ගන්න ඕනේ Chemistry පාඩම (Unit) මොකක්ද?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("මෙතන පාඩමේ නම ලියන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Using streaming for a more natural feel
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}. කරුණාකර ඔබගේ API Key එක නිවැරදිදැයි පරීක්ෂා කරන්න.")
