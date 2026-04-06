import streamlit as st
import base64
from gtts import gTTS
import io
import time

st.set_page_config(page_title="SCORPION AI - TALKING HUMANOID", layout="wide")

# ----------------------------------------------------------------------
# Authentication with fallback (no KeyError)
# ----------------------------------------------------------------------
def get_expected_password():
    try:
        return st.secrets["password"]
    except KeyError:
        return "20082010"

def check_password():
    def password_entered():
        if st.session_state["password"] == get_expected_password():
            st.session_state["authenticated"] = True
            del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
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
# Avatar SVG (static)
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
# Demo questions and answers (in three languages)
# ----------------------------------------------------------------------
qa_data = {
    "English": [
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
    ],
    "French": [
        ("Qu'est-ce que GlobalInternet.py ?", "GlobalInternet.py est une entreprise de logiciels basée en Haïti, fondée par Gesner Deslandes. Nous construisons des applications web personnalisées, des outils d'IA et des systèmes de bases de données pour les entreprises, les gouvernements et les particuliers."),
        ("Qui est Gesner Deslandes ?", "Gesner Deslandes est le propriétaire et le développeur Python principal de GlobalInternet.py. Il est un développeur autodidacte qui utilise l'IA pour construire des applications plus rapidement, en se concentrant sur l'architecture et l'expérience utilisateur."),
        ("Quels services offrez-vous ?", "Nous offrons le développement d'applications web complètes, des outils alimentés par l'IA, des systèmes de bases de données, des logiciels de comptabilité, des systèmes de gestion de prêts et des solutions personnalisées. Toutes les applications sont déployées sur Streamlit Cloud et livrées dans les 24 heures."),
        ("Pouvez-vous construire un logiciel personnalisé pour mon entreprise ?", "Absolument. Nous écoutons vos besoins, concevons l'architecture, construisons l'application, la testons et la déployons. Vous obtenez un produit fonctionnel en quelques jours, pas en quelques mois."),
        ("Quel est le coût de vos services ?", "Chaque application est tarifée individuellement en fonction de sa complexité. Notre logiciel de comptabilité, par exemple, coûte 149 $ une fois. Pour un travail personnalisé, nous fournissons un devis après avoir compris vos besoins."),
        ("Travaillez-vous avec les gouvernements ?", "Oui. Nous avons construit une base de données d'archives nationales pour le gouvernement haïtien, comprenant les dossiers des citoyens, le téléchargement de documents et la validation ministérielle. Nous sommes prêts à travailler avec toute entité gouvernementale."),
        ("Quelles technologies utilisez-vous ?", "Nous utilisons Python, Streamlit, SQLite, PostgreSQL, l'API OpenAI et diverses bibliothèques TTS/STT. Nous déployons sur Streamlit Cloud et gérons le code avec GitHub."),
        ("Comment puis-vous contacter ?", "Vous pouvez nous envoyer un courriel à deslndes78@gmail.com ou appeler/WhatsApp au (509) 4738-5663. Nous acceptons également les paiements via Moncash en utilisant Prisme Transfer."),
        ("Que fait le drapeau haïtien sur votre avatar ?", "L'avatar arbore fièrement le drapeau haïtien pour honorer nos racines. Tous nos logiciels sont fabriqués en Haïti, et nous nous engageons à apporter une technologie de classe mondiale à notre pays."),
        ("Combien de temps faut-il pour construire une application ?", "La plupart des applications sont livrées dans les 24 heures suivant la réception des exigences et du paiement. Les systèmes complexes peuvent prendre quelques jours."),
        ("Quel genre d'applications avez-vous construites ?", "Nous avons construit une application d'enseignement des échecs, une base de données d'archives nationales, un constructeur d'applications IA (SCORPION), une suite radio intelligente, un système de comptabilité et de gestion de prêts, et un humanoïde parlant IA."),
        ("Comment acheter votre logiciel ?", "Envoyez le paiement par Prisme Transfer au numéro Moncash (509) 4738-5663, puis envoyez la confirmation par courriel à deslndes78@gmail.com. Vous recevrez le lien de connexion, le mot de passe et le guide d'installation dans les 24 heures.")
    ],
    "Spanish": [
        ("¿Qué es GlobalInternet.py?", "GlobalInternet.py es una empresa de software con sede en Haití, fundada por Gesner Deslandes. Construimos aplicaciones web personalizadas, herramientas de IA y sistemas de bases de datos para empresas, gobiernos y particulares."),
        ("¿Quién es Gesner Deslandes?", "Gesner Deslandes es el propietario y desarrollador principal de Python de GlobalInternet.py. Es un desarrollador autodidacta que utiliza la IA para construir aplicaciones más rápido, centrándose en la arquitectura y la experiencia del usuario."),
        ("¿Qué servicios ofrecen?", "Ofrecemos desarrollo de aplicaciones web completas, herramientas impulsadas por IA, sistemas de bases de datos, software de contabilidad, sistemas de gestión de préstamos y soluciones personalizadas. Todas las aplicaciones se despliegan en Streamlit Cloud y se entregan en 24 horas."),
        ("¿Pueden construir software personalizado para mi negocio?", "Absolutamente. Escuchamos sus necesidades, diseñamos la arquitectura, construimos la aplicación, la probamos y la desplegamos. Obtiene un producto funcional en días, no en meses."),
        ("¿Cuál es el costo de sus servicios?", "Cada aplicación tiene un precio individual según su complejidad. Nuestro software de contabilidad, por ejemplo, cuesta $149 por única vez. Para trabajos personalizados, proporcionamos un presupuesto después de comprender sus requisitos."),
        ("¿Trabajan con gobiernos?", "Sí. Hemos construido una base de datos de archivos nacionales para el gobierno haitiano, que incluye registros de ciudadanos, carga de documentos y validación ministerial. Estamos listos para trabajar con cualquier entidad gubernamental."),
        ("¿Qué tecnologías utilizan?", "Usamos Python, Streamlit, SQLite, PostgreSQL, la API de OpenAI y varias bibliotecas TTS/STT. Desplegamos en Streamlit Cloud y gestionamos el código con GitHub."),
        ("¿Cómo puedo contactarlos?", "Puede enviarnos un correo electrónico a deslndes78@gmail.com o llamar/WhatsApp al (509) 4738-5663. También aceptamos pagos a través de Moncash usando Prisme Transfer."),
        ("¿Qué hace la bandera haitiana en su avatar?", "El avatar muestra con orgullo la bandera haitiana para honrar nuestras raíces. Todo nuestro software está hecho en Haití, y estamos comprometidos a llevar tecnología de clase mundial a nuestro país."),
        ("¿Cuánto tiempo lleva construir una aplicación?", "La mayoría de las aplicaciones se entregan dentro de las 24 horas posteriores a la recepción de los requisitos y el pago. Los sistemas complejos pueden tardar unos días."),
        ("¿Qué tipo de aplicaciones han construido?", "Hemos construido una aplicación de enseñanza de ajedrez, una base de datos de archivos nacionales, un constructor de aplicaciones de IA (SCORPION), una suite de radio inteligente, un sistema de contabilidad y gestión de préstamos, y un humanoide parlante de IA."),
        ("¿Cómo compro su software?", "Envíe el pago mediante Prisme Transfer al número de Moncash (509) 4738-5663, luego envíe la confirmación por correo electrónico a deslndes78@gmail.com. Recibirá el enlace de inicio de sesión, la contraseña y la guía de instalación en 24 horas.")
    ]
}

