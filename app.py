import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3
import threading
import base64
import time
from streamlit_mic_recorder import mic_recorder

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(page_title="Scorpion AI - Talking Humanoid", layout="wide")

# ----------------------------------------------------------------------
# Authentication
# ----------------------------------------------------------------------
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["authenticated"] = True
            del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.text_input("🔐 Enter password to unlock Scorpion AI", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["authenticated"]:
        st.text_input("🔐 Enter password to unlock Scorpion AI", type="password", on_change=password_entered, key="password")
        st.error("Wrong password. Access denied.")
        return False
    else:
        return True

# ----------------------------------------------------------------------
# OpenAI setup (only used if demo mode is off)
# ----------------------------------------------------------------------
def get_ai_response(prompt, language):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are Scorpion, a helpful AI assistant. You speak {language}. Respond concisely and clearly."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# ----------------------------------------------------------------------
# Avatar with lip movement (SVG)
# ----------------------------------------------------------------------
svg_closed = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <rect width="400" height="400" fill="url(#haitiGradient)" rx="20"/>
  <defs>
    <linearGradient id="haitiGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#00209F;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#00209F;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#D21034;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#D21034;stop-opacity:1" />
    </linearGradient>
  </defs>
  <image href="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Coat_of_arms_of_Haiti.svg/320px-Coat_of_arms_of_Haiti.svg.png" x="100" y="20" width="200" opacity="0.3"/>
  <circle cx="200" cy="200" r="120" fill="#F5CBA7" stroke="gold" stroke-width="4"/>
  <circle cx="150" cy="170" r="15" fill="white"/>
  <circle cx="250" cy="170" r="15" fill="white"/>
  <circle cx="155" cy="170" r="7" fill="black"/>
  <circle cx="245" cy="170" r="7" fill="black"/>
  <line x1="130" y1="145" x2="170" y2="140" stroke="black" stroke-width="5" stroke-linecap="round"/>
  <line x1="270" y1="145" x2="230" y2="140" stroke="black" stroke-width="5" stroke-linecap="round"/>
  <path d="M190 190 L200 205 L210 190" stroke="#A0522D" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M160 240 Q200 260 240 240" stroke="#A0522D" stroke-width="6" fill="none" stroke-linecap="round"/>
  <text x="200" y="100" font-family="Arial" font-size="24" font-weight="bold" fill="gold" text-anchor="middle">♏️ SCORPION ♏️</text>
</svg>'''

svg_open = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <rect width="400" height="400" fill="url(#haitiGradient)" rx="20"/>
  <defs>
    <linearGradient id="haitiGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#00209F;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#00209F;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#D21034;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#D21034;stop-opacity:1" />
    </linearGradient>
  </defs>
  <image href="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Coat_of_arms_of_Haiti.svg/320px-Coat_of_arms_of_Haiti.svg.png" x="100" y="20" width="200" opacity="0.3"/>
  <circle cx="200" cy="200" r="120" fill="#F5CBA7" stroke="gold" stroke-width="4"/>
  <circle cx="150" cy="170" r="15" fill="white"/>
  <circle cx="250" cy="170" r="15" fill="white"/>
  <circle cx="155" cy="170" r="7" fill="black"/>
  <circle cx="245" cy="170" r="7" fill="black"/>
  <line x1="130" y1="145" x2="170" y2="140" stroke="black" stroke-width="5" stroke-linecap="round"/>
  <line x1="270" y1="145" x2="230" y2="140" stroke="black" stroke-width="5" stroke-linecap="round"/>
  <path d="M190 190 L200 205 L210 190" stroke="#A0522D" stroke-width="4" fill="none" stroke-linecap="round"/>
  <ellipse cx="200" cy="250" rx="40" ry="25" fill="#A0522D"/>
  <ellipse cx="200" cy="245" rx="30" ry="15" fill="#8B4513"/>
  <ellipse cx="200" cy="243" rx="20" ry="10" fill="#4A2A1A"/>
  <text x="200" y="100" font-family="Arial" font-size="24" font-weight="bold" fill="gold" text-anchor="middle">♏️ SCORPION ♏️</text>
</svg>'''

def get_avatar_data_uri(svg):
    b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{b64}"

closed_uri = get_avatar_data_uri(svg_closed)
open_uri = get_avatar_data_uri(svg_open)

# ----------------------------------------------------------------------
# Text-to-Speech (TTS) using pyttsx3 (male voice)
# ----------------------------------------------------------------------
def speak_text(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'male' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

# ----------------------------------------------------------------------
# Demo questions and answers
# ----------------------------------------------------------------------
demo_qa = [
    ("What is GlobalInternet.py?", "GlobalInternet.py is a software company based in Haiti, founded by Gesner Deslandes. We build custom web applications, AI tools, and database systems for businesses, governments, and individuals."),
    ("Who is Gesner Deslandes?", "Gesner Deslandes is the owner and lead Python developer of GlobalInternet.py. He is a self-taught developer who uses AI to build applications faster, focusing on architecture and user experience."),
    ("What services do you offer?", "We offer full‑stack web app development, AI‑powered tools, database systems, accounting software, loan management systems, and custom solutions. All applications are deployed on Streamlit Cloud and delivered within 24 hours."),
    ("Can you build custom software for my business?", "Absolutely. We listen to your needs, design the architecture, build the app, test it, and deploy it. You get a working product within days, not months."),
    ("What is the cost of your services?", "Each application is priced individually based on complexity. Our accounting software, for example, is $149 one‑time. For custom work, we provide a quote after understanding your requirements."),
    ("Do you work with governments?", "Yes. We have built a national archives database for the Haitian government, including citizen records, document uploads, and ministerial validation. We are ready to work with any government entity."),
    ("What technologies do you use?", "We use Python, Streamlit, SQLite, PostgreSQL, OpenAI API, and various TTS/STT libraries. We deploy on Streamlit Cloud and manage code with GitHub."),
    ("How can I contact you?", "You can email us at deslndes78@gmail.com or call/WhatsApp at (509) 4738-5663. We also accept payments via Moncash using Prisme Transfer."),
    ("What is the Haitian flag doing on your avatar?", "The avatar proudly displays the Haitian flag to honor our roots. All our software is made in Haiti, and we are committed to bringing world‑class technology to our country."),
    ("How long does it take to build an app?", "Most applications are delivered within 24 hours after we receive the requirements and payment. Complex systems may take a few days."),
    ("What kind of apps have you built?", "We have built a chess teaching app, a national archives database, an AI app builder (SCORPION), a smart radio suite, an accounting and loan management system, and a talking humanoid AI."),
    ("How do I purchase your software?", "Send payment via Prisme Transfer to Moncash number (509) 4738-5663, then email the confirmation to deslndes78@gmail.com. You will receive the login link, password, and setup guide within 24 hours.")
]

# ----------------------------------------------------------------------
# Main app
# ----------------------------------------------------------------------
if not check_password():
    st.stop()

# Sidebar settings
st.sidebar.image("https://flagcdn.com/w320/ht.png", width=100)
st.sidebar.title("Scorpion AI")
st.sidebar.markdown("**GlobalInternet.py**")
st.sidebar.markdown("Owner: Gesner Deslandes")
st.sidebar.markdown("📧 deslndes78@gmail.com | 📞 (509) 4738-5663")
st.sidebar.markdown("---")

# Demo mode toggle
demo_mode = st.sidebar.checkbox("🎮 Demo Mode (use pre‑defined questions)")
language = st.sidebar.selectbox("Select Language", ["English", "French", "Spanish"], disabled=demo_mode)

# Main area
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f'<div class="avatar-container"><img src="{closed_uri}" id="avatar" style="width:100%; max-width:400px;"></div>', unsafe_allow_html=True)
    
    if demo_mode:
        st.subheader("📋 Example Questions")
        for i, (question, answer) in enumerate(demo_qa):
            if st.button(f"{i+1}. {question}", key=f"demo_q_{i}"):
                st.markdown(f"**You asked:** {question}")
                st.markdown(f"**Scorpion:** {answer}")
                # Animate avatar and speak answer
                st.markdown(f"""
                <script>
                    const avatar = document.getElementById('avatar');
                    const closed = "{closed_uri}";
                    const open = "{open_uri}";
                    let isOpen = false;
                    const interval = setInterval(() => {{
                        if (avatar) {{
                            avatar.src = isOpen ? closed : open;
                            isOpen = !isOpen;
                        }}
                    }}, 200);
                    setTimeout(() => {{
                        clearInterval(interval);
                        if (avatar) avatar.src = closed;
                    }}, 5000);
                </script>
                """, unsafe_allow_html=True)
                speak_text(answer)
    else:
        if st.button("🎙️ Start Voice Interaction"):
            st.write("Listening... Please speak clearly.")
            try:
                audio = mic_recorder(start_prompt="", stop_prompt="", key='recorder')
                if audio:
                    recognizer = sr.Recognizer()
                    text = recognizer.recognize_google(audio)
                    st.write(f"**You said:** {text}")
                    with st.spinner("Thinking..."):
                        response = get_ai_response(text, language)
                        st.write(f"**Scorpion:** {response}")
                        st.markdown(f"""
                        <script>
                            const avatar = document.getElementById('avatar');
                            const closed = "{closed_uri}";
                            const open = "{open_uri}";
                            let isOpen = false;
                            const interval = setInterval(() => {{
                                if (avatar) {{
                                    avatar.src = isOpen ? closed : open;
                                    isOpen = !isOpen;
                                }}
                            }}, 200);
                            setTimeout(() => {{
                                clearInterval(interval);
                                if (avatar) avatar.src = closed;
                            }}, 5000);
                        </script>
                        """, unsafe_allow_html=True)
                        speak_text(response)
                else:
                    st.warning("No audio captured. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with col2:
    st.markdown("### How to use")
    if demo_mode:
        st.markdown("""
        - **Demo Mode** is active. Click any question button below to hear Scorpion's answer.
        - The avatar's mouth will move while Scorpion speaks.
        - This mode does not require an internet connection or OpenAI API key.
        - To use live voice interaction, turn off Demo Mode in the sidebar.
        """)
    else:
        st.markdown("""
        1. Click the **Start Voice Interaction** button.
        2. Speak clearly into your microphone.
        3. Scorpion will transcribe your speech, generate an AI response, and speak back.
        4. The avatar's mouth will move while Scorpion is talking.
        """)
    st.markdown("---")
    st.markdown("### Teaching AI")
    st.markdown("""
    - **Ask questions** about AI, machine learning, or any topic.
    - **Learn English, French, or Spanish** – Scorpion will respond in your chosen language.
    - **Practice conversations** and improve your language skills.
    """)

st.markdown("---")
st.markdown("© 2026 GlobalInternet.py – All rights reserved")
