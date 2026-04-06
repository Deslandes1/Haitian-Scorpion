import streamlit as st
import base64

st.set_page_config(page_title="SCORPION AI - TALKING HUMANOID", layout="wide")

# ----------------------------------------------------------------------
# Authentication with fallback (no KeyError)
# ----------------------------------------------------------------------
def get_expected_password():
    try:
        return st.secrets["password"]
    except KeyError:
        # Fallback to default password if secret is missing
        return "20082010"

def check_password():
    def password_entered():
        if st.session_state["password"] == get_expected_password():
            st.session_state["authenticated"] = True
            del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        # Show login screen with Haitian flag and title
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.image("https://flagcdn.com/w320/ht.png", width=100)
        with col2:
            st.markdown("<h1 style='text-align: center;'>SCORPION AI</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'><em>Talking Humanoid</em></p>", unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style='text-align: right;'>
                <b>GlobalInternet.py</b><br>
                Gesner Deslandes<br>
                Python Developer
            </div>
            """, unsafe_allow_html=True)
        st.divider()
        st.text_input("🔐 Enter password to unlock", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["authenticated"]:
        st.text_input("🔐 Enter password to unlock", type="password", on_change=password_entered, key="password")
        st.error("Wrong password. Access denied.")
        return False
    else:
        return True

# ----------------------------------------------------------------------
# Avatar SVG
# ----------------------------------------------------------------------
svg_avatar = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
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

avatar_data_uri = "data:image/svg+xml;base64," + base64.b64encode(svg_avatar.encode()).decode()

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

# After login, show main interface with flag and title again
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image("https://flagcdn.com/w320/ht.png", width=100)
with col2:
    st.markdown("<h1 style='text-align: center;'>SCORPION AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'><em>Talking Humanoid</em></p>", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style='text-align: right;'>
        <b>GlobalInternet.py</b><br>
        Gesner Deslandes<br>
        Python Developer
    </div>
    """, unsafe_allow_html=True)
st.divider()

# Sidebar
st.sidebar.image("https://flagcdn.com/w320/ht.png", width=100)
st.sidebar.title("SCORPION AI")
st.sidebar.markdown("**GlobalInternet.py**")
st.sidebar.markdown("Owner: Gesner Deslandes")
st.sidebar.markdown("📧 deslndes78@gmail.com | 📞 (509) 4738-5663")
st.sidebar.markdown("---")
st.sidebar.info("Click any question below to see Scorpion's answer.")

col1, col2 = st.columns([1, 2])

with col1:
    st.image(avatar_data_uri, width=300)
    st.subheader("📋 Example Questions")
    for i, (question, answer) in enumerate(demo_qa):
        if st.button(f"{i+1}. {question}", key=f"q_{i}"):
            st.session_state["answer"] = answer
            st.session_state["question"] = question

with col2:
    st.markdown("### 💬 Conversation")
    if "answer" in st.session_state:
        st.markdown(f"**You asked:** {st.session_state['question']}")
        st.markdown(f"**Scorpion:** {st.session_state['answer']}")
    else:
        st.markdown("Click a question button to start.")

st.markdown("---")
st.markdown("© 2026 GlobalInternet.py – All rights reserved")
