import streamlit as st
import pandas as pd
from datetime import datetime
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Mbarek – Time Management AI",
    page_icon="⏰",
    layout="wide"
)

# -----------------------------
# LANGUAGE SWITCH
# -----------------------------
lang = st.toggle("🇫🇷 Français / 🇬🇧 English", value=True)

def t(fr, en):
    return fr if lang else en

# -----------------------------
# SESSION STATE
# -----------------------------
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<style>
.big-title {font-size:42px; font-weight:bold; color:#4CAF50;}
.subtitle {font-size:18px; color: #999;}
.creator {font-size:14px; color:#666;}
.card {background-color:#1e1e1e; padding:20px; border-radius:15px;}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="big-title">⏰ Mbarek – Time Management Assistant</div>
<div class="subtitle">{t("Organise ton temps intelligemment", "Organize your time intelligently")}</div>
""", unsafe_allow_html=True)

# -----------------------------
# USER NAME (WITH BUTTON)
# -----------------------------
st.markdown("### 👤 " + t("Identification", "Identification"))

name_input = st.text_input(
    t("Entre ton prénom", "Enter your name"),
    placeholder="Ex: Mohamed"
)

if st.button(t("➡️ Continuer", "➡️ Continue")):
    if name_input.strip() == "":
        st.error(t("❌ Veuillez entrer votre prénom.", "❌ Please enter your name."))
    else:
        st.session_state.user_name = name_input.strip()

if st.session_state.user_name == "":
    st.stop()

st.success(t(
    f"Bonjour {st.session_state.user_name} 👋 Prêt à optimiser ton temps ?",
    f"Hello {st.session_state.user_name} 👋 Ready to optimize your time?"
))

st.divider()

# -----------------------------
# QUIZ (2 COLUMNS – 10 QUESTIONS)
# -----------------------------
st.markdown("## 📝 " + t("Quiz de gestion du temps", "Time Management Quiz"))

left, right = st.columns(2)

with left:
    q1 = st.text_input("1️⃣ " + t("À quelle heure te lèves-tu ?", "What time do you wake up?"))
    q2 = st.text_input("2️⃣ " + t("À quelle heure dors-tu ?", "What time do you sleep?"))
    q3 = st.text_area("3️⃣ " + t("Décris ta journée actuelle", "Describe your current day"))
    q4 = st.text_area("4️⃣ " + t("Qu'est-ce qui te fait perdre du temps ?", "What wastes your time?"))
    q5 = st.selectbox(
        "5️⃣ " + t("Moment le plus productif", "Most productive moment"),
        ["Matin", "Après-midi", "Soir", "Nuit"]
    )

with right:
    q6 = st.selectbox(
        "6️⃣ " + t("Moment le plus fatiguant", "Most tiring moment"),
        ["Matin", "Après-midi", "Soir", "Nuit"]
    )
    q7 = st.text_area("7️⃣ " + t("Objectifs principaux", "Main goals"))
    q8 = st.text_area("8️⃣ " + t("Temps pour études (heures)", "Study time (hours)"))
    q9 = st.text_area("9️⃣ " + t("Temps pour loisirs", "Leisure time"))
    q10 = st.text_area("🔟 " + t("Que veux-tu améliorer ?", "What do you want to improve?"))

# -----------------------------
# GENERATE BUTTON
# -----------------------------
st.markdown("## ⚙️ " + t("Génération", "Generation"))

if st.button("✨ " + t("Générer mon planning", "Generate my schedule")):

    # Validate
    if not all([q1, q2, q3, q4, q7, q10]):
        st.error(t(
            "❌ Tu dois répondre à toutes les questions importantes.",
            "❌ You must answer all important questions."
        ))
        st.stop()

    with st.spinner(t("Analyse en cours...", "Analyzing...")):
        time.sleep(1.5)

    # -----------------------------
    # SCORE
    # -----------------------------
    score = 100
    if "téléphone" in q4.lower() or "phone" in q4.lower():
        score -= 20
    if "je ne sais pas" in q7.lower():
        score -= 15
    if q5 == q6:
        score -= 10

    score = max(score, 40)

    # -----------------------------
    # DYNAMIC SCHEDULE LOGIC
    # -----------------------------
    schedule = []

    if q5 == "Matin":
        schedule.append(("07:00", "09:00", "Études / Travail profond"))
    elif q5 == "Soir":
        schedule.append(("18:00", "20:00", "Études ciblées"))

    schedule += [
        ("09:00", "12:00", "Cours / Travail"),
        ("12:00", "13:00", "Pause & repas"),
        ("13:00", "16:00", "Révisions / Devoirs"),
        ("16:00", "17:30", "Sport / Marche"),
        ("17:30", "19:00", "Loisirs contrôlés"),
        ("21:00", q2, "Préparation au sommeil")
    ]

    df = pd.DataFrame(schedule, columns=[
        t("Début", "Start"),
        t("Fin", "End"),
        t("Activité", "Activity")
    ])

    # -----------------------------
    # DISPLAY RESULTS
    # -----------------------------
    st.markdown("## 📊 " + t("Résultats", "Results"))

    st.metric(
        t("Score d'organisation", "Organization score"),
        f"{score}/100"
    )

    st.markdown("### 📅 " + t("Planning personnalisé", "Personalized schedule"))
    st.table(df)

    st.markdown("### 💡 " + t("Conseils personnalisés", "Personalized advice"))

    advices = [
        t(
            "• Réduis les distractions pendant tes heures productives.",
            "• Reduce distractions during your productive hours."
        ),
        t(
            "• Respecte une heure de sommeil fixe.",
            "• Keep a fixed sleeping time."
        ),
        t(
            "• Transforme tes objectifs en tâches concrètes.",
            "• Turn goals into concrete tasks."
        ),
        t(
            "• Utilise ton moment fort pour les tâches difficiles.",
            "• Use your peak time for hard tasks."
        )
    ]

    for a in advices:
        st.write(a)

    # -----------------------------
    # SAVE HISTORY
    # -----------------------------
    st.session_state.history.append({
        "time": datetime.now().strftime("%H:%M"),
        "score": score,
        "schedule": df
    })

# -----------------------------
# HISTORY SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("## 📜 " + t("Historique", "History"))

    if st.session_state.history:
        for i, h in enumerate(st.session_state.history[::-1], 1):
            st.markdown(f"**{i}. {h['time']} – {h['score']}/100**")
    else:
        st.info(t("Aucun historique", "No history yet"))

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.markdown("""
<div class="creator">
👨‍💻 Projet réalisé par:<br>
• MED MBAREK<br>
• EYA ALLAH MAHMOUD<br>
• MAJDI EL BEHI<br>
• INSAF EL MATHLOUTHI
</div>
""", unsafe_allow_html=True)

