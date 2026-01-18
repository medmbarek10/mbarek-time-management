import streamlit as st
from datetime import datetime
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

# -----------------------------
# Page Config & Title
# -----------------------------
st.set_page_config(page_title="Mbarek Chat - Gestion du Temps", layout="wide")
st.title("Mbarek Chat - Gestion du Temps")

# -----------------------------
# Session State
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "warning_fields" not in st.session_state:
    st.session_state.warning_fields = []

# -----------------------------
# Upload CSV Schedule
# -----------------------------
st.subheader("1️⃣ Téléversez votre emploi du temps actuel (optionnel)")
uploaded_file = st.file_uploader(
    "Téléversez un fichier CSV avec vos tâches (Titre, Date)", type=["csv"]
)

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
# Quiz Form: 10 questions (5 left, 5 right)
# -----------------------------
st.subheader("2️⃣ Répondez au Quiz de Gestion du Temps")

with st.form("time_management_quiz"):
    col1, col2 = st.columns(2)

    with col1:
        q1 = st.text_input("1- À quelle heure vous levez-vous généralement ?")
        q2 = st.text_input("2- Pourquoi vous levez-vous si tôt/tard ?")
        q3 = st.text_area("3- Combien de temps consacrez-vous à chaque activité quotidienne ?")
        q4 = st.text_area("4- Pourquoi êtes-vous insatisfait de votre emploi du temps ?")
        q5 = st.text_area("5- Quelles activités souhaitez-vous réduire et de combien de temps ?")

    with col2:
        q6 = st.text_area("6- Quelles activités souhaitez-vous ajouter ou consacrer plus de temps ? Combien de temps ?")
        q7 = st.selectbox("7- À quel moment de la journée vous sentez-vous le plus énergique/focalisé ?", ["Matin", "Après-midi", "Soir", "Nuit"])
        q8 = st.selectbox("8- À quel moment de la journée vous sentez-vous le plus fatigué/distrait ?", ["Matin", "Après-midi", "Soir", "Nuit"])
        q9 = st.text_area("9- Qu'est-ce qui vous distrait habituellement de vos objectifs ?")
        q10 = st.text_area("10- Vous sentez-vous débordé par votre emploi du temps ou avez-vous l'impression de ne pas en faire assez ?")

    submitted = st.form_submit_button("Générer le planning personnalisé")

# -----------------------------
# Validation for empty fields
# -----------------------------
required_fields = {
    "1": q1, "2": q2, "3": q3, "4": q4, "5": q5,
    "6": q6, "7": q7, "8": q8, "9": q9, "10": q10
}

empty_fields = [k for k, v in required_fields.items() if not v.strip()]
if submitted and empty_fields:
    st.warning("⚠️ Vous devez répondre à toutes les questions en français !")
    st.session_state.warning_fields = empty_fields
else:
    st.session_state.warning_fields = []

