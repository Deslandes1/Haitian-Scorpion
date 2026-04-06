import streamlit as st
import base64

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

# Sidebar
st.sidebar.image("https://flagcdn.com/w320/ht.png", width=100)
st.sidebar.title("Scorpion AI")
st.sidebar.markdown("**GlobalInternet.py**")
st.sidebar.markdown("Owner: Gesner Deslandes")
st.sidebar.markdown("📧 deslndes78@gmail.com | 📞 (509) 4738-5663")
st.sidebar.markdown("---")
st.sidebar.info("💡 Demo Mode: Click any question button to see Scorpion's answer and watch his lips move.")

# Main area
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f'<div class="avatar-container"><img src="{closed_uri}" id="avatar" style="width:100%; max-width:400px;"></div>', unsafe_allow_html=True)
    
    st.subheader("📋 Example Questions")
    for i, (question, answer) in enumerate(demo_qa):
        if st.button(f"{i+1}. {question}", key=f"demo_q_{i}"):
            st.markdown(f"**You asked:** {question}")
            st.markdown(f"**Scorpion:** {answer}")
            # Animate avatar (mouth moves)
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

with col2:
    st.markdown("### How to use")
    st.markdown("""
    - **Click any question button** on the left.
    - Scorpion will display the answer and his lips will move for 5 seconds, as if he is talking.
    - This demo mode showcases the knowledge Scorpion has about GlobalInternet.py.
    - For live voice interaction, an upgraded version is available (contact us).
    """)
    st.markdown("---")
    st.markdown("### Teaching AI")
    st.markdown("""
    - Scorpion can teach you about AI, Python, software development, and more.
    - Use the demo questions to learn about our company and services.
    - Contact us to integrate real voice interaction and AI responses.
    """)

st.markdown("---")
st.markdown("© 2026 GlobalInternet.py – All rights reserved")