# ----------------------------------------------------------------------
# Audio generation using gTTS
# ----------------------------------------------------------------------
def text_to_speech(text, lang_code):
    tts = gTTS(text=text, lang=lang_code, slow=False)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

# ----------------------------------------------------------------------
# Main app
# ----------------------------------------------------------------------
if not check_password():
    st.stop()

# After login, show main interface
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
language = st.sidebar.selectbox("Select Language", ["English", "French", "Spanish"])
st.sidebar.info("Click a question below. Scorpion will answer in text and audio in your chosen language.")

col1, col2 = st.columns([1, 2])

with col1:
    st.image(avatar_data_uri, width=300)
    st.subheader("📋 Example Questions")
    lang_qa = qa_data[language]
    for i, (question, answer) in enumerate(lang_qa):
        if st.button(f"{i+1}. {question}", key=f"q_{i}"):
            st.session_state["answer"] = answer
            st.session_state["question"] = question
            # Generate audio
            lang_code = {"English": "en", "French": "fr", "Spanish": "es"}[language]
            audio_bytes = text_to_speech(answer, lang_code)
            st.session_state["audio_bytes"] = audio_bytes

with col2:
    st.markdown("### 💬 Conversation")
    if "answer" in st.session_state:
        st.markdown(f"**You asked:** {st.session_state['question']}")
        st.markdown(f"**Scorpion:** {st.session_state['answer']}")
        if "audio_bytes" in st.session_state:
            st.audio(st.session_state["audio_bytes"], format="audio/mp3")
    else:
        st.markdown("Click a question button to start.")

st.markdown("---")
st.markdown("© 2026 GlobalInternet.py – All rights reserved")