# -----------------------------
# Intelligent Schedule Generator
# -----------------------------
def generate_plan(answers_dict, schedule_text):
    morning = []
    afternoon = []
    evening = []
    advice = []

    # Extract key info
    wake_time = answers_dict["1"].strip()
    reason_wake = answers_dict["2"].strip()
    time_per_activity = answers_dict["3"].strip()
    dissatisfaction = answers_dict["4"].strip()
    reduce_activities = answers_dict["5"].strip()
    add_activities = answers_dict["6"].strip()
    peak_energy = answers_dict["7"].strip()
    low_energy = answers_dict["8"].strip()
    distractions = answers_dict["9"].strip()
    overwhelm = answers_dict["10"].strip()

    # Morning Block
    morning.append(f"- Réveil à {wake_time}. Commencez par une activité motivante (ex: étirement, planification).")
    if peak_energy.lower() == "matin":
        morning.append("- Moment de haute énergie ! Effectuez vos tâches importantes maintenant.")
    else:
        morning.append("- Moment moins optimal. Faites des tâches légères ou préparations pour la journée.")

    # Afternoon Block
    if peak_energy.lower() == "après-midi":
        afternoon.append("- Moment de haute énergie ! Priorisez les tâches importantes.")
    else:
        afternoon.append("- Moment moyen. Tâches modérées ou réunions légères.")
    afternoon.append(f"- Activités à ajouter : {add_activities}")
    afternoon.append(f"- Réduire ces activités : {reduce_activities}")

    # Evening Block
    if peak_energy.lower() == "soir":
        evening.append("- Moment de haute énergie ! Dernières tâches importantes ou projets personnels.")
    else:
        evening.append("- Moment plus calme. Détente ou préparation pour demain.")
    evening.append(f"- Réflexion sur la journée : {dissatisfaction}")
    evening.append(f"- Éviter distractions : {distractions}")

    # General Advice
    advice.append(f"- Pourquoi vous levez-vous à cette heure : {reason_wake}")
    advice.append(f"- Temps consacré aux activités : {time_per_activity}")
    if overwhelm:
        advice.append(f"- Sentiment débordé : {overwhelm} → Priorisez et déléguez si possible.")
    advice.append("- Respectez vos pics d'énergie pour les tâches difficiles et prenez des pauses régulières.")
    advice.append("- Techniques anti-distraction : notifications coupées, téléphone éloigné, environnement calme.")

    # Integrate uploaded schedule
    if schedule_text:
        advice.append("\nVotre emploi du temps actuel :\n" + schedule_text)
        advice.append("💡 Conseil : réorganisez vos tâches selon vos pics d'énergie et moments de faible énergie.")

    # Build final formatted plan
    final_plan = "### 📋 Planning quotidien personnalisé\n\n"
    final_plan += "#### 🌅 Matin\n" + "\n".join(morning) + "\n\n"
    final_plan += "#### ☀️ Après-midi\n" + "\n".join(afternoon) + "\n\n"
    final_plan += "#### 🌙 Soir\n" + "\n".join(evening) + "\n\n"
    final_plan += "### 💡 Conseils généraux\n" + "\n".join(advice)

    return final_plan

# -----------------------------
# Convert text to PNG for download
# -----------------------------
def text_to_png(text, file_name="planning.png"):
    lines = text.split("\n")
    width = 800
    line_height = 25
    height = line_height * (len(lines) + 2)
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()
    y = 10
    for line in lines:
        draw.text((10, y), line, fill='black', font=font)
        y += line_height
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

# -----------------------------
# Generate plan if all fields filled
# -----------------------------
if submitted and not empty_fields:
    answers_dict = {k: v for k, v in required_fields.items()}
    generated_text = generate_plan(answers_dict, schedule_text)

    st.write("### 📋 Planning personnalisé & recommandations")
    st.write(generated_text)

    # Save to history
    st.session_state.chat_history.append({
        "answers": answers_dict,
        "response": generated_text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # -----------------------------
    # Download as TXT
    # -----------------------------
    schedule_bytes = io.BytesIO()
    schedule_bytes.write(generated_text.encode('utf-8'))
    schedule_bytes.seek(0)
    st.download_button(
        label="📥 Télécharger le planning (TXT)",
        data=schedule_bytes,
        file_name="planning_personnalise.txt",
        mime="text/plain"
    )

    # -----------------------------
    # Download as PNG
    # -----------------------------
    img_bytes = text_to_png(generated_text)
    st.download_button(
        label="📥 Télécharger le planning (PNG)",
        data=img_bytes,
        file_name="planning_personnalise.png",
        mime="image/png"
    )

# -----------------------------
# Sidebar History
# -----------------------------
with st.sidebar:
    st.subheader("📜 Historique du chat")
    if st.session_state.chat_history:
        for idx, chat in enumerate(st.session_state.chat_history, 1):
            st.markdown(f"**{idx}. Généré à :** {chat['time']}")
            st.markdown(f"**Réponses fournies :** {chat['answers']}")
            st.markdown(f"**Plan :** {chat['response']}")
    else:
        st.info("Aucun historique pour le moment !")

# -----------------------------
# Footer / Creator Tag
# -----------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray; font-size:12px;'>Créé par MED MBAREK, EYA ALLAH MAHMOUD, MAJDI EL BEHI, INSAF EL MATHLOUTHI</p>",
    unsafe_allow_html=True
)
