import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title=" - Gestion du Temps", layout="wide")

st.title("Gestion du Temps (Logic-Based AI)")

system_prompt = """Vous êtes un assistant expert en gestion du temps.
Analysez les réponses de l'utilisateur et son emploi du temps pour créer un planning quotidien
personnalisé et équilibré entre études, travail, santé et divertissement."""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Upload CSV schedule
st.subheader("1️⃣ Téléversez votre emploi du temps actuel (optionnel)")
uploaded_file = st.file_uploader("Téléversez un fichier CSV avec vos tâches (Titre, Date)", type=["csv"])

schedule_text = ""
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        if "Titre" in df.columns and "Date" in df.columns:
            schedule_text = "Emploi du temps actuel de l'utilisateur :\n"
            for _, row in df.iterrows():
                schedule_text += f"- {row['Titre']} (Date limite : {row['Date']})\n"
            st.success("✅ Emploi du temps téléchargé avec succès !")
        else:
            st.warning("⚠️ Le CSV doit contenir les colonnes : Titre, Date")
    except Exception as e:
        st.error(f"⚠️ Erreur lors de la lecture du fichier : {e}")

# Quiz form
st.subheader("2️⃣ Répondez au Quiz de Gestion du Temps")

with st.form("time_management_quiz"):
    col1, col2 = st.columns(2)

    with col1:
        q1 = st.text_input("1- Pourquoi vous levez-vous si tôt/tard ?")
        q2 = st.text_area("2- Combien de temps consacrez-vous à chaque activité quotidienne ?")
        q3 = st.text_area("3- Pourquoi êtes-vous insatisfait de votre emploi du temps ?")
        q4 = st.text_area("4- Quelles activités souhaitez-vous réduire et de combien de temps ?")
        q5 = st.text_area("5- Quelles activités souhaitez-vous ajouter ou consacrer plus de temps ? Combien de temps ?")

    with col2:
        q6 = st.selectbox("6- À quel moment de la journée vous sentez-vous le plus énergique/focalisé ?", ["", "Matin", "Après-midi", "Soir", "Nuit"])
        q7 = st.selectbox("7- À quel moment de la journée vous sentez-vous le plus fatigué/distrait ?", ["", "Matin", "Après-midi", "Soir", "Nuit"])
        q8 = st.text_area("8- Qu'est-ce qui vous distrait habituellement de vos objectifs ?")
        q9 = st.text_area("9- Vous sentez-vous débordé par votre emploi du temps ou avez-vous l'impression de ne pas en faire assez ?")
        q10 = st.text_area("10- Comment aimeriez-vous équilibrer vos études et vos moments de détente ?")

    submitted = st.form_submit_button("Générer le planning personnalisé")

    # -----------------------------
    # Validate answers
    # -----------------------------
    required_fields = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    missing = [i+1 for i, f in enumerate(required_fields) if not f.strip()]

    if submitted:
        if missing:
            st.error(f"⚠️ Veuillez répondre à toutes les questions en français. Questions manquantes: {missing}")
            submitted = False  # prevent generation

# -----------------------------
# Logic-based AI generator
# -----------------------------
def generate_logic_plan(answers, schedule=""):
    """
    Analyze answers and generate a personalized plan using logic.
    """
    def summarize_text(text):
        return [line.strip() for line in text.split('.') if line.strip()]

    plan = "### 📋 Planning personnalisé & recommandations\n\n"

    if schedule:
        plan += "**Emploi du temps actuel:**\n" + schedule + "\n"

    plan += f"- Vous êtes le plus énergique : {answers['q6']}\n"
    plan += f"- Vous êtes le moins énergique : {answers['q7']}\n"

    dissatisfaction_points = summarize_text(answers['q3'])
    if dissatisfaction_points:
        plan += "- Points à améliorer dans l'emploi du temps:\n"
        for p in dissatisfaction_points:
            plan += f"  • {p}\n"

    reduce_points = summarize_text(answers['q4'])
    add_points = summarize_text(answers['q5'])

    if reduce_points:
        plan += "- Activités à réduire:\n"
        for p in reduce_points:
            plan += f"  • {p}\n"

    if add_points:
        plan += "- Activités à ajouter / consacrer plus de temps:\n"
        for p in add_points:
            plan += f"  • {p}\n"

    distractions = summarize_text(answers['q8'])
    if distractions:
        plan += "- Distractions fréquentes:\n"
        for d in distractions:
            plan += f"  • {d}\n"

    if "débordé" in answers['q9'].lower() or "pas en faire assez" in answers['q9'].lower():
        plan += "- Recommandation: Priorisez vos tâches importantes et créez des blocs de temps dédiés.\n"

    if answers['q1']:
        plan += f"- Motivation pour le réveil: {answers['q1']}\n"

    if answers['q2']:
        plan += f"- Temps actuel pour chaque activité: {answers['q2']}\n"

    if answers['q10']:
        plan += f"- Équilibre études / détente: {answers['q10']}\n"

    return plan

# -----------------------------
# Generate plan on submit
# -----------------------------
if submitted:
    answers = {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q4": q4,
        "q5": q5,
        "q6": q6,
        "q7": q7,
        "q8": q8,
        "q9": q9,
        "q10": q10
    }

    full_plan = generate_logic_plan(answers, schedule_text)
    st.markdown(full_plan)

    # Save history
    st.session_state.chat_history.append({
        "answers": answers,
        "plan": full_plan,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# -----------------------------
# History panel on the left
# -----------------------------
with st.sidebar:
    st.header("📜 Historique")
    if st.button("Afficher / Cacher l'historique"):
        if st.session_state.chat_history:
            for idx, h in enumerate(st.session_state.chat_history, 1):
                st.markdown(f"**{idx}. Réponses:**")
                for k,v in h['answers'].items():
                    st.markdown(f"- {k}: {v}")
                st.markdown(f"**Plan généré:**\n{h['plan']}")
                st.markdown(f"_À : {h['time']}_")
        else:
            st.info("Aucun historique pour le moment !")




 