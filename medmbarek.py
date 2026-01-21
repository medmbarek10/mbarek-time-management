import streamlit as st
import time
import pandas as pd
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Time Management",
    page_icon="⏳",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "logged" not in st.session_state:
    st.session_state.logged = False
if "name" not in st.session_state:
    st.session_state.name = ""
if "lang" not in st.session_state:
    st.session_state.lang = "FR"
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- LANGUAGE SWITCH (ALWAYS SHOWS) ----------------
lang_toggle = st.toggle("🌍 Français / English")
st.session_state.lang = "EN" if lang_toggle else "FR"

def t(fr, en):
    return en if st.session_state.lang == "EN" else fr

# ===================== LOGIN SCREEN =====================
if not st.session_state.logged:

    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("⏳ AI Time Management")
        st.subheader(t(
            "Entre ton prénom pour continuer",
            "Enter your name to continue"
        ))

        name_input = st.text_input(
            t("Ton prénom", "Your name"),
            placeholder="Mohamed"
        )

        if st.button(t("➡️ Continuer", "➡️ Continue"), use_container_width=True):
            if name_input.strip().isalpha():
                st.session_state.name = name_input.strip().title()
                st.session_state.logged = True
                st.rerun()
            else:
                st.error(t(
                    "❌ Prénom invalide (lettres uniquement)",
                    "❌ Invalid name (letters only)"
                ))

    # ⛔ STOP ONLY HERE
    st.stop()

# ===================== MAIN APP =====================
st.title(t(
    f"👋 Salut {st.session_state.name}",
    f"👋 Hello {st.session_state.name}"
))

st.caption(t(
    "Réponds sérieusement pour obtenir un vrai planning personnalisé",
    "Answer seriously to get a real personalized schedule"
))

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.subheader(t("📜 Historique", "📜 History"))
    if not st.session_state.history:
        st.caption(t("Aucun planning", "No schedules yet"))
    else:
        for h in st.session_state.history[-5:]:
            st.markdown(f"- **{h['date']}** · {h['score']}%")

# ---------------- QUESTIONS ----------------
st.subheader(t("📝 Questionnaire", "📝 Questionnaire"))

left, right = st.columns(2)

with left:
    wake = st.text_input(t("1️⃣ Heure de réveil", "1️⃣ Wake-up time"))
    sleep = st.text_input(t("2️⃣ Heure de sommeil", "2️⃣ Sleep time"))
    study = st.slider(t("3️⃣ Heures d'étude / jour", "3️⃣ Study hours/day"), 0, 10, 2)
    phone = st.slider(t("4️⃣ Temps téléphone", "4️⃣ Phone time"), 0, 10, 4)
    productive = st.selectbox(
        t("5️⃣ Moment le plus productif", "5️⃣ Most productive time"),
        [t("Matin", "Morning"), t("Après-midi", "Afternoon"), t("Soir", "Evening"), t("Nuit", "Night")]
    )

with right:
    tired = st.selectbox(
        t("6️⃣ Moment le plus fatigant", "6️⃣ Most tiring time"),
        [t("Matin", "Morning"), t("Après-midi", "Afternoon"), t("Soir", "Evening"), t("Nuit", "Night")]
    )
    goals = st.text_area(t("7️⃣ Objectifs", "7️⃣ Goals"))
    distractions = st.text_area(t("8️⃣ Distractions", "8️⃣ Distractions"))
    improve = st.text_area(t("9️⃣ À améliorer", "9️⃣ What to improve"))
    motivation = st.slider(t("🔟 Motivation", "🔟 Motivation"), 0, 10, 5)

# ---------------- VALIDATION ----------------
def valid(txt):
    return txt and len(txt.strip()) >= 4 and not txt.strip().isnumeric()

# ---------------- GENERATE ----------------
if st.button(t("⚡ Générer mon planning", "⚡ Generate my schedule"), use_container_width=True):

    if not all([
        valid(wake), valid(sleep), valid(goals), valid(distractions), valid(improve)
    ]):
        st.error(t(
            "❌ Réponses invalides ou absurdes détectées",
            "❌ Invalid or nonsense answers detected"
        ))
        st.stop()

    with st.spinner(t("🧠 Analyse en cours...", "🧠 Analyzing...")):
        time.sleep(1.5)

    score = int((motivation + study + (10 - phone)) / 3 * 10)

    schedule = [
        ("07:00", t("Réveil & routine", "Wake up & routine")),
        ("08:00", t("Études prioritaires", "Priority study")),
        ("12:00", t("Pause", "Break")),
        ("14:00", t("Travail ciblé", "Focused work")),
        ("18:00", t("Détente / sport", "Relax / sport")),
        ("22:30", t("Déconnexion & sommeil", "Disconnect & sleep"))
    ]

    df = pd.DataFrame(schedule, columns=[t("Heure", "Time"), t("Activité", "Activity")])

    st.success(t("✅ Planning généré", "✅ Schedule generated"))
    st.table(df)

    st.subheader(t("💡 Conseils personnalisés", "💡 Personalized advice"))
    st.markdown(f"""
    - 🔵 {t("Réduis le téléphone progressivement", "Reduce phone usage gradually")}
    - 🟢 {t("Travaille par blocs de 45 min", "Work in 45-minute blocks")}
    - 🟡 {t("Dors au moins 7h", "Sleep at least 7h")}
    - 🔴 {t("3 priorités max par jour", "Max 3 priorities per day")}
    """)

    st.metric(t("Score de productivité", "Productivity score"), f"{score}%")

    st.session_state.history.append({
        "date": datetime.now().strftime("%d/%m %H:%M"),
        "score": score
    })

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "👨‍💻 MED MBAREK · 👩‍💻 EYA ALLAH MAHMOUD · 👨‍💻 MAJDI EL BEHI · 👩‍💻 INSAF EL MATHLOUTHI"
)
