import google.generativeai as genai
import streamlit as st
from datetime import datetime
import pandas as pd

# -----------------------------
# Configuration AI
# -----------------------------
genai.configure(api_key='AIzaSyAjKkzbGeLNLREvNLsH0RCMRNmSKkf09ag')
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("Mbarek Chat - Gestion du Temps")

# -----------------------------
# Prompt Système
# -----------------------------
system_prompt = ("""Vous êtes une IA professionnelle de gestion du temps.
Analysez l'emploi du temps téléchargé de l'utilisateur et ses réponses au quiz pour créer un planning quotidien personnalisé, équilibrant travail, études, divertissement et santé. Soyez clair, concis et proposez des actions concrètes.
""")

# -----------------------------
# État de session
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Upload de l'emploi du temps
# -----------------------------
st.subheader("1️⃣ Téléversez votre emploi du temps actuel (optionnel)")
uploaded_file = st.file_uploader("Téléversez un fichier CSV avec vos tâches (Titre, Date)", type=["csv"])

schedule_text = ""
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        if "Titre" in df.columns and "Date" in df.columns:
            schedule_text = "Voici l'emploi du temps actuel de l'utilisateur :\n"
            for idx, row in df.iterrows():
                schedule_text += f"- {row['Titre']} (Date limite : {row['Date']})\n"
            st.success("✅ Emploi du temps téléchargé avec succès !")
        else:
            st.warning("⚠️ Le CSV doit contenir les colonnes : Titre, Date")
    except Exception as e:
        st.error(f"⚠️ Erreur lors de la lecture du fichier : {e}")

# -----------------------------
# Quiz de gestion du temps
# -----------------------------
st.subheader("2️⃣ Répondez au Quiz de Gestion du Temps")

with st.form("time_management_quiz"):
    q2 = st.text_input("2- Pourquoi vous levez-vous si tôt/tard ?")
    q3 = st.text_area("3- Combien de temps consacrez-vous à chaque activité quotidienne ?")
    q4 = st.text_area("4- Pourquoi êtes-vous insatisfait de votre emploi du temps ?")
    q5 = st.text_area("5- Quelles activités souhaitez-vous réduire et de combien de temps ?")
    q6 = st.text_area("6- Quelles activités souhaitez-vous ajouter ou consacrer plus de temps ? Combien de temps ?")
    q7 = st.selectbox("7- À quel moment de la journée vous sentez-vous le plus énergique/focalisé ?", ["Matin", "Après-midi", "Soir", "Nuit"])
    q8 = st.selectbox("8- À quel moment de la journée vous sentez-vous le plus fatigué/distrait ?", ["Matin", "Après-midi", "Soir", "Nuit"])
    q9 = st.text_area("9- Qu'est-ce qui vous distrait habituellement de vos objectifs ?")
    q10 = st.text_area("10- Vous sentez-vous débordé par votre emploi du temps ou avez-vous l'impression de ne pas en faire assez ?")

    submitted = st.form_submit_button("Générer le planning personnalisé")

# -----------------------------
# Génération de la réponse AI
# -----------------------------
if submitted:
    user_responses = f"""
    2. Pourquoi vous levez-vous si tôt/tard ? {q2}
    3. Temps consacré aux activités quotidiennes : {q3}
    4. Pourquoi insatisfait de l'emploi du temps : {q4}
    5. Activités à réduire : {q5}
    6. Activités à ajouter / plus de temps : {q6}
    7. Moment de pic d'énergie : {q7}
    8. Moment de faible énergie : {q8}
    9. Distractions habituelles : {q9}
    10. Sentiment sur l'emploi du temps : {q10}
    """

    # Combiner emploi du temps uploadé et réponses
    full_prompt = system_prompt
    if schedule_text:
        full_prompt += "\nEmploi du temps téléchargé :\n" + schedule_text
    full_prompt += "\nRéponses de l'utilisateur :\n" + user_responses + "\nIA :"

    # Génération du texte par AI
    response = model.generate_content(full_prompt)
    generated_text = response.text

    st.write("### 📋 Planning personnalisé & recommandations")
    st.write(generated_text)

    # Sauvegarder l'historique
    st.session_state.chat_history.append({
        "prompt": full_prompt,
        "response": generated_text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# -----------------------------
# Historique facultatif
# -----------------------------
if st.button("📜 Afficher / Cacher l'historique du chat"):
    if st.session_state.chat_history:
        for idx, chat in enumerate(st.session_state.chat_history, 1):
            st.markdown(f"**{idx}. Prompt :** {chat['prompt']}")
            st.markdown(f"**Réponse IA :** {chat['response']}")
            st.markdown(f"_À : {chat['time']}_")
    else:
        st.info("Aucun historique pour le moment !")
 