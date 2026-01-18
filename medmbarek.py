import streamlit as st
from datetime import datetime
import pandas as pd
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Mbarek Chat – Gestion du Temps",
    page_icon="⏳",
    layout="wide"
)

# -----------------------------
# STYLING
# -----------------------------
st.markdown("""
<style>
.advice {
    background-color:#f5f7fa;
    padding:20px;
    border-radius:12px;
}
.planning {
    background-color:#e8f0fe;
    padding:20px;
    border-radius:12px;
}
.footer {
    text-align:center;
    margin-top:30px;
    font-size:14px;
    color:gray;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LANGUAGE SWITCHER
# -----------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "FR"

lang = st.radio("🌐 Language / Langue", ["FR", "EN"], index=0, horizontal=True)
st.session_state.lang = lang

texts = {
    "FR": {
        "title": "⏳ Mbarek Chat – Gestion du Temps Intelligente",
        "upload": "📂 Téléverse ton emploi du temps (optionnel)",
        "quiz": "📝 Quiz de Gestion du Temps (réponds en français)",
        "generate": "🚀 Générer mon planning",
        "history": "📜 Historique",
        "advice": "💡 Conseils personnalisés",
        "footer": "Projet réalisé par : MED MBAREK – EYA ALLAH MAHMOUD – MAJDI EL BEHI – INSAF EL MATHLOUTHI",
        "table_headers": ["Heure", "Activité"]
    },
    "EN": {
        "title": "⏳ Mbarek Chat – Smart Time Management",
        "upload": "📂 Upload your schedule (optional)",
        "quiz": "📝 Time Management Quiz (answer in English)",
        "generate": "🚀 Generate My Schedule",
        "history": "📜 History",
        "advice": "💡 Personalized Advice",
        "footer": "Project by: MED MBAREK – EYA ALLAH MAHMOUD – MAJDI EL BEHI – INSAF EL MATHLOUTHI",
        "table_headers": ["Time", "Activity"]
    }
}

st.title(texts[lang]["title"])
st.subheader(texts[lang]["upload"])

# -----------------------------
# SESSION STATE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# UPLOAD CSV (OPTIONAL)
# -----------------------------
uploaded_file = st.file_uploader(f"{texts[lang]['upload']}", type=["csv"])
schedule_text = ""
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if "Titre" in df.columns and "Date" in df.columns:
        for _, row in df.iterrows():
            schedule_text += f"- {row['Titre']} (avant {row['Date']})\n"
        st.success("✅ Emploi du temps chargé" if lang=="FR" else "✅ Schedule uploaded")

# -----------------------------
# QUIZ
# -----------------------------
st.subheader(texts[lang]["quiz"])
with st.form("quiz"):
    col1, col2 = st.columns(2)

    with col1:
        q1 = st.text_input("1️⃣ " + ("À quelle heure te lèves-tu habituellement ?" if lang=="FR" else "What time do you usually wake up?"))
        q2 = st.text_input("2️⃣ " + ("Pourquoi te lèves-tu à cette heure ?" if lang=="FR" else "Why do you wake up at this time?"))
        q3 = st.text_area("3️⃣ " + ("Temps pour chaque activité quotidienne" if lang=="FR" else "Time spent on each daily activity"))
        q4 = st.text_area("4️⃣ " + ("Pourquoi ton emploi du temps ne te satisfait pas ?" if lang=="FR" else "Why is your schedule unsatisfying?"))
        q5 = st.text_area("5️⃣ " + ("Activités à réduire (et de combien)" if lang=="FR" else "Activities to reduce (and by how much)"))

    with col2:
        q6 = st.text_area("6️⃣ " + ("Activités à ajouter (et durée)" if lang=="FR" else "Activities to add (and duration)"))
        q7 = st.selectbox("7️⃣ " + ("Moment où tu es le plus concentré" if lang=="FR" else "Time of peak focus"), ["Matin","Après-midi","Soir","Nuit"] if lang=="FR" else ["Morning","Afternoon","Evening","Night"])
        q8 = st.selectbox("8️⃣ " + ("Moment où tu es le plus fatigué" if lang=="FR" else "Time of least energy"), ["Matin","Après-midi","Soir","Nuit"] if lang=="FR" else ["Morning","Afternoon","Evening","Night"])
        q9 = st.text_area("9️⃣ " + ("Principales distractions" if lang=="FR" else "Main distractions"))
        q10 = st.selectbox("🔟 " + ("Te sens-tu débordé ?" if lang=="FR" else "Do you feel overwhelmed?"), ["Oui","Non"] if lang=="FR" else ["Yes","No"])

    submit = st.form_submit_button(texts[lang]["generate"])

# -----------------------------
# PLANNINGS
# -----------------------------
plannings = [
    {
        "name":"🌅 Planning Matinal Ultra-Productif",
        "energy":"Matin",
        "daily":[
            ("06:30","Réveil + hydratation + étirements"),
            ("07:00","Étude profonde (45 min)"),
            ("08:00","Petit-déjeuner"),
            ("09:00","Cours / travail"),
            ("13:00","Pause"),
            ("16:30","Révisions"),
            ("18:00","Sport"),
            ("20:00","Temps libre"),
            ("22:00","Déconnexion"),
            ("22:30","Sommeil")
        ],
        "weekly":"Début de semaine intense",
        "score":0
    },
    {
        "name":"🌙 Planning Soir Concentration Maximale",
        "energy":"Soir",
        "daily":[
            ("08:30","Réveil"),
            ("09:30","Cours / obligations"),
            ("13:30","Pause"),
            ("17:00","Repos"),
            ("19:00","Études intensives"),
            ("21:30","Révisions"),
            ("22:30","Déconnexion"),
            ("23:30","Sommeil")
        ],
        "weekly":"Productivité en soirée",
        "score":0
    },
    {
        "name":"⚖️ Planning Équilibré Durable",
        "energy":"Après-midi",
        "daily":[
            ("07:30","Réveil"),
            ("08:30","Cours"),
            ("13:30","Pause"),
            ("15:30","Étude"),
            ("17:30","Loisirs / sport"),
            ("19:30","Révisions"),
            ("21:30","Déconnexion"),
            ("22:30","Sommeil")
        ],
        "weekly":"Prévention du burn-out",
        "score":0
    }
]

# -----------------------------
# GENERATION
# -----------------------------
if submit:
    if not all([q1,q2,q3,q4,q5,q6,q9]):
        st.error("❌ " + ("Tu dois remplir toutes les questions" if lang=="FR" else "You must fill all the questions"))
    else:
        with st.spinner("🧠 " + ("Analyse en cours..." if lang=="FR" else "Analyzing...")):
            time.sleep(1.5)

        # Score each planning
        for p in plannings:
            if p["energy"] == q7:
                p["score"] += 3
            if q8 != p["energy"]:
                p["score"] += 1
            if q10 == ("Oui" if lang=="FR" else "Yes") and "Équilibré" in p["name"]:
                p["score"] += 2

        best = max(plannings, key=lambda x:x["score"])

        st.markdown('<div class="planning">', unsafe_allow_html=True)
        st.subheader(f"📅 {best['name']}")

        df_schedule = pd.DataFrame(best["daily"], columns=texts[lang]["table_headers"])
        st.table(df_schedule)
        st.markdown(f"**{('Stratégie hebdomadaire' if lang=='FR' else 'Weekly Strategy')}:** {best['weekly']}")
        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # ADVICES
        # -----------------------------
        st.markdown('<div class="advice">', unsafe_allow_html=True)
        st.subheader(texts[lang]["advice"])
        st.markdown("- Planifie la veille / Plan the night before")
        st.markdown("- Travaille par blocs de 45 minutes / Work in 45-min blocks")
        if "téléphone" in q9.lower() or "réseaux" in q9.lower():
            st.markdown("- Téléphone hors de portée / Keep phone away")
        if q10 == ("Oui" if lang=="FR" else "Yes"):
            st.markdown("- Réduis tes objectifs / Reduce daily goals")
        st.markdown("- Garde une heure de coucher fixe / Maintain fixed sleep time")
        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # HISTORY
        # -----------------------------
        st.session_state.history.append({
            "time": datetime.now().strftime("%H:%M"),
            "planning": best["name"]
        })

# -----------------------------
# SIDEBAR HISTORY
# -----------------------------
with st.sidebar:
    st.subheader(texts[lang]["history"])
    for h in st.session_state.history[::-1]:
        st.markdown(f"- {h['time']} → {h['planning']}")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown(f"""
<div class="footer">
{texts[lang]['footer']}
</div>
""", unsafe_allow_html=True)







